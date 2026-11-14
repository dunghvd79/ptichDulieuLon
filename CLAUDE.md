# CLAUDE.md — Bài tập lớn "Tích hợp và phân tích dữ liệu lớn"

Hướng dẫn và bối cảnh cho Claude (Claude Code / IDE agent) khi làm việc trong repo này.
**Luôn trả lời người dùng bằng tiếng Việt.**

## 1. Bối cảnh

- **Bài tập lớn** (KHÔNG gọi là đồ án) môn **Tích hợp và phân tích dữ liệu lớn** (Kỳ 1 – Năm 4), Trường Công nghệ Thông tin, ĐH Phenikaa.
- Repo GitHub: `https://github.com/dunghvd79/ptichDulieuLon`, để **public** (người dùng đồng ý 2026-11-14). Chỉ chứa code, hình và số liệu tổng hợp theo tỉnh, không bao giờ đẩy dữ liệu cấp thí sinh.
- Thư mục local (Windows): `E:\2026 Year\Ki_1_Nam_4\cuoiki_PtichDulieuLon`.
- **Đề tài:** Điểm thi tốt nghiệp THPT 2026 và điều kiện kinh tế – xã hội theo tỉnh.
- **Câu hỏi nghiên cứu:**
  - Tỉnh giàu hơn, đô thị hóa cao hơn, điều kiện giáo dục tốt hơn có điểm thi cao hơn không?
  - Môn nào chênh lệch giữa các tỉnh nhiều nhất?
- **Đơn vị phân tích:** 34 tỉnh, thành phố sau sắp xếp hành chính (hiệu lực 01/07/2025, Nghị quyết 202/2025/QH15).
- Yêu cầu của môn: phải thể hiện được **tích hợp nhiều nguồn** và dùng **công cụ Big Data** (Spark, MLlib…). Một mình bộ điểm thi (1,2 triệu dòng) chưa đủ "lớn", nên điểm nhấn của bài tập lớn là phần tích hợp và pipeline.

## 2. Nguồn dữ liệu

| Nguồn | Ghi chú | Vị trí |
|---|---|---|
| Điểm thi THPT 2026 – repo `duongtrongnguyen123/diem-thi-thptqg-2026` | 1.200.202 thí sinh, 34 CSV theo tỉnh, ~115 MB. Cào từ VietnamNet ngày 01/07/2026. **Dữ liệu cá nhân.** | `data/raw/diemthi_2026/` |
| Niên giám thống kê 2025 – Cục Thống kê (nso.gov.vn) | PDF 1.557 trang, không có bản Excel. Phụ lục 34 tỉnh ở **trang 1142–1555 (209 biểu)**. | `data/raw/NG-TOAN-QUOC-2025.pdf` |
| Bảng ánh xạ 63 → 34 tỉnh | Tự dựng theo NQ 202/2025/QH15; đã đối chiếu, 34 mã mới khớp mã tỉnh trong SBD | `data/reference/map_63_34_tinh.csv` |

Repo `TruongThuHa/diem_thi_thptqg-2026-` (người dùng tìm thấy đầu tiên) **không chứa dữ liệu**, chỉ có script. Dữ liệu nằm ở repo gốc nói trên.

URL PDF Niên giám: `https://www.nso.gov.vn/wp-content/uploads/2026/07/NG-TOAN-QUOC-2025-1.pdf`

## 3. Cấu trúc repo

