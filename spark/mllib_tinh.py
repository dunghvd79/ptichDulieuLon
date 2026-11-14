"""Spark MLlib trên bảng 34 tỉnh (đầu ra của etl_diemthi.py).

1. Hồi quy tuyến tính (Pipeline: VectorAssembler -> StandardScaler -> LinearRegression)
   - n = 34 rất nhỏ -> đánh giá bằng REPEATED K-FOLD (5 fold x 5 lần lặp, seed cố định),
     so với mốc "dự đoán bằng trung bình tập train". R²_cv = 1 - SSE_mô_hình / SSE_mốc
     (ngoài mẫu; có thể âm nếu mô hình tệ hơn đoán trung bình).
   - Fit OLS trên toàn bộ 34 tỉnh để lấy hệ số chuẩn hóa, p-value, R² trong mẫu.
   - VIF để kiểm tra đa cộng tuyến của mô hình đa biến.
2. KMeans phân cụm tỉnh trên biến KT-XH + điểm đã chuẩn hóa, k = 2..6, chọn k theo
   silhouette (ClusteringEvaluator); PCA 2 chiều để vẽ.

Đầu ra: data/processed/spark/ml_*.csv
Chạy (từ thư mục gốc repo): <python của venv> spark/mllib_tinh.py
"""
import time

import numpy as np
import pandas as pd
from pyspark.ml import Pipeline
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.feature import PCA, StandardScaler, VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql import functions as F

from _session import get_spark
from common import PROCESSED

OUT = PROCESSED / "spark"
K_FOLD, LAP, SEED = 5, 5, 2026

TARGETS = {"toan_tb": "Điểm Toán TB", "van_tb": "Điểm Văn TB", "diem_tb_chung": "Điểm TB chung"}

# Biến log: thu nhập/GRDP lệch phải mạnh (TP.HCM, Hà Nội, Quảng Ninh)
NHAN = {
    "log_thu_nhap": "log(thu nhập BQ/người/tháng)",
    "log_grdp": "log(GRDP/người 2025)",
    "hdi": "HDI",
    "ty_le_do_thi_pct": "Tỷ lệ đô thị (%)",
    "ty_le_ld_qua_dao_tao": "Tỷ lệ LĐ qua đào tạo (%)",
    "hs_tren_gv_thpt": "Học sinh/giáo viên THPT",
    "ty_le_ho_ngheo": "Tỷ lệ hộ nghèo (%)",
    "ty_le_dung_internet": "Tỷ lệ dùng internet (%)",
}
# Các đặc tả so sánh. Biến KT-XH tương quan rất mạnh với nhau (thu nhập–HDI r=0,90,
# thu nhập–internet 0,88) nên mô hình đa biến chỉ giữ các biến ít trùng thông tin.
DA_BIEN = ["log_thu_nhap", "ty_le_do_thi_pct", "ty_le_ld_qua_dao_tao", "hs_tren_gv_thpt"]
MODELS = [
    ("M1_thu_nhap", ["log_thu_nhap"], 0.0),
    ("M2_hdi", ["hdi"], 0.0),
    ("M3_grdp", ["log_grdp"], 0.0),
    ("M4_da_bien_ols", DA_BIEN, 0.0),
    ("M5_da_bien_ridge", DA_BIEN, 0.5),   # L2 trên biến đã chuẩn hóa
]

CLUSTER_VARS = ["log_thu_nhap", "hdi", "ty_le_do_thi_pct", "ty_le_ld_qua_dao_tao",
                "ty_le_ho_ngheo", "ty_le_dung_internet", "toan_tb", "van_tb", "ty_le_thi_ngoai_ngu"]


def pipeline(features, target, reg):
    return Pipeline(stages=[
        VectorAssembler(inputCols=features, outputCol="x_raw"),
        StandardScaler(inputCol="x_raw", outputCol="x", withMean=True, withStd=True),
        LinearRegression(featuresCol="x", labelCol=target, regParam=reg, elasticNetParam=0.0,
                         solver="normal"),
    ])


def load(spark):
    df = (spark.read.csv((OUT / "diemthi_x_ktxh_34tinh.csv").as_posix(), header=True, inferSchema=True)
          .withColumn("ma_tinh", F.lpad(F.col("ma_tinh").cast("string"), 2, "0"))
          .withColumn("log_thu_nhap", F.log("thu_nhap_bq_nguoi_thang"))
          .withColumn("log_grdp", F.log("grdp_nguoi_2025")))
    assert df.count() == 34
    return df


