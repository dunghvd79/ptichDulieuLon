# Điểm thi THPT 2026 và điều kiện kinh tế – xã hội theo tỉnh

Đồ án môn **Tích hợp và phân tích dữ liệu lớn**.

**Câu hỏi nghiên cứu:** Mức sống, thu nhập, đô thị hóa và điều kiện giáo dục của 34 tỉnh, thành phố (sau sắp xếp đơn vị hành chính 01/07/2025) liên quan thế nào đến kết quả thi tốt nghiệp THPT 2026? Môn nào chênh lệch giữa các tỉnh nhiều nhất?

## Nguồn dữ liệu

| Nguồn | Nội dung | Kích thước | Vị trí |
|---|---|---|---|
| [diem-thi-thptqg-2026](https://github.com/duongtrongnguyen123/diem-thi-thptqg-2026) (duongtrongnguyen123), thu thập từ trang tra cứu công khai của VietnamNet ngày 01/07/2026 | Điểm thi của 1.200.202 thí sinh, 34 file CSV theo tỉnh | ~115 MB | `data/raw/diemthi_2026/` |
| [Niên giám thống kê 2025](https://www.nso.gov.vn/default/2026/07/nien-giam-thong-ke-2025/), Cục Thống kê (Bộ Tài chính) | Phụ lục số liệu 34 tỉnh, trang 1142–1555, 209 biểu | PDF 1.557 trang | `data/raw/NG-TOAN-QUOC-2025.pdf` |
| Nghị quyết 202/2025/QH15 | Sắp xếp 63 tỉnh thành 34 tỉnh | – | `data/reference/map_63_34_tinh.csv` |

> Dữ liệu điểm thi là dữ liệu cá nhân: chỉ dùng cho học tập, nghiên cứu. Cột số báo danh (SBD) bị loại bỏ ngay ở bước làm sạch, kết quả chỉ báo cáo ở mức tổng hợp. `data/raw/` không đưa lên Git.

## Cấu trúc thư mục

```
data/
  raw/           dữ liệu gốc (không commit)
  reference/     bảng ánh xạ 63 -> 34 tỉnh
  processed/     dữ liệu đã làm sạch / tổng hợp / ghép
scripts/
  common.py          đường dẫn, danh sách môn, danh sách 34 tỉnh
  get_data.py        bước 0: tải dữ liệu thô
  clean_diemthi.py   bước 1: làm sạch điểm thi
  build_ktxh.py      bước 2: trích số liệu KT-XH từ PDF Niên giám
  join_explore.py    bước 3: ghép 2 nguồn, tương quan thăm dò
notebooks/       phân tích khám phá, biểu đồ
spark/           pipeline PySpark + MLlib
```

## Cách chạy

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt

cd scripts
python get_data.py        # bỏ qua nếu data/raw đã có dữ liệu
python clean_diemthi.py
python build_ktxh.py
python join_explore.py
```

## Các vấn đề tích hợp dữ liệu đã xử lý

1. **Điểm bị dồn vào cột `extra` (điểm thi).** Ở 14 tỉnh (TP.HCM, Hải Phòng, Đồng Nai, Cần Thơ…), các cột điểm trống. Toàn bộ điểm nằm trong cột `extra` dạng chuỗi mã hóa HTML (`To&#xE1;n=8; V&#x103;n=7`). Đọc thẳng thì chỉ **39,3%** thí sinh có điểm Toán; sau khi giải mã và tách lại là **98,6%**.
2. **Đổi môn thi.** GDCD đổi thành GD Kinh tế & Pháp luật, môn này cũng chỉ có trong `extra`. Thêm Tin học, Công nghệ (công nghiệp/nông nghiệp).
3. **Đổi địa giới và mã tỉnh.** 63 tỉnh thành 34 tỉnh. **7 mã số cũ nay trỏ sang tỉnh khác**: 15 (Yên Bái → Lào Cai), 24 (Bắc Giang → Bắc Ninh), 44 (Quảng Bình → Quảng Trị), 52 (Bình Định → Gia Lai), 80 (Long An → Tây Ninh), 82 (Tiền Giang → Đồng Tháp), 91 (Kiên Giang → An Giang). Ghép dữ liệu cũ theo mã số mà không qua bảng ánh xạ sẽ sai mà không có lỗi nào báo ra.
4. **Số liệu nằm trong PDF, không có Excel.**
   - Phải đổi số định dạng Việt Nam (`1.234,5`).
   - Ô trống làm lệch cột; xử lý bằng cách gán số vào cột theo vị trí ký tự, lấy các dòng đủ cột trên cùng trang làm mốc.
   - Mỗi biểu trải 2 trang với lề lệch nhau.
   - Kiểm chứng: tổng 34 tỉnh khớp chính xác dòng "Cả nước" ở dân số, số giáo viên và học sinh THPT.
5. **Gộp chỉ tiêu bình quân.** Khi phải tự gộp từ 63 sang 34 tỉnh, chỉ tiêu tổng (dân số, GRDP) thì cộng; chỉ tiêu bình quân (GRDP/người, thu nhập/người) phải tính lại theo trọng số dân số, không lấy trung bình cộng. Niên giám 2025 đã có sẵn phụ lục 34 tỉnh nên dự án dùng trực tiếp số liệu này.

## Dữ liệu đầu ra (`data/processed/`)

| File | Mô tả |
|---|---|
| `diemthi_2026_clean.parquet` | Điểm từng thí sinh đã làm sạch, không có SBD (không commit) |
| `diemthi_theo_tinh.csv` | Điểm TB, trung vị, tỷ lệ dưới 5 / từ 8, tỷ lệ chọn từng môn theo tỉnh |
| `ktxh_34tinh_long.csv` | tỉnh – chỉ tiêu – năm – giá trị – đơn vị – số biểu Niên giám |
| `ktxh_34tinh_2025_wide.csv` | Mỗi tỉnh một dòng: năm 2025 + chuỗi GRDP/người 2020–2025 |
| `diemthi_x_ktxh_34tinh.csv` | Bảng đã ghép 2 nguồn |
| `tuong_quan_spearman.csv` | Tương quan thăm dò |

**Chỉ tiêu KT-XH đã trích:**
- Dân số, dân số thành thị (tính ra tỷ lệ đô thị hóa), diện tích, mật độ dân số.
- GRDP/người 2020–2025, thu nhập bình quân đầu người/tháng, thu nhập bình quân một lao động.
- HDI, GINI, tỷ lệ hộ nghèo, tỷ lệ lao động qua đào tạo, tỷ lệ dùng internet.
- Số trường, giáo viên, học sinh THPT; số học sinh/giáo viên.

Muốn lấy thêm biểu khác, xem nhanh bằng: `python build_ktxh.py --bieu 52 60`.

## Kết quả thăm dò ban đầu (Spearman, n = 34 tỉnh)

| | Toán TB | Văn TB | Tỷ lệ thi Ngoại ngữ |
|---|---|---|---|
| HDI | 0,79 | 0,36 | 0,86 |
| Thu nhập bình quân đầu người | 0,76 | 0,35 | 0,85 |
| Tỷ lệ hộ nghèo | −0,77 | −0,31 | −0,79 |
| GRDP bình quân đầu người | 0,60 | 0,21 | 0,78 |
| Học sinh / giáo viên THPT | 0,15 | 0,24 | 0,17 |

Điểm Toán và tỷ lệ chọn Ngoại ngữ đi theo mức sống rõ rệt, còn Văn thì yếu. Thu nhập và HDI giải thích tốt hơn GRDP. Đây mới là kết quả thăm dò; n = 34 nhỏ, cần kiểm định và mô hình hóa ở các bước sau.

## Việc tiếp theo

- [ ] Chuyển bước làm sạch và ghép sang PySpark (`spark/`)
- [ ] Hồi quy điểm TB theo các biến KT-XH (Spark MLlib)
- [ ] Phân cụm tỉnh (KMeans) theo hồ sơ KT-XH + điểm thi
- [ ] Dashboard / trực quan hóa