```
data/raw/          dữ liệu gốc — KHÔNG commit (.gitignore)
data/reference/    map_63_34_tinh.csv
data/processed/    đầu ra; diemthi_2026_clean.* KHÔNG commit (dữ liệu cấp thí sinh)
scripts/
  common.py          đường dẫn, SUBJECTS, PROVINCES_34 (tên đúng như trong Niên giám)
  get_data.py        bước 0: clone repo điểm thi + tải PDF (bỏ qua nếu đã có)
  clean_diemthi.py   bước 1: làm sạch điểm thi -> parquet + diemthi_theo_tinh.csv
  build_ktxh.py      bước 2: trích số liệu KT-XH từ PDF (pypdf, layout mode)
  join_explore.py    bước 3: ghép 2 nguồn + tương quan Spearman
notebooks/         (trống) phân tích khám phá, biểu đồ
spark/             pipeline PySpark (xem spark/README.md)
  _session.py        SparkSession local đã xử lý các lỗi Windows
  etl_diemthi.py     Bronze/Silver/Gold -> data/processed/spark/*.csv (~65 giây)
  doi_chieu_pandas.py  so Spark vs pandas (60/60 cột khớp)
  mllib_tinh.py      hồi quy repeated k-fold + KMeans/PCA -> spark/ml_*.csv (~4 phút; --chi-phan-cum ~20 giây)
bao_cao/DE_CUONG.md  đề cương báo cáo ~20 trang + trạng thái từng mục + số liệu đã ghi
bao_cao/ve_hinh.py   vẽ hình -> bao_cao/hinh/*.png (cần matplotlib trong venv)
bao_cao/bao_cao.md   NGUỒN NỘI DUNG báo cáo Word (chương 1–7, TLTK, phụ lục; cú pháp @bang/@hinh/@ref)
bao_cao/build_docx.js  bao_cao.md -> BaoCao_DiemThi2026_KTXH.docx (cd bao_cao && npm install && node build_docx.js)
bao_cao/cap_nhat_word.ps1  Word COM: cập nhật mục lục/danh mục, xuất PDF (chạy sau build_docx.js)
bao_cao/kich_ban_thuyet_trinh.md  lời nói mẫu khi thuyết trình
bao_cao/dat_van_de.md  bản nháp cũ (đã chuyển sang bao_cao.md, không sửa nữa)
```

Spark chạy bằng venv **ngoài repo**: `C:\Users\DELL\venvs\ptdl` (Python 3.11 + PySpark 4.0.1, `requirements-spark.txt`), chạy từ thư mục gốc repo.

Chạy (từ thư mục `scripts/`): `python get_data.py && python clean_diemthi.py && python build_ktxh.py && python join_explore.py`
Phụ thuộc: `pandas`, `pyarrow`, `pypdf` (xem `requirements.txt`). Xem nhanh một biểu bất kỳ: `python build_ktxh.py --bieu 52 60`.

## 4. Các vấn đề tích hợp đã phát hiện và xử lý (quan trọng cho báo cáo)

1. **Cột `extra` chứa điểm.**
   - Ở 14 tỉnh (TP.HCM, Hải Phòng, Đồng Nai, Cần Thơ, An Giang, Huế, Gia Lai…), các cột điểm trống; điểm bị dồn vào `extra` dạng chuỗi mã hóa HTML, ví dụ `To&#xE1;n=8; V&#x103;n=7; S&#x1EED;=9`.
   - Đọc thẳng: 39,3% thí sinh có điểm Toán. Sau khi `html.unescape` và tách: **98,6%**.
   - Khoảng 96% thí sinh có đủ 4 môn (Toán, Văn + 2 môn tự chọn, cấu trúc thi mới).
   - Khóa môn trong `extra`: toán, văn, ngoại ngữ, lí, hóa, sử, địa, giáo dục kinh tế pháp luật, công nghệ công nghiệp, công nghệ nông nghiệp.
2. **Đổi môn.** GDCD đổi thành **GD Kinh tế & Pháp luật** (cột `gdktpl`, chỉ có trong `extra`); thêm Tin học, Công nghệ.
3. **Mã tỉnh bị tái sử dụng.** 7 mã số cũ nay trỏ sang tỉnh khác:
   - 15 Yên Bái → Lào Cai
   - 24 Bắc Giang → Bắc Ninh
   - 44 Quảng Bình → Quảng Trị
   - 52 Bình Định → Gia Lai
   - 80 Long An → Tây Ninh
   - 82 Tiền Giang → Đồng Tháp
   - 91 Kiên Giang → An Giang

   Ghép dữ liệu cũ theo mã số mà không qua bảng ánh xạ sẽ sai mà không có lỗi nào báo ra.
4. **Trích PDF.**
   - Số định dạng Việt Nam `1.234,5`; `-` / `..` nghĩa là không có số liệu.
   - **Ô trống (giá trị 0) làm lệch cột**: gán số vào cột theo vị trí ký tự, lấy các dòng đủ cột **trên cùng trang** làm mốc (số căn phải). Mỗi biểu trải 2 trang ("Tiếp theo") với lề khác nhau.
   - Tên tỉnh trong PDF: `TP. Hồ Chí Minh`, đổi thành `Hồ Chí Minh` khi ghép.
   - Bỏ qua trang mục lục (chứa "Trang"/"Page").
5. **Kiểm chứng.** Tổng 34 tỉnh khớp **chính xác** dòng "Cả nước": dân số 102.345,3 nghìn người, giáo viên THPT 148.396, học sinh THPT 3.082.574. GRDP/người bình quân theo dân số = 124,9 so với 125,5 cả nước (chênh lệch là bình thường).
6. **Gộp chỉ tiêu bình quân** (nếu phải tự quy đổi 63 → 34): chỉ tiêu tổng thì cộng; chỉ tiêu bình quân thì tính lại theo trọng số dân số, không lấy trung bình cộng. Niên giám 2025 đã có sẵn phụ lục 34 tỉnh (2020–2025) nên hiện chưa cần.