def gan_fold(spark, df, lap):
    """Chia 34 tỉnh vào K_FOLD fold gần đều nhau (7/7/7/7/6), khác nhau theo từng lần lặp."""
    ma = sorted(r.ma_tinh for r in df.select("ma_tinh").collect())
    rng = np.random.default_rng(SEED + lap)
    perm = rng.permutation(len(ma))
    folds = spark.createDataFrame([(ma[i], int(j % K_FOLD)) for j, i in enumerate(perm)], ["ma_tinh", "fold"])
    return df.join(folds, "ma_tinh").cache()


def kfold(spark, df):
    rows = []
    for lap in range(LAP):
        d = gan_fold(spark, df, lap)
        for target in TARGETS:
            preds = {name: [] for name, _, _ in MODELS}
            base = []
            for k in range(K_FOLD):
                train, test = d.where(F.col("fold") != k), d.where(F.col("fold") == k)
                mu = train.agg(F.avg(target)).first()[0]
                yt = [r[0] for r in test.select(target).collect()]
                base += [(y, mu) for y in yt]
                for name, feats, reg in MODELS:
                    m = pipeline(feats, target, reg).fit(train)
                    preds[name] += [(r[target], r.prediction) for r in
                                    m.transform(test).select(target, "prediction").collect()]
            sse_base = sum((y - p) ** 2 for y, p in base)
            for name, feats, reg in MODELS:
                sse = sum((y - p) ** 2 for y, p in preds[name])
                rows.append(dict(lap=lap, bien_phu_thuoc=target, mo_hinh=name,
                                 rmse_cv=(sse / len(preds[name])) ** 0.5,
                                 rmse_moc=(sse_base / len(base)) ** 0.5,
                                 r2_cv=1 - sse / sse_base))
        d.unpersist()
        print(f"  lặp {lap + 1}/{LAP} xong")
    raw = pd.DataFrame(rows)
    tom = (raw.groupby(["bien_phu_thuoc", "mo_hinh"])
              .agg(r2_cv_tb=("r2_cv", "mean"), r2_cv_sd=("r2_cv", "std"),
                   rmse_cv_tb=("rmse_cv", "mean"), rmse_moc_tb=("rmse_moc", "mean"))
              .reset_index())
    spec = {n: (", ".join(f), r) for n, f, r in MODELS}
    tom["bien_doc_lap"] = tom["mo_hinh"].map(lambda n: spec[n][0])
    tom["reg_param"] = tom["mo_hinh"].map(lambda n: spec[n][1])
    return raw, tom


def he_so_full(df):
    """OLS trên toàn bộ 34 tỉnh: hệ số trên biến chuẩn hóa (so sánh được độ lớn), p-value."""
    rows = []
    for target in TARGETS:
        for name, feats, reg in MODELS:
            if reg:
                continue
            m = pipeline(feats, target, 0.0).fit(df)
            lr = m.stages[-1]
            s = lr.summary
            pv = s.pValues  # phần tử cuối là intercept
            for i, f in enumerate(feats):
                rows.append(dict(bien_phu_thuoc=target, mo_hinh=name, bien=f, nhan=NHAN[f],
                                 he_so_chuan_hoa=lr.coefficients[i], p_value=pv[i],
                                 r2_trong_mau=s.r2, r2_hieu_chinh=s.r2adj))
    return pd.DataFrame(rows)


def vif(df, feats):
    X = df.select(*feats).toPandas().to_numpy(dtype=float)
    out = []
    for j, f in enumerate(feats):
        y, A = X[:, j], np.column_stack([np.ones(len(X)), np.delete(X, j, axis=1)])
        resid = y - A @ np.linalg.lstsq(A, y, rcond=None)[0]
        r2 = 1 - resid.var() / y.var()
        out.append(dict(bien=f, nhan=NHAN[f], vif=1 / (1 - r2)))
    return pd.DataFrame(out)


