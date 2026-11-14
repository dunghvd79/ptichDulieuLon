# Đề cương báo cáo (~20 trang)

**Tên đề tài:** Tích hợp dữ liệu điểm thi tốt nghiệp THPT 2026 với điều kiện kinh tế – xã hội 34 tỉnh, thành và phân tích bằng Apache Spark

Quy ước trạng thái: ⬜ chưa có số liệu · 🟨 có số liệu, chưa viết · ✅ đã viết bản nháp

**Bản nháp nội dung chương 1–5 nằm trong `bao_cao/dat_van_de.md`** (mỗi chương có đoạn báo cáo + lời nói mẫu).

Khổ A4, Times New Roman 13, giãn dòng 1,3. Khoảng 20 trang nội dung, chưa tính bìa, mục lục và phụ lục.

| # | Chương / mục | Trang | Nguồn số liệu, bảng/hình | TT |
|---|---|---|---|---|
| — | Bìa, lời cảm ơn, mục lục, danh mục bảng/hình | (ngoài 20) | | ⬜ |
| 1 | **Mở đầu** | 2 | | ✅ |
| 1.1 | Bối cảnh: thi 2025+ theo chương trình mới (4 môn), sáp nhập 63 → 34 tỉnh từ 01/07/2025 | | NQ 202/2025/QH15 | ✅ |
| 1.2 | Câu hỏi nghiên cứu (2 câu) | | CLAUDE.md §1 | ✅ |
| 1.3 | Phạm vi, đóng góp: pipeline tích hợp + phân tích bằng Spark | | | ✅ |
| 2 | **Dữ liệu** | 3 | | ✅ |
| 2.1 | Điểm thi 2026: nguồn, quy mô (1.200.202 dòng, 34 CSV, ~115 MB), lược đồ | | Bảng 2.1 lược đồ cột | ✅ |
| 2.2 | Niên giám thống kê 2025: phụ lục 34 tỉnh, 209 biểu; các biểu đã trích | | Bảng 2.2 = CLAUDE.md §5 | ✅ |
| 2.3 | Bảng ánh xạ 63 → 34 tỉnh | | `data/reference/map_63_34_tinh.csv` | ✅ |
| 2.4 | Vấn đề đạo đức: dữ liệu cá nhân, bỏ SBD, chỉ công bố số liệu tổng hợp | | | ✅ |
| 3 | **Tích hợp dữ liệu: vấn đề và cách xử lý** (điểm nhấn) | 4 | | ✅ |
| 3.1 | Điểm dồn trong cột `extra` (HTML-encoded): tỷ lệ có điểm Toán 39,3% → 98,6% | | `spark/chat_luong_du_lieu.csv`; Hình 3.1 trước/sau | ✅ |
| 3.2 | Đổi môn GDCD → GD KT&PL, môn mới | | | ✅ |
| 3.3 | Mã tỉnh bị tái sử dụng (7 mã): ví dụ ghép sai im lặng | | Bảng 3.1 | ✅ |
| 3.4 | Trích bảng từ PDF: số kiểu VN, ô trống lệch cột, biểu 2 trang | | Hình 3.2 minh họa trang PDF | ✅ |
| 3.5 | Kiểm chứng: tổng 34 tỉnh = "Cả nước"; Spark = pandas | | `spark/doi_chieu_pandas` | ✅ |
| 4 | **Kiến trúc pipeline Big Data** | 3 | | ✅ |
| 4.1 | Sơ đồ tổng thể: nguồn → Bronze → Silver → Gold → MLlib → báo cáo | | H4.1 | ✅ |
| 4.2 | PySpark ETL: đọc song song, pandas UDF (Arrow) giải mã `extra`, unpivot, cửa sổ | | `spark/etl_diemthi.py` | ✅ |
| 4.3 | Môi trường và các lỗi khi triển khai Spark trên Windows | | `spark/README.md` | ✅ |
| 4.4 | Hiệu năng: thời gian từng bước, Spark vs pandas | | `spark/thoi_gian_chay.csv` | ✅ |
| 5 | **Kết quả phân tích** | 6 | | ✅ |
| 5.1 | Mô tả: phân phối điểm từng môn toàn quốc; tổ hợp môn phổ biến | | Hình 5.1 histogram; Bảng 5.1 tổ hợp | ✅ |
| 5.2 | CH2: Môn nào chênh lệch giữa các tỉnh nhiều nhất (eta², độ lệch chuẩn giữa tỉnh, khoảng cách) | | `chenh_lech_giua_tinh_theo_mon.csv`; Hình 5.2 | ✅ |
| 5.3 | CH1: Tương quan KT-XH ↔ điểm (Spearman, n=34) | | Hình 5.3 heatmap; Hình 5.4 scatter thu nhập–Toán | ✅ |
| 5.4 | Hồi quy tuyến tính MLlib (chuẩn hóa, k-fold CV) | | Bảng 5.2 hệ số, R² CV (`ml_hoi_quy_*.csv`, `ml_vif.csv`) | ✅ |
| 5.5 | Phân cụm tỉnh KMeans (chọn k bằng silhouette) | | Hình 5.5 PCA 2D tô màu theo cụm (`ml_kmeans_k3_*.csv`, `ml_pca_tai.csv`) | ✅ |
| 5.6 | Quan sát: điểm Văn dồn ở 5,0, chỉ nêu như quan sát thống kê | | H5.6, `van_dinh_5_theo_tinh.csv` | ✅ |
| 6 | **Thảo luận** | 1,5 | | ⬜ |
| 6.1 | Diễn giải; tương quan không phải nhân quả; n=34 nhỏ; ecological fallacy | | | ⬜ |
| 6.2 | Hạn chế: tự chọn môn (selection bias), dữ liệu cào web, số liệu 2025 vs thi 2026 | | | ⬜ |
| 7 | **Kết luận và hướng phát triển** | 0,5 | | ⬜ |
| — | Tài liệu tham khảo | | | ⬜ |
| — | Phụ lục: cấu trúc repo, cách chạy, bảng 34 tỉnh đầy đủ | (ngoài 20) | | ⬜ |