## 5. Chỉ tiêu KT-XH đã trích (số biểu trong phụ lục)

| Biểu | Chỉ tiêu |
|---|---|
| 5 | Diện tích, mật độ dân số |
| 6 | Dân số TB 2020–2025 |
| 9 | Dân số thành thị (tính ra `ty_le_do_thi_pct`) |
| 34 | Tỷ lệ lao động qua đào tạo |
| 43 | GRDP/người 2020–2025 |
| 140 / 142 / 143 / 147 | Số trường, giáo viên, học sinh THPT; số học sinh/giáo viên |
| 158 | Thu nhập bình quân đầu người/tháng 2025 |
| 163 | Thu nhập bình quân một lao động |
| 164 | HDI |
| 166 | GINI |
| 173 | Tỷ lệ hộ nghèo |
| 186 | Tỷ lệ dùng internet |

Các biểu khác còn dùng được: doanh nghiệp (52–71), y tế (149–151), chi tiêu (167–171), nhà ở (193–196), tỷ lệ hộ có máy tính (182).

## 6. Kết quả thăm dò ban đầu (Spearman, n = 34)

| | Toán TB | Văn TB | Tỷ lệ thi Ngoại ngữ |
|---|---|---|---|
| HDI | 0,79 | 0,36 | 0,86 |
| Thu nhập bình quân đầu người | 0,76 | 0,35 | 0,85 |
| Tỷ lệ hộ nghèo | −0,77 | −0,31 | −0,79 |
| GRDP/người | 0,60 | 0,21 | 0,78 |
| Học sinh / giáo viên THPT | 0,15 | 0,24 | 0,17 |

Nhận xét:
- Toán và tỷ lệ chọn Ngoại ngữ đi theo mức sống rõ rệt; Văn thì yếu.
- Thu nhập và HDI giải thích tốt hơn GRDP (Quảng Ninh có GRDP/người cao nhất nhưng thu nhập người dân không cao nhất).
- Đây mới là thăm dò, n = 34 nhỏ.

## 7. Việc tiếp theo

Nhật ký tiến độ: mỗi phiên cập nhật mục này và mục "Ghi chép số liệu" trong `bao_cao/DE_CUONG.md`.

- [x] **PySpark ETL** (2026-11-14): `spark/etl_diemthi.py`, pandas UDF parse `extra`, khớp bản pandas 60/60 cột.
- [x] Bảng phân phối tỉnh × môn, chênh lệch giữa tỉnh theo môn (eta²), tổ hợp môn (2026-11-14).
- [x] **Spark MLlib** (2026-11-14): `spark/mllib_tinh.py`, đã chạy xong hồi quy repeated 5-fold × 5 lần và KMeans k = 2..6. Kết quả ghi trong `bao_cao/DE_CUONG.md`.
- [x] **Biểu đồ cho báo cáo** (2026-11-14): `bao_cao/ve_hinh.py` → `bao_cao/hinh/` (8 hình). ETL có thêm `pho_diem.csv` và `co_diem_theo_mon.csv`.
- [ ] **Review kiến thức cùng người dùng** — người dùng hẹn làm ngay sau khi chỉnh xong hình (2026-11-14). Giải thích bằng ngôn ngữ đời thường, có ví dụ từ chính dữ liệu đồ án. Các chủ đề:
  - Spark: vì sao dùng Spark, đọc song song/partition, lazy evaluation, pandas UDF qua Arrow, tầng Bronze/Silver/Gold.
  - Tích hợp dữ liệu: cột `extra`, mã tỉnh bị tái sử dụng, trích PDF, kiểm chứng chéo Spark = pandas.
  - Thống kê: Spearman, eta², R² ngoài mẫu và k-fold, overfitting khi n = 34, VIF.
  - Phân cụm: KMeans, silhouette, PCA.
  - Văn dồn ở 5,0: vì sao so với mốc 4,5/5,5.
  - Quyền riêng tư: xóa SBD từ bước 2, chỉ công bố số liệu tổng hợp. Ý này đã bỏ khỏi hình H4.1, cần viết trong báo cáo mục 2.4.
