"""Bước 3: ghép điểm thi (theo tỉnh) với số liệu kinh tế – xã hội, tính tương quan thăm dò.

Đầu ra:
  data/processed/diemthi_x_ktxh_34tinh.csv
  data/processed/tuong_quan_spearman.csv

Chạy:  python scripts/join_explore.py
"""
import pandas as pd
from common import PROCESSED

diem = pd.read_csv(PROCESSED / "diemthi_theo_tinh.csv", dtype={"ma_tinh": str})
ktxh = pd.read_csv(PROCESSED / "ktxh_34tinh_2025_wide.csv", dtype={"ma_tinh": str})
J = ktxh.merge(diem.drop(columns="ten_tinh"), on="ma_tinh", how="inner", validate="1:1")
assert len(J) == 34, f"Chỉ ghép được {len(J)}/34 tỉnh"
J.to_csv(PROCESSED / "diemthi_x_ktxh_34tinh.csv", index=False)

X = ["grdp_nguoi_2025", "thu_nhap_bq_nguoi_thang", "hdi", "ty_le_do_thi_pct",
     "ty_le_ld_qua_dao_tao", "ty_le_ho_ngheo", "hs_tren_gv_thpt", "ty_le_dung_internet"]
Y = ["toan_tb", "van_tb", "anh_tb", "diem_tb_chung", "ty_le_thi_ngoai_ngu", "ty_le_toan_duoi_5"]
C = J[X + Y].corr(method="spearman").loc[X, Y].round(2)
C.to_csv(PROCESSED / "tuong_quan_spearman.csv")
print(f"[join] {len(J)} tỉnh\n\nTương quan Spearman (n=34):\n{C.to_string()}")