## Danh mục hình/bảng cần sinh (script: `notebooks/` hoặc `bao_cao/hinh/`)

Script: `bao_cao/ve_hinh.py` → `bao_cao/hinh/*.png` (200 dpi, rộng 16 cm, nền trắng). Palette đã kiểm bằng validator của skill dataviz.

- [x] H3.1 Tỷ lệ có điểm theo môn: trước và sau khi tách `extra` (dumbbell)
- [x] H4.1 Sơ đồ pipeline
- [x] H5.1 Phổ điểm 11 môn (small multiples, khoảng 0,25)
- [x] H5.2 eta² theo môn (cột ngang, nhấn mạnh Văn)
- [x] H5.3 Heatmap Spearman KT-XH × điểm (cũng ghi ra `spark/tuong_quan_spearman.csv`)
- [x] H5.4 Thu nhập → Toán và Văn (2 panel cùng trục y, tô theo cụm k = 3, R²_cv)
- [x] H5.5 KMeans k = 3 trên mặt phẳng PCA
- [x] H5.6 Văn dồn ở 5,0: toàn quốc + theo tỉnh
- [x] B5.1 Top tổ hợp môn: bảng trong mục ghi chép 2026-11-14
- [x] B5.2 Hệ số hồi quy + R²_cv: bảng trong mục ghi chép MLlib

## Ghi chép số liệu để viết (điền khi có)

_(Mỗi khi chạy ra kết quả mới, ghi số chính ở đây kèm file nguồn để lúc viết không phải tra lại.)_

### 2026-11-14 — PySpark ETL (`data/processed/spark/`)

**Chất lượng dữ liệu** (`chat_luong_du_lieu.csv`):
- 1.200.202 dòng, SBD không trùng, 34 mã tỉnh. Mã tỉnh trong SBD khớp `province_code` 100%.
- 70,4% dòng có cột `extra`. Cả 34 tỉnh đều dùng `extra` ít nhất một phần, vì GD KT&PL chỉ có trong đó.
- Có điểm Toán: **39,3% → 98,6%** sau khi tách `extra`.
- Phân bố số môn:

  | Số môn | Số thí sinh |
  |---|---|
  | 4 | 1.157.271 (96,4%) |
  | 3 | 40.075 |
  | 2 | 1.158 |
  | 1 | 1.698 |

- 0 thí sinh không có điểm nào, 0 điểm nằm ngoài khoảng [0; 10].

**Kiểm chứng:** Spark khớp pandas 60/60 cột, sai số ≤ 0,001 (`doi_chieu_pandas.csv`).

**Thời gian chạy** (local[*], 8 partition): khởi động 11 s, đọc CSV 13 s, làm sạch (pandas UDF) 16–20 s, tổng hợp gold 20 s, ghép 3 s. Tổng khoảng 65 s.

**CH2 – chênh lệch giữa tỉnh theo môn** (`chenh_lech_giua_tinh_theo_mon.csv`), xếp theo eta², tức tỷ lệ phương sai điểm thí sinh nằm ở chênh lệch giữa các tỉnh:

