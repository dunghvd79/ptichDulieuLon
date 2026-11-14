"""Bước 0: tải dữ liệu thô (chỉ cần chạy nếu data/raw đang trống).

- Điểm thi THPT 2026: clone repo gốc của duongtrongnguyen123, chép 34 file CSV
  vào data/raw/diemthi_2026/.
- Niên giám thống kê 2025: tải PDF từ nso.gov.vn (một số mạng chặn; nếu lỗi,
  tải tay rồi đặt vào data/raw/NG-TOAN-QUOC-2025.pdf).

Chạy:  python scripts/get_data.py
"""
import shutil, subprocess, tempfile, urllib.request
from common import DIEMTHI_RAW, NIENGIAM_PDF

REPO = "https://github.com/duongtrongnguyen123/diem-thi-thptqg-2026"
PDF_URL = "https://www.nso.gov.vn/wp-content/uploads/2026/07/NG-TOAN-QUOC-2025-1.pdf"


def get_diemthi():
    if DIEMTHI_RAW.exists() and len(list(DIEMTHI_RAW.glob("*.csv"))) == 34:
        print("[diemthi] đã có 34 file, bỏ qua")
        return
    DIEMTHI_RAW.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["git", "clone", "--depth", "1", REPO, tmp], check=True)
        for f in sorted((__import__("pathlib").Path(tmp) / "data").glob("[0-9][0-9]-*.csv")):
            shutil.copy2(f, DIEMTHI_RAW / f.name)
    print(f"[diemthi] đã chép {len(list(DIEMTHI_RAW.glob('*.csv')))} file vào {DIEMTHI_RAW}")


def get_niengiam():
    if NIENGIAM_PDF.exists():
        print("[niengiam] đã có PDF, bỏ qua")
        return
    try:
        urllib.request.urlretrieve(PDF_URL, NIENGIAM_PDF)
        print(f"[niengiam] đã tải {NIENGIAM_PDF}")
    except Exception as e:
        print(f"[niengiam] không tải được ({e}). Hãy tải tay từ:\n  {PDF_URL}\n"
              f"rồi lưu thành {NIENGIAM_PDF}")


if __name__ == "__main__":
    get_diemthi()
    get_niengiam()
