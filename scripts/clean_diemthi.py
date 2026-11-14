"""Bước 1: làm sạch dữ liệu điểm thi THPT 2026.

Lỗi dữ liệu gốc cần xử lý:
  1. Ở 14 tỉnh (TP.HCM, Hải Phòng, Đồng Nai, Cần Thơ...), các cột điểm trống;
     toàn bộ điểm bị dồn vào cột `extra` dạng chuỗi mã hóa HTML, ví dụ
     "To&#xE1;n=8; V&#x103;n=7; S&#x1EED;=9".
  2. Môn GD Kinh tế & Pháp luật không có cột riêng, cũng nằm trong `extra`.
  3. Cột `gdcd` gần như rỗng (môn đã đổi tên từ 2025).
Ngoài ra: bỏ cột SBD (ẩn danh), giữ mã điểm thi (3 số sau mã tỉnh) để phân tích theo cụm.

Đầu ra:
  data/processed/diemthi_2026_clean.parquet   (hoặc .csv.gz nếu thiếu pyarrow)
  data/processed/diemthi_theo_tinh.csv        (tổng hợp theo 34 tỉnh)

Chạy:  python scripts/clean_diemthi.py
"""
import html
import pandas as pd
from common import DIEMTHI_RAW, PROCESSED, SUBJECTS

# Tên môn trong cột `extra` (sau khi giải mã HTML, viết thường) -> tên cột chuẩn
EXTRA_MAP = {
    "toán": "toan", "văn": "ngu_van", "ngữ văn": "ngu_van", "ngoại ngữ": "ngoai_ngu",
    "lí": "vat_li", "lý": "vat_li", "hóa": "hoa_hoc", "sinh": "sinh_hoc",
    "sử": "lich_su", "địa": "dia_li", "tin học": "tin_hoc", "tin": "tin_hoc",
    "công nghệ công nghiệp": "cong_nghe", "công nghệ nông nghiệp": "cong_nghe",
    "công nghệ": "cong_nghe", "giáo dục kinh tế pháp luật": "gdktpl",
}


def parse_extra(s):
    """'To&#xE1;n=8; V&#x103;n=7' -> {'toan': 8.0, 'ngu_van': 7.0}"""
    out = {}
    if not isinstance(s, str):
        return out
    for part in html.unescape(s).split(";"):
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        col = EXTRA_MAP.get(k.strip().lower())
        if col:
            try:
                out[col] = float(v)
            except ValueError:
                pass
    return out


def load_raw():
    files = sorted(DIEMTHI_RAW.glob("*.csv"))
    assert files, f"Không thấy CSV trong {DIEMTHI_RAW}. Chạy scripts/get_data.py trước."
    return pd.concat((pd.read_csv(f, dtype=str) for f in files), ignore_index=True)


def clean(df):
    df = df.rename(columns={"gdcd": "gdktpl"})
    extra = pd.DataFrame(df["extra"].map(parse_extra).tolist(), index=df.index)
    for c in SUBJECTS:
        df[c] = pd.to_numeric(df.get(c), errors="coerce")
        if c in extra:
            df[c] = df[c].fillna(extra[c])
    df["ma_tinh"] = df["sbd"].str[:2]
    df["ma_diem_thi"] = df["sbd"].str[2:5]   # cụm ~1000 SBD, thường ứng với 1 điểm thi
    df["so_mon"] = df[SUBJECTS].notna().sum(axis=1)
    df["diem_tb"] = df[SUBJECTS].mean(axis=1)
    keep = ["ma_tinh", "province_name", "ma_diem_thi", *SUBJECTS, "so_mon", "diem_tb"]
    return df[keep].rename(columns={"province_name": "ten_tinh"})  # bỏ SBD


def aggregate(df):
    g = df.groupby(["ma_tinh", "ten_tinh"])
    out = g.agg(
        so_thi_sinh=("toan", "size"),
        toan_tb=("toan", "mean"), van_tb=("ngu_van", "mean"), anh_tb=("ngoai_ngu", "mean"),
        diem_tb_chung=("diem_tb", "mean"),
        toan_trung_vi=("toan", "median"),
    )
    out["ty_le_thi_ngoai_ngu"] = g["ngoai_ngu"].apply(lambda x: x.notna().mean())
    out["ty_le_toan_duoi_5"] = g["toan"].apply(lambda x: (x < 5).sum() / x.notna().sum())
    out["ty_le_toan_tu_8"] = g["toan"].apply(lambda x: (x >= 8).sum() / x.notna().sum())
    for c in ["vat_li", "hoa_hoc", "sinh_hoc", "lich_su", "dia_li", "gdktpl", "tin_hoc", "cong_nghe"]:
        out[f"ty_le_chon_{c}"] = g[c].apply(lambda x: x.notna().mean())
    return out.round(4).reset_index()


if __name__ == "__main__":
    PROCESSED.mkdir(parents=True, exist_ok=True)
    raw = load_raw()
    print(f"[load] {len(raw):,} thí sinh, {raw['sbd'].str[:2].nunique()} tỉnh")
    print(f"[truoc] có điểm Toán: {pd.to_numeric(raw['toan'], errors='coerce').notna().mean():.1%}")
    df = clean(raw)
    print(f"[sau]   có điểm Toán: {df['toan'].notna().mean():.1%}")
    print("[so mon]", df["so_mon"].value_counts().sort_index().to_dict())
    try:
        df.to_parquet(PROCESSED / "diemthi_2026_clean.parquet", index=False)
        print("[save] diemthi_2026_clean.parquet")
    except ImportError:
        df.to_csv(PROCESSED / "diemthi_2026_clean.csv.gz", index=False)
        print("[save] diemthi_2026_clean.csv.gz (cài pyarrow để lưu parquet)")
    aggregate(df).to_csv(PROCESSED / "diemthi_theo_tinh.csv", index=False)
    print("[save] diemthi_theo_tinh.csv")