| Môn | eta² | Độ lệch chuẩn của TB tỉnh | Tỉnh thấp nhất → cao nhất |
|---|---|---|---|
| Ngữ văn | **0,163** | 0,53 | Vĩnh Long 5,00 → Ninh Bình 7,26 |
| Sinh học | 0,077 | 0,55 | Cao Bằng 4,49 → Bắc Ninh 6,91 |
| Tin học | 0,072 | 0,56 | Sơn La 4,86 → Hà Tĩnh 7,50 |
| Toán | 0,057 | 0,49 | Sơn La 4,25 → Ninh Bình 6,26 |
| Công nghệ | 0,042 | | |
| GD KT&PL | 0,041 | | |
| Ngoại ngữ | 0,037 | | |
| Vật lí | 0,036 | | |
| Địa lí | 0,026 | | |
| Hóa học | 0,021 | | |
| Lịch sử | 0,019 | | |

Nhận xét:
- Văn chênh lệch giữa tỉnh lớn nhất, gần gấp 3 Toán, nhưng lại tương quan yếu với KT-XH (§6 CLAUDE.md). Chênh lệch Văn vì thế có thể đến từ yếu tố khác mức sống, ví dụ khâu chấm thi. Gợi ý cho mục 5.6: điểm Văn TB của Vĩnh Long là 4,998 ≈ 5,0.
- Các môn tự chọn có selection bias: thí sinh chọn môn mình mạnh, nên chỉ so sánh trong phạm vi thận trọng.

**Tổ hợp tự chọn** (`to_hop_toan_quoc.csv`, chỉ thí sinh thi đủ 4 môn):

| Tổ hợp | Tỷ lệ |
|---|---|
| Sử + Địa | 22,8% |
| Lí + Hóa | 14,5% |
| Ngoại ngữ + Lí | 12,2% |
| Sử + GD KT&PL | 10,2% |
| Địa + GD KT&PL | 8,8% |
| Ngoại ngữ + Sử | 7,6% |

Tổng cộng có 36 tổ hợp.

### 2026-11-14 — Spark MLlib (`spark/mllib_tinh.py`, `data/processed/spark/ml_*.csv`)

**Hồi quy.** Pipeline gồm VectorAssembler → StandardScaler → LinearRegression.
- Đánh giá bằng repeated 5-fold × 5 lần lặp, seed 2026.
- R²_cv = 1 − SSE / SSE của mốc "đoán bằng trung bình tập train". Đây là R² ngoài mẫu.

| Biến phụ thuộc | M1 log(thu nhập) | M2 HDI | M3 log(GRDP) | M4 đa biến OLS | M5 đa biến ridge λ=0,5 |
|---|---|---|---|---|---|
| Toán TB | **0,65** | 0,56 | 0,26 | 0,62 | 0,48 |
| Văn TB | 0,06 | 0,04 | −0,02 | −0,08 | 0,08 |
| Điểm TB chung | **0,35** | 0,30 | 0,08 | 0,32 | 0,27 |

Độ lệch chuẩn của R²_cv giữa các lần lặp ≤ 0,04 (riêng M4–Văn là 0,13). Với Toán, RMSE giảm từ 0,50 (mốc) xuống 0,30.

**OLS đa biến M4 trên toàn bộ 34 tỉnh, Toán TB** (hệ số chuẩn hóa, p-value). R² = 0,77, R² hiệu chỉnh = 0,73:

| Biến | Hệ số chuẩn hóa | p-value |
|---|---|---|
| log(thu nhập) | +0,46 | < 0,001 |
| LĐ qua đào tạo | +0,17 | 0,005 |
| Tỷ lệ đô thị | −0,15 | 0,04 |
| HS/GV THPT | −0,10 | 0,06 |

- VIF của các biến từ 1,2 đến 2,4, nên không có đa cộng tuyến đáng ngại.
- Hệ số âm của đô thị là "khi đã giữ cố định thu nhập". Không diễn giải thành "đô thị hóa làm giảm điểm".

**Nhận xét cho báo cáo:**
- Chỉ một biến log(thu nhập) dự đoán ngoài mẫu tốt nhất. Thêm biến làm R² trong mẫu tăng lên 0,77 nhưng R²_cv không tăng. Đây là ví dụ đẹp về overfitting khi n = 34.
- Thu nhập người dân và HDI giải thích tốt hơn nhiều so với GRDP (0,65 so với 0,26).
- Văn: R²_cv ≈ 0, tức KT-XH không dự đoán được Văn. Văn lại có eta² giữa tỉnh cao nhất (0,163). Kết hợp hai điều này: chênh lệch Văn giữa tỉnh là có thật nhưng không đến từ điều kiện kinh tế – xã hội. Đây là kết luận chính cho câu hỏi 2, nối sang mục 5.6.
- Ridge λ = 0,5 quá mạnh nên underfit. Nếu cần thì thử thêm lưới λ (nested CV).

