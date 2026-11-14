"""Pipeline PySpark: điểm thi THPT 2026 (1,2 triệu thí sinh) + số liệu KT-XH 34 tỉnh.

Kiến trúc 3 tầng (medallion):
  Bronze  đọc nguyên trạng 34 CSV (mọi cột là chuỗi, có cột nguồn file).
  Silver  chuẩn hóa từng thí sinh: giải mã + tách cột `extra` (pandas UDF / Arrow),
          ép kiểu an toàn (try_cast), đổi gdcd -> gdktpl, tách mã tỉnh/mã điểm thi, BỎ SBD.
  Gold    bảng tổng hợp: theo tỉnh, theo tỉnh x môn, độ chênh lệch giữa các tỉnh theo môn,
          tổ hợp môn tự chọn, báo cáo chất lượng dữ liệu, và bảng ghép với KT-XH.

Đầu ra (chỉ số liệu tổng hợp, không có dữ liệu cấp thí sinh): data/processed/spark/
Chạy (từ thư mục gốc repo):  <python của venv> spark/etl_diemthi.py
"""
import time

import pandas as pd
from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.sql.window import Window

from _session import get_spark
from common import DIEMTHI_RAW, PROCESSED, SUBJECTS
from clean_diemthi import parse_extra  # dùng chung bảng ánh xạ tên môn với bản pandas

OUT = PROCESSED / "spark"
BAT_BUOC = ["toan", "ngu_van"]
TU_CHON = [c for c in SUBJECTS if c not in BAT_BUOC]
TEN_MON = {
    "toan": "Toán", "ngu_van": "Ngữ văn", "ngoai_ngu": "Ngoại ngữ", "vat_li": "Vật lí",
    "hoa_hoc": "Hóa học", "sinh_hoc": "Sinh học", "lich_su": "Lịch sử", "dia_li": "Địa lí",
    "gdktpl": "GD KT&PL", "tin_hoc": "Tin học", "cong_nghe": "Công nghệ",
}
RAW_COLS = ["sbd", "province_code", "province_name", "toan", "ngu_van", "ngoai_ngu", "vat_li",
            "hoa_hoc", "sinh_hoc", "lich_su", "dia_li", "gdcd", "tin_hoc", "cong_nghe", "extra"]

EXTRA_SCHEMA = T.StructType([T.StructField(c, T.DoubleType()) for c in SUBJECTS])


@F.pandas_udf(EXTRA_SCHEMA)
def parse_extra_udf(s: pd.Series) -> pd.DataFrame:
    """Vector hóa: mỗi batch Arrow (~10k dòng) được giải mã HTML và tách thành 11 cột điểm."""
    return pd.DataFrame(s.map(parse_extra).tolist(), index=s.index).reindex(columns=SUBJECTS)


def save(df, name):
    pdf = df.toPandas() if hasattr(df, "toPandas") else df
    pdf.to_csv(OUT / f"{name}.csv", index=False)
    print(f"  [save] spark/{name}.csv  ({len(pdf)} dòng)")
    return pdf


class Timer:
    def __init__(self):
        self.t0, self.log = time.perf_counter(), []

    def lap(self, name):
        t = time.perf_counter()
        self.log.append((name, round(t - self.t0, 2)))
        print(f"[{name}] {t - self.t0:.1f}s")
        self.t0 = t


# ----------------------------------------------------------------------------- Bronze
def bronze(spark):
    schema = T.StructType([T.StructField(c, T.StringType()) for c in RAW_COLS])
    # Truyền danh sách file thay vì glob "*.csv": glob của Hadoop trên Windows gọi NativeIO
    # (cần winutils.exe) và treo im lặng nếu thiếu.
    files = [p.as_posix() for p in sorted(DIEMTHI_RAW.glob("*.csv"))]
    assert len(files) == 34, f"Cần 34 CSV, thấy {len(files)}. Chạy scripts/get_data.py trước."
    return (spark.read.csv(files, header=True, schema=schema, encoding="UTF-8")
            .withColumn("nguon_file", F.element_at(F.split(F.input_file_name(), "/"), -1)))


