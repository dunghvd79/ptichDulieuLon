"""Kiểm chứng chéo: kết quả Spark (data/processed/spark/) phải khớp bản pandas (data/processed/).

Hai pipeline viết độc lập (chỉ dùng chung bảng ánh xạ tên môn), nên khớp nhau là bằng chứng
logic làm sạch/tổng hợp đúng. Đầu ra: data/processed/spark/doi_chieu_pandas.csv
Chạy: python spark/doi_chieu_pandas.py   (không cần Spark)
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import PROCESSED  # noqa: E402

TOL = 1e-3  # bản pandas làm tròn 4 chữ số


def so_sanh(ten, khoa="ma_tinh"):
    a = pd.read_csv(PROCESSED / ten, dtype={khoa: str}).set_index(khoa).sort_index()
    b = pd.read_csv(PROCESSED / "spark" / ten, dtype={khoa: str}).set_index(khoa).sort_index()
    assert list(a.index) == list(b.index), f"{ten}: tập tỉnh khác nhau"
    rows = []
    for c in a.columns.intersection(b.columns):
        if pd.api.types.is_numeric_dtype(a[c]):
            d = (a[c] - b[c]).abs().max()
            rows.append((ten, c, d, d <= TOL))
        else:
            rows.append((ten, c, int((a[c] != b[c]).sum()), bool((a[c] == b[c]).all())))
    thieu = sorted(set(a.columns) ^ set(b.columns))
    return rows, thieu


if __name__ == "__main__":
    out = []
    for f in ["diemthi_theo_tinh.csv", "diemthi_x_ktxh_34tinh.csv"]:
        rows, thieu = so_sanh(f)
        out += rows
        if thieu:
            print(f"[{f}] cột chỉ có ở một bên: {thieu}")
    df = pd.DataFrame(out, columns=["file", "cot", "chenh_lech_max", "khop"])
    df.to_csv(PROCESSED / "spark" / "doi_chieu_pandas.csv", index=False)
    print(df.to_string(index=False))
    sai = df[~df["khop"]]
    print(f"\n{len(df) - len(sai)}/{len(df)} cột khớp (sai số <= {TOL})")
    sys.exit(1 if len(sai) else 0)
