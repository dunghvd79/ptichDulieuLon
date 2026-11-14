"""Hằng số và đường dẫn dùng chung cho các script."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
REF = ROOT / "data" / "reference"
PROCESSED = ROOT / "data" / "processed"

DIEMTHI_RAW = RAW / "diemthi_2026"            # 34 file CSV theo tỉnh
NIENGIAM_PDF = RAW / "NG-TOAN-QUOC-2025.pdf"  # Niên giám thống kê 2025
MAP_63_34 = REF / "map_63_34_tinh.csv"

# Môn thi theo cấu trúc 2025+ (GDCD đã đổi thành GD Kinh tế & Pháp luật)
SUBJECTS = [
    "toan", "ngu_van", "ngoai_ngu", "vat_li", "hoa_hoc", "sinh_hoc",
    "lich_su", "dia_li", "gdktpl", "tin_hoc", "cong_nghe",
]

# 34 tỉnh, thành theo đúng cách viết trong phụ lục Niên giám 2025
PROVINCES_34 = [
    "Hà Nội", "Bắc Ninh", "Quảng Ninh", "Hải Phòng", "Hưng Yên", "Ninh Bình",
    "Cao Bằng", "Tuyên Quang", "Lào Cai", "Thái Nguyên", "Lạng Sơn", "Phú Thọ",
    "Điện Biên", "Lai Châu", "Sơn La", "Thanh Hóa", "Nghệ An", "Hà Tĩnh",
    "Quảng Trị", "Huế", "Đà Nẵng", "Quảng Ngãi", "Gia Lai", "Khánh Hòa",
    "Đắk Lắk", "Lâm Đồng", "Tây Ninh", "Đồng Nai", "TP. Hồ Chí Minh",
    "Vĩnh Long", "Đồng Tháp", "An Giang", "Cần Thơ", "Cà Mau",
]