- [ ] **Viết báo cáo** — đang làm. Bản nháp nội dung nằm trong `bao_cao/dat_van_de.md`.
  - Đã có đủ chương 1–7 và tài liệu tham khảo (2026-11-14). Mỗi chương có đoạn báo cáo kèm lời nói mẫu. Spearman, eta², R², KMeans, silhouette, PCA đều đã có giải thích đời thường và ví dụ.
  - Người dùng yêu cầu **khoảng 25 trang** (bản đầu 54 trang bị chê dài). Lỗi đã mắc ghi trong mục 9.
  - Tài liệu tham khảo có 2 mục đánh dấu (\*) chưa chắc số hiệu/ngày; người dùng chấp nhận để nguyên.
  - [x] Đã xuất Word (2026-11-14), sửa theo góp ý: `bao_cao/BaoCao_DiemThi2026_KTXH.docx` + PDF, **22 trang** (bìa + 4 trang đầu i–iv, 17 trang thân). Không có lời cảm ơn, bảng phân công, phụ lục. Mỗi hình gói chung ảnh + chú thích trong một ô không tách trang. Sửa nội dung trong `bao_cao.md` rồi chạy lại `build_docx.js` và `cap_nhat_word.ps1`. Chỗ người dùng tự điền in đậm trong [ngoặc vuông].
  - Form: không tìm được quy định chính thức của Phenikaa; dùng form phổ biến (A4, lề 2/2/3/2 cm, TNR 13, giãn dòng 1,5, hình/bảng đánh số theo chương, TLTK APA theo ABC). Tên GV, SV là dữ liệu demo.
  - Người dùng chuộng khung **Vấn đề → Giải pháp → Kết quả** và ngôn ngữ đời thường.
- [ ] (Tùy chọn) Hồi quy: thử lưới regParam cho ridge (hiện chỉ có 0,5, quá mạnh) bằng nested CV.
- [x] Điểm Văn dồn ở 5,0 **ở cấp tỉnh** (H5.6). So với mốc 4,5/5,5, không dùng 4,75/5,25, vì Văn được chấm theo nửa điểm.
- [ ] (Tuỳ chọn) Xem tiếp ở cấp cụm điểm thi (`ma_diem_thi` = 3 số sau mã tỉnh trong SBD). Chỉ trình bày như "quan sát thống kê", không kết luận gian lận.

## 8. Lưu ý kỹ thuật

- Máy người dùng chạy **Windows** (PowerShell), có JDK 22 (chạy được với PySpark 4.0.1), không có winutils. Khi viết code Spark mới:
  - Luôn tạo session qua `spark/_session.py`.
  - Không dùng glob trong `spark.read` mà truyền danh sách file `Path.as_posix()`.
  - Không dùng `df.write` hay `addPyFile`; xuất kết quả qua `.toPandas().to_csv(...)`.
  - Chi tiết các lỗi đã gặp: `spark/README.md`.
- Docker Desktop có cài (đang tắt) — phương án dự phòng.
- Máy có Microsoft Word 16 (COM). Khi tự động hóa Word: mở CHỈ ĐỌC rồi SaveAs2 sang file tạm; không gọi `TablesOfContents.UpdatePageNumbers()` (treo); không bật `features.updateFields` trong docx-js (hiện hộp thoại); luôn chạy trong Start-Job có timeout và chỉ kill tiến trình WINWORD có `/Automation`.
- Không commit `data/raw/` hay dữ liệu cấp thí sinh. **Luôn bỏ SBD** trước khi xuất bất cứ thứ gì; chỉ báo cáo số liệu tổng hợp.
- Giữ đường dẫn tập trung trong `scripts/common.py`; script chạy từ thư mục `scripts/`.
- Người dùng là kỹ sư phần mềm (TypeScript/NestJS), quen Git; trình bày ngắn gọn, đi thẳng vào việc.

## 9. Lỗi đã mắc khi làm báo cáo (không lặp lại)

Người dùng phát hiện ở bản Word đầu tiên (2026-11-14):
1. Gọi là "đồ án": sai, đây là **bài tập lớn**.
2. Dài 54 trang (do ước lượng theo số chữ, không đo PDF thật): mục tiêu khoảng **25 trang**.
3. **Ảnh và chú thích bị tách nhau**: nay ảnh + chú thích nằm chung một ô bảng `cantSplit` (`figure()` trong `build_docx.js`), hình đặt ngay sau đoạn nhắc đến nó.
4. Có lời cảm ơn và bảng phân công dù không cần: đã bỏ.

Trước khi bàn giao file Word/PDF: kiểm tra tên loại bài, đếm trang trên PDF thật, xem từng hình có liền chú thích không.