def phan_cum(df):
    prep = Pipeline(stages=[
        VectorAssembler(inputCols=CLUSTER_VARS, outputCol="x_raw"),
        StandardScaler(inputCol="x_raw", outputCol="x", withMean=True, withStd=True),
        PCA(k=2, inputCol="x", outputCol="pc"),
    ]).fit(df)
    d = prep.transform(df).cache()
    ev = ClusteringEvaluator(featuresCol="x", predictionCol="cum", metricName="silhouette")
    sil, models = [], {}
    for k in range(2, 7):
        m = KMeans(featuresCol="x", predictionCol="cum", k=k, seed=SEED, maxIter=100).fit(d)
        p = m.transform(d)
        sizes = sorted((r["count"] for r in p.groupBy("cum").count().collect()), reverse=True)
        sil.append(dict(k=k, silhouette=ev.evaluate(p), wssse=m.summary.trainingCost,
                        kich_thuoc_cum=str(sizes)))
        models[k] = p
    sil = pd.DataFrame(sil)
    k_best = int(sil.loc[sil["silhouette"].idxmax(), "k"])
    pca_model = prep.stages[-1]
    tai = pd.DataFrame(pca_model.pc.toArray(), index=CLUSTER_VARS, columns=["pc1", "pc2"])
    tai.loc["__ty_le_phuong_sai__"] = pca_model.explainedVariance.toArray()
    # Lưu cả k tốt nhất theo silhouette và k = 3 (silhouette gần bằng, dễ diễn giải hơn)
    ket_qua = {k: _ho_so(models[k]) for k in sorted({k_best, 3})}
    return sil, k_best, ket_qua, tai.reset_index(names="bien")


def _ho_so(p):
    gan = (p.select("ma_tinh", "ten_tinh", "cum", F.col("pc"), *CLUSTER_VARS).toPandas())
    gan[["pc1", "pc2"]] = pd.DataFrame(gan.pop("pc").map(lambda v: v.toArray()).tolist(), index=gan.index)
    hoso = gan.groupby("cum")[CLUSTER_VARS].mean().assign(so_tinh=gan.groupby("cum").size())
    hoso["thu_nhap_bq_nguoi_thang"] = np.exp(hoso.pop("log_thu_nhap")).round(0)
    hoso["cac_tinh"] = gan.groupby("cum")["ten_tinh"].apply(lambda s: ", ".join(sorted(s)))
    return gan, hoso.reset_index()


def main(chi_phan_cum=False):
    t0 = time.perf_counter()
    spark = get_spark("mllib_tinh")
    df = load(spark).cache()
    if not chi_phan_cum:
        hoi_quy(spark, df)
    phan_cum_va_luu(df)
    print(f"\n[tong] {time.perf_counter() - t0:.0f}s")
    spark.stop()


def hoi_quy(spark, df):
    print(f"[hoi quy] repeated {K_FOLD}-fold x {LAP} lần, {len(MODELS)} mô hình x {len(TARGETS)} biến phụ thuộc")
    raw, tom = kfold(spark, df)
    raw.to_csv(OUT / "ml_hoi_quy_kfold_chi_tiet.csv", index=False)
    tom.to_csv(OUT / "ml_hoi_quy_kfold.csv", index=False)
    print(tom.round(3).to_string(index=False))

    hs = he_so_full(df)
    hs.to_csv(OUT / "ml_hoi_quy_he_so.csv", index=False)
    print("\n[hệ số OLS toàn bộ 34 tỉnh, biến chuẩn hóa]")
    print(hs[hs.mo_hinh == "M4_da_bien_ols"].round(3).to_string(index=False))

    v = vif(df, DA_BIEN)
    v.to_csv(OUT / "ml_vif.csv", index=False)
    print("\n[VIF mô hình đa biến]\n" + v.round(2).to_string(index=False))


def phan_cum_va_luu(df):
    sil, k_best, ket_qua, tai = phan_cum(df)
    sil.to_csv(OUT / "ml_kmeans_silhouette.csv", index=False)
    tai.to_csv(OUT / "ml_pca_tai.csv", index=False)
    print("\n[KMeans]\n" + sil.round(3).to_string(index=False) + f"\n-> silhouette cao nhất: k = {k_best}")
    for k, (gan, hoso) in ket_qua.items():
        gan.to_csv(OUT / f"ml_kmeans_k{k}_cum_tinh.csv", index=False)
        hoso.to_csv(OUT / f"ml_kmeans_k{k}_ho_so_cum.csv", index=False)
        print(f"\n[k = {k}]\n" + hoso.drop(columns="cac_tinh").round(2).to_string(index=False))
        for _, r in hoso.iterrows():
            print(f"  cụm {r.cum}: {r.cac_tinh}")


if __name__ == "__main__":
    import sys
    main(chi_phan_cum="--chi-phan-cum" in sys.argv)