**KMeans** trên 9 biến chuẩn hóa: log(thu nhập), HDI, đô thị, LĐ qua đào tạo, hộ nghèo, internet, Toán TB, Văn TB, tỷ lệ thi Ngoại ngữ.

| k | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| Silhouette | **0,536** | 0,489 | 0,363 | 0,387 | 0,352 |

- k = 2 tách 7 tỉnh miền núi phía Bắc khỏi 27 tỉnh còn lại.
- Báo cáo dùng **k = 3**: silhouette gần bằng và dễ diễn giải hơn.

| Cụm | Số tỉnh | Thu nhập BQ (nghìn đồng/tháng) | Đô thị | Hộ nghèo | Toán TB | Văn TB | Tỷ lệ thi Ngoại ngữ | Các tỉnh |
|---|---|---|---|---|---|---|---|---|
| Đô thị – thu nhập cao | 9 | 6.777 | 55% | 0,5% | 5,88 | 6,53 | 34% | Hà Nội, TP.HCM, Hải Phòng, Đà Nẵng, Bắc Ninh, Quảng Ninh, Đồng Nai, Huế, Ninh Bình |
| Trung bình | 18 | 5.094 | 27% | 1,7% | 5,44 | 6,42 | 21% | Còn lại |
| Miền núi phía Bắc | 7 | 3.111 | 15% | 8,6% | 4,71 | 6,09 | 12% | Cao Bằng, Lai Châu, Lào Cai, Lạng Sơn, Sơn La, Tuyên Quang, Điện Biên |

Khoảng cách Toán giữa cụm đô thị và cụm miền núi là 1,17 điểm, Văn chỉ 0,44 điểm.

### 2026-11-14 — Biểu đồ và các quan sát thêm khi vẽ

- **Sinh học và Tin học không có trong `extra`.** Cột `extra` chỉ có 10 khóa môn. Điểm Sinh và Tin ở cả 34 tỉnh, kể cả 14 tỉnh dùng `extra`, đều nằm trong cột thường (tỷ lệ chọn Sinh ≥ 2,2% ở mọi tỉnh), nên không mất dữ liệu. Có thể nêu trong mục 3.1. Xem `co_diem_theo_mon.csv`.
- **Điểm lẻ không phải lỗi.** Đề trắc nghiệm mới (đúng/sai, trả lời ngắn) cho điểm lẻ, ví dụ 6,1. Tỷ lệ điểm không phải bội 0,25 theo môn:

  | Môn | Tỷ lệ điểm lẻ |
  |---|---|
  | GD KT&PL | 53% |
  | Địa | 37% |
  | Sử | 34% |
  | Sinh | 33% |
  | Lí | 27% |
  | Hóa | 26% |
  | Toán | 14% |
  | Văn | 0,4% (tự luận, chấm theo bước 0,25) |

  Vì vậy phổ điểm H5.1 được gom vào khoảng rộng 0,25, không lọc bỏ điểm lẻ.
- **Phổ điểm Toán có hai đỉnh** (khoảng 4,5 và 7–7,75), kèm các gai ở mức cao. Môn Văn lệch phải, đỉnh ở 7,0.
- **Mục 5.6 – Văn dồn ở 5,0** (`van_dinh_5_theo_tinh.csv`):
  - Văn có thói quen chấm theo nửa điểm: các mức x,0/x,5 luôn cao hơn x,25/x,75 kề bên. Vì vậy mốc so sánh là các mức cùng độ chẵn, TB(4,5; 5,5), không dùng 4,75/5,25 (sẽ phóng đại).
  - Toàn quốc: 5,0 điểm chiếm 4,1%, so với 4,5 điểm 2,0% và 5,5 điểm 4,4%. Tỷ số = **1,27**.
  - Đối chứng: các mức 4,5 / 5,5 / 6,0 có tỷ số 0,73 / 0,86 / 1,04, nên chỉ riêng 5,0 nhô lên.
  - Theo tỉnh: cao nhất là Lâm Đồng 1,82, Đồng Nai 1,74, Điện Biên 1,59, Vĩnh Long 1,58; thấp nhất (≈ 1,0) là Hưng Yên, Bắc Ninh, Lai Châu, TP.HCM, Hà Nội.
  - Chỉ trình bày như quan sát thống kê về phân phối điểm, không suy diễn nguyên nhân.
- **PCA:** PC1 giải thích 68% phương sai (trục mức sống), PC2 12%. Vĩnh Long tách hẳn trên PC2, khớp với điểm Văn TB thấp nhất (5,00).