# ----------------------------------------------------------------------------- Silver
def silver(raw):
    ex = parse_extra_udf(F.col("extra"))
    df = raw.withColumnRenamed("gdcd", "gdktpl").withColumn("_ex", ex)
    for c in SUBJECTS:
        # try_cast: chuỗi không phải số -> null thay vì lỗi (Spark 4 bật ANSI mặc định)
        df = df.withColumn(c, F.coalesce(F.expr(f"try_cast({c} as double)"), F.col(f"_ex.{c}")))
    diem = F.filter(F.array(*SUBJECTS), lambda x: x.isNotNull())
    return df.select(
        F.substring("sbd", 1, 2).alias("ma_tinh"),
        F.col("province_name").alias("ten_tinh"),
        F.substring("sbd", 3, 3).alias("ma_diem_thi"),   # cụm ~1000 SBD, thường là 1 điểm thi
        *SUBJECTS,
        F.size(diem).alias("so_mon"),
        F.when(F.size(diem) > 0,
               F.aggregate(diem, F.lit(0.0), lambda a, x: a + x) / F.size(diem)).alias("diem_tb"),
        F.array_join(F.filter(
            F.array(*[F.when(F.col(c).isNotNull(), F.lit(TEN_MON[c])) for c in TU_CHON]),
            lambda x: x.isNotNull()), " + ").alias("to_hop_tu_chon"),
    )  # SBD bị bỏ ở đây: mọi bảng phía sau không còn định danh thí sinh


# ----------------------------------------------------------------------------- Gold
def chat_luong(raw, df):
    """Bảng chất lượng dữ liệu trước/sau làm sạch (dùng cho báo cáo)."""
    r = raw.agg(
        F.count("*").alias("so_dong"),
        F.countDistinct("sbd").alias("so_sbd_khac_nhau"),
        F.countDistinct(F.substring("sbd", 1, 2)).alias("so_ma_tinh"),
        F.avg(F.expr("try_cast(toan as double)").isNotNull().cast("int")).alias("co_toan_truoc"),
        F.avg(F.col("extra").isNotNull().cast("int")).alias("ty_le_dong_co_extra"),
        F.countDistinct(F.when(F.col("extra").isNotNull(), F.col("province_code"))).alias("so_tinh_dung_extra"),
        F.sum((F.col("province_code") != F.substring("sbd", 1, 2)).cast("int")).alias("lech_ma_tinh_vs_sbd"),
    ).first().asDict()
    s = df.agg(
        F.avg(F.col("toan").isNotNull().cast("int")).alias("co_toan_sau"),
        F.avg((F.col("so_mon") == 4).cast("int")).alias("ty_le_du_4_mon"),
        F.sum((F.col("so_mon") == 0).cast("int")).alias("khong_co_diem_nao"),
        # coalesce: môn không thi (null) phải tính là 0, nếu không cả tổng thành null
        F.sum(sum(F.coalesce(((F.col(c) < 0) | (F.col(c) > 10)).cast("int"), F.lit(0))
                  for c in SUBJECTS)).alias("diem_ngoai_0_10"),
    ).first().asDict()
    so_mon = {f"so_mon_{r_['so_mon']}": r_["count"] for r_ in df.groupBy("so_mon").count().collect()}
    return pd.DataFrame([{**r, **s, **dict(sorted(so_mon.items()))}]).T.reset_index() \
             .set_axis(["chi_so", "gia_tri"], axis=1)


def co_diem_theo_mon(raw, df):
    """Tỷ lệ thí sinh có điểm từng môn: đọc thẳng cột (trước) và sau khi tách `extra`."""
    truoc = raw.withColumnRenamed("gdcd", "gdktpl").agg(
        *[F.avg(F.expr(f"try_cast({c} as double)").isNotNull().cast("int")).alias(c) for c in SUBJECTS]
    ).first().asDict()
    sau = df.agg(*[F.avg(F.col(c).isNotNull().cast("int")).alias(c) for c in SUBJECTS]).first().asDict()
    return pd.DataFrame([dict(mon=c, ten_mon=TEN_MON[c], ty_le_truoc=truoc[c], ty_le_sau=sau[c])
                         for c in SUBJECTS])


def pho_diem(df):
    """Phổ điểm: số bài theo (tỉnh, môn, mức điểm). Điểm là bội của 0,05 -> làm tròn 2 chữ số."""
    return (df.unpivot(["ma_tinh"], SUBJECTS, "mon", "diem").where(F.col("diem").isNotNull())
              .withColumn("diem", F.round("diem", 2))
              .groupBy("ma_tinh", "mon", "diem").count().withColumnRenamed("count", "so_bai")
              .orderBy("ma_tinh", "mon", "diem"))


def theo_tinh(df):
    """Cùng định nghĩa cột với scripts/clean_diemthi.py::aggregate để đối chiếu."""
    co = lambda c: F.col(c).isNotNull().cast("int")
    return (df.groupBy("ma_tinh", "ten_tinh").agg(
        F.count("*").alias("so_thi_sinh"),
        F.avg("toan").alias("toan_tb"), F.avg("ngu_van").alias("van_tb"),
        F.avg("ngoai_ngu").alias("anh_tb"), F.avg("diem_tb").alias("diem_tb_chung"),
        F.median("toan").alias("toan_trung_vi"),
        F.avg(co("ngoai_ngu")).alias("ty_le_thi_ngoai_ngu"),
        (F.sum((F.col("toan") < 5).cast("int")) / F.count("toan")).alias("ty_le_toan_duoi_5"),
        (F.sum((F.col("toan") >= 8).cast("int")) / F.count("toan")).alias("ty_le_toan_tu_8"),
        *[F.avg(co(c)).alias(f"ty_le_chon_{c}") for c in TU_CHON if c != "ngoai_ngu"],
    ).orderBy("ma_tinh"))


def tinh_x_mon(df):
    """Bảng dài: mỗi dòng là 1 tỉnh x 1 môn, mô tả cả phân phối chứ không chỉ điểm TB."""
    n_tinh = df.groupBy("ma_tinh").agg(F.count("*").alias("_n_tinh"))
    long = df.unpivot(["ma_tinh", "ten_tinh"], SUBJECTS, "mon", "diem").where(F.col("diem").isNotNull())
    return (long.groupBy("ma_tinh", "ten_tinh", "mon").agg(
        F.count("*").alias("so_bai"),
        F.avg("diem").alias("tb"), F.median("diem").alias("trung_vi"),
        F.stddev("diem").alias("do_lech_chuan"),
        F.percentile("diem", 0.25).alias("p25"), F.percentile("diem", 0.75).alias("p75"),
        F.avg((F.col("diem") < 5).cast("int")).alias("ty_le_duoi_5"),
        F.avg((F.col("diem") >= 8).cast("int")).alias("ty_le_tu_8"),
        F.avg((F.col("diem") <= 1).cast("int")).alias("ty_le_liet"),
    ).join(n_tinh, "ma_tinh")
     .withColumn("ty_le_chon", F.col("so_bai") / F.col("_n_tinh")).drop("_n_tinh")
     .orderBy("ma_tinh", "mon")), long


def chenh_lech_mon(long, tm):
    """Môn nào chênh lệch giữa các tỉnh nhiều nhất?

    - do_lech_chuan_giua_tinh / khoang_cach: trên 34 điểm TB tỉnh (mỗi tỉnh 1 phiếu).
    - eta2 = SS_giữa_tỉnh / SS_toàn_bộ (cấp thí sinh): tỷ lệ phương sai điểm do khác biệt
      giữa các tỉnh. Không phụ thuộc thang điểm của từng môn nên so được giữa các môn.
    """
    toan_quoc = long.groupBy("mon").agg(
        F.count("*").alias("so_bai"), F.avg("diem").alias("tb_toan_quoc"),
        (F.variance("diem") * (F.count("*") - 1)).alias("ss_total"))
    ss_between = (tm.join(toan_quoc.select("mon", "tb_toan_quoc"), "mon")
                    .groupBy("mon").agg(
                        F.sum(F.col("so_bai") * (F.col("tb") - F.col("tb_toan_quoc")) ** 2).alias("ss_between"),
                        F.stddev("tb").alias("do_lech_chuan_giua_tinh"),
                        F.min("tb").alias("tb_tinh_thap_nhat"), F.max("tb").alias("tb_tinh_cao_nhat"),
                        F.min_by("ten_tinh", "tb").alias("tinh_thap_nhat"),
                        F.max_by("ten_tinh", "tb").alias("tinh_cao_nhat"),
                        F.stddev("ty_le_duoi_5").alias("do_lech_chuan_ty_le_duoi_5")))
    return (toan_quoc.join(ss_between, "mon")
            .withColumn("khoang_cach", F.col("tb_tinh_cao_nhat") - F.col("tb_tinh_thap_nhat"))
            .withColumn("he_so_bien_thien", F.col("do_lech_chuan_giua_tinh") / F.col("tb_toan_quoc"))
            .withColumn("eta2", F.col("ss_between") / F.col("ss_total"))
            .withColumn("ten_mon", F.udf(TEN_MON.get)("mon"))  # nhỏ (11 dòng), UDF thường là đủ
            .drop("ss_between", "ss_total")
            .orderBy(F.desc("eta2")))


def to_hop(df):
    """Tỷ lệ chọn từng tổ hợp 2 môn tự chọn (chỉ thí sinh thi đủ 4 môn)."""
    d = df.where(F.col("so_mon") == 4)
    tq = (d.groupBy("to_hop_tu_chon").count()
            .withColumn("ty_le", F.col("count") / F.sum("count").over(Window.partitionBy()))
            .orderBy(F.desc("count")))
    w = Window.partitionBy("ma_tinh")
    theo_t = (d.groupBy("ma_tinh", "ten_tinh", "to_hop_tu_chon").count()
                .withColumn("ty_le", F.col("count") / F.sum("count").over(w))
                .orderBy("ma_tinh", F.desc("count")))
    return tq, theo_t


def ghep_ktxh(spark, tt):
    ktxh = spark.read.csv((PROCESSED / "ktxh_34tinh_2025_wide.csv").as_posix(), header=True, inferSchema=True) \
                .withColumn("ma_tinh", F.lpad(F.col("ma_tinh").cast("string"), 2, "0"))
    j = ktxh.join(tt.drop("ten_tinh"), "ma_tinh", "inner").orderBy("ma_tinh")
    n = j.count()
    assert n == 34, f"Chỉ ghép được {n}/34 tỉnh"
    # tỉnh nào lệch tên giữa 2 nguồn (để báo cáo vấn đề tích hợp)
    lech = (ktxh.select("ma_tinh", F.col("ten_tinh").alias("ten_ng"))
                .join(tt.select("ma_tinh", "ten_tinh"), "ma_tinh")
                .where(F.col("ten_ng") != F.col("ten_tinh")).collect())
    for r in lech:
        print(f"  [tên lệch] {r.ma_tinh}: Niên giám '{r.ten_ng}' vs điểm thi '{r.ten_tinh}'")
    return j


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tm_ = Timer()
    spark = get_spark("etl_diemthi")
    tm_.lap("khoi_dong_spark")

    raw = bronze(spark).cache()
    print(f"  bronze: {raw.count():,} dòng, {raw.rdd.getNumPartitions()} partition")
    tm_.lap("bronze_doc_csv")

    df = silver(raw).cache()
    df.count()
    tm_.lap("silver_lam_sach")

    save(chat_luong(raw, df), "chat_luong_du_lieu")
    save(co_diem_theo_mon(raw, df), "co_diem_theo_mon")
    save(pho_diem(df), "pho_diem")
    tt = theo_tinh(df)
    save(tt, "diemthi_theo_tinh")
    tm, long = tinh_x_mon(df)
    save(tm, "diemthi_tinh_x_mon")
    save(chenh_lech_mon(long, tm), "chenh_lech_giua_tinh_theo_mon")
    tq, theo_t = to_hop(df)
    save(tq, "to_hop_toan_quoc")
    save(theo_t, "to_hop_theo_tinh")
    tm_.lap("gold_tong_hop")

    save(ghep_ktxh(spark, tt), "diemthi_x_ktxh_34tinh")
    tm_.lap("ghep_ktxh")

    save(pd.DataFrame(tm_.log, columns=["buoc", "giay"]), "thoi_gian_chay")
    spark.stop()


if __name__ == "__main__":
    main()
