# Chương 1. Đặt vấn đề

## 1.1. Bối cảnh

Năm 2026 là năm thứ hai kỳ thi tốt nghiệp THPT tổ chức theo chương trình giáo dục phổ thông mới: mỗi thí sinh thi 4 môn gồm Toán, Ngữ văn và 2 môn tự chọn. Từ ngày 01/07/2025, cả nước sắp xếp lại từ 63 còn 34 tỉnh, thành phố (Nghị quyết 202/2025/QH15), nên đây là kỳ thi đầu tiên diễn ra hoàn toàn trên bản đồ hành chính mới.

Bộ dữ liệu điểm thi 2026 gồm 1.200.202 thí sinh cho biết tỉnh nào có điểm cao, tỉnh nào có điểm thấp, nhưng **không trả lời được vì sao các tỉnh lại khác nhau**, vì nó không có thông tin gì về điều kiện sống của từng địa phương. Bài tập lớn vì vậy bổ sung một nguồn thứ hai là **Niên giám thống kê 2025** của Cục Thống kê, rồi ghép hai nguồn theo tỉnh. Số liệu năm 2025 là số liệu mới nhất có tại thời điểm thi; mức sống của một địa phương lại thay đổi chậm, nên dùng được cho kỳ thi 2026.

Việc ghép không đơn giản: tên và mã tỉnh thay đổi sau sắp xếp, điểm thi của 14 tỉnh bị dồn vào một cột văn bản mã hóa, còn số liệu kinh tế – xã hội chỉ có trong file PDF. Toàn bộ dữ liệu được xử lý bằng Apache Spark, một công cụ xử lý dữ liệu lớn.

## 1.2. Câu hỏi nghiên cứu

1. **Các tỉnh có thu nhập, mức sống, mức độ đô thị hóa và điều kiện giáo dục tốt hơn thì kết quả thi tốt nghiệp THPT 2026 có cao hơn không?**
2. **Môn thi nào có mức chênh lệch giữa các tỉnh lớn nhất?**

## 1.3. Phạm vi

- **Đơn vị phân tích là tỉnh, không phải từng thí sinh.** Kết luận có dạng "tỉnh có thu nhập cao hơn thì điểm trung bình của tỉnh cao hơn", không suy ra cho từng học sinh.
- **Kết quả mang tính tương quan, không phải nhân quả.**
- **Quyền riêng tư:** điểm thi là dữ liệu cá nhân. Số báo danh bị xóa ngay ở bước làm sạch; báo cáo chỉ dùng số liệu tổng hợp theo tỉnh.

# Chương 2. Dữ liệu

Bài tập lớn sử dụng hai bộ dữ liệu rất khác nhau. Điểm chung duy nhất giữa chúng là **tỉnh**, nên tỉnh được dùng làm khóa để ghép.

@bang So sánh hai bộ dữ liệu
| | Bộ 1: Điểm thi tốt nghiệp THPT 2026 | Bộ 2: Niên giám thống kê 2025 |
|---|---|---|
| Nguồn | Dữ liệu công khai trên GitHub, thu thập từ trang tra cứu điểm ngày 01/07/2026 | Cục Thống kê, phụ lục số liệu 34 tỉnh, thành phố |
| Dạng, quy mô | 34 file CSV, 1.200.202 thí sinh, khoảng 115 MB | 1 file PDF 1.557 trang; dùng 15 bảng, lấy 24 chỉ tiêu |
| Mỗi dòng là | Một thí sinh: mã tỉnh, điểm 11 môn | Một tỉnh |
| Dùng để đo | Kết quả thi của từng tỉnh | Điều kiện kinh tế – xã hội của từng tỉnh |

**Bộ 1** gồm điểm 2 môn bắt buộc (Toán, Ngữ văn) và 9 môn tự chọn (Ngoại ngữ, Vật lí, Hóa học, Sinh học, Lịch sử, Địa lí, Giáo dục kinh tế và pháp luật, Tin học, Công nghệ).

**Bộ 2:** từ Niên giám, nhóm lấy các chỉ tiêu xếp thành 3 nhóm, khớp với câu hỏi nghiên cứu:

@bang Các nhóm chỉ tiêu lấy từ Niên giám thống kê 2025
| Nhóm | Chỉ tiêu chính |
|---|---|
| Thu nhập và mức sống | Thu nhập bình quân đầu người/tháng; GRDP bình quân đầu người; chỉ số phát triển con người (HDI); tỷ lệ hộ nghèo; tỷ lệ dùng internet |
| Đô thị hóa | Dân số thành thị, từ đó tính ra tỷ lệ đô thị hóa |
| Điều kiện giáo dục | Số học sinh trên một giáo viên THPT; tỷ lệ lao động đã qua đào tạo |

Chỉ có 34 tỉnh để phân tích, nên nhóm chỉ dùng 8 chỉ tiêu chính, không lấy cả 209 bảng: dùng quá nhiều chỉ tiêu sẽ khiến mô hình "học thuộc" dữ liệu thay vì tìm ra quy luật.

# Chương 3. Tích hợp dữ liệu

Tích hợp gồm hai việc: **làm sạch** từng nguồn (mục 3.1), rồi **ghép** hai nguồn thành một bảng chung (mục 3.2). Phần lớn vấn đề gặp phải **không làm chương trình báo lỗi**: nếu không kiểm tra kỹ, kết quả vẫn ra nhưng sai.

## 3.1. Làm sạch dữ liệu

### 3.1.1. Điểm thi bị "giấu" trong một cột văn bản

**Vấn đề:** ở 14 tỉnh, trong đó có TP.HCM, Hải Phòng, Đồng Nai, Cần Thơ, các cột điểm đều trống. Toàn bộ điểm bị dồn vào một cột phụ tên `extra`, dưới dạng chuỗi mã hóa kiểu trang web, ví dụ `To&#xE1;n=8; V&#x103;n=7` (nghĩa là Toán = 8, Văn = 7). Môn Giáo dục kinh tế và pháp luật chỉ nằm trong cột này. Đọc thẳng các cột điểm thì chỉ 39,3% thí sinh có điểm Toán, trong khi gần như ai cũng thi Toán.

**Giải pháp:** giải mã chuỗi về tiếng Việt, tách thành từng cặp "môn = điểm", rồi điền vào đúng cột môn; ô nào đã có điểm thì giữ nguyên.

**Kết quả:** 96,4% thí sinh có đủ 4 môn, đúng với cấu trúc thi mới (Bảng 3.1, Hình 3.1).

@bang Tỷ lệ thí sinh có điểm trước và sau khi xử lý cột extra
| Môn | Trước | Sau |
|---|---|---|
| Toán | 39,3% | **98,6%** |
| Ngữ văn | 39,6% | **99,0%** |
| GD kinh tế và pháp luật | 0% | **23,4%** |

@hinh H3_1_co_diem_truoc_sau.png | Tỷ lệ thí sinh có điểm theo môn, trước và sau khi xử lý cột extra | 13

### 3.1.2. Môn thi thay đổi theo chương trình mới

**Vấn đề:** dữ liệu còn cột môn cũ Giáo dục công dân (gần như trống), môn mới Giáo dục kinh tế và pháp luật không có cột riêng, môn Công nghệ được ghi thành hai tên khác nhau. Nhiều môn còn có điểm lẻ như 6,1 hay 7,35, trông giống lỗi.

**Giải pháp:** đổi tên, gộp và chuẩn hóa về 11 môn thống nhất. Điểm lẻ được xác nhận là điểm thật (đề trắc nghiệm mới có phần đúng/sai và trả lời ngắn) nên giữ nguyên.

**Kết quả:** 34 tỉnh dùng chung một danh sách 11 môn; so sánh giữa các tỉnh là so cùng một môn.

### 3.1.3. Mã tỉnh cũ bị dùng lại cho tỉnh khác

**Vấn đề:** sau sắp xếp, 7 mã số cũ nay trỏ sang một tỉnh khác hẳn (Bảng 3.2). Nếu ghép số liệu theo mã số, ví dụ số liệu của Bình Định sẽ bị gán nhầm cho Gia Lai mà **không có thông báo lỗi nào**. Tên tỉnh giữa hai nguồn cũng lệch nhau ("TP. Hồ Chí Minh" và "Hồ Chí Minh").

@bang Bảy mã tỉnh cũ được dùng lại cho tỉnh khác sau sắp xếp hành chính
| Mã | 15 | 24 | 44 | 52 | 80 | 82 | 91 |
|---|---|---|---|---|---|---|---|
| Trước 01/07/2025 | Yên Bái | Bắc Giang | Quảng Bình | Bình Định | Long An | Tiền Giang | Kiên Giang |
| Nay | Lào Cai | Bắc Ninh | Quảng Trị | Gia Lai | Tây Ninh | Đồng Tháp | An Giang |

**Giải pháp:** tự xây bảng ánh xạ 63 tỉnh cũ sang 34 tỉnh mới theo Nghị quyết 202/2025/QH15, chỉ ghép theo **mã tỉnh mới**, không ghép theo tên.

**Kết quả:** mã tỉnh mới khớp 100% với mã tỉnh nằm trong số báo danh của thí sinh.

### 3.1.4. Số liệu kinh tế – xã hội nằm trong file PDF

**Vấn đề:** Niên giám không có bản Excel. Số viết kiểu Việt Nam (`1.234,5`); một ô trống làm các số phía sau dồn sang trái và rơi nhầm vào cột khác; mỗi bảng trải trên 2 trang với lề khác nhau.

**Giải pháp:** chuyển số kiểu Việt Nam sang dạng số máy hiểu được, và xác định cột dựa trên **vị trí của từng con số trên trang** thay vì thứ tự xuất hiện.

**Kết quả:** trích được 24 chỉ tiêu cho 34 tỉnh. Cộng số liệu 34 tỉnh so với dòng "Cả nước" có sẵn trong Niên giám **khớp chính xác**: dân số 102.345,3 nghìn người, giáo viên THPT 148.396, học sinh THPT 3.082.574.

## 3.2. Ghép dữ liệu

Sau khi làm sạch, hai nguồn đã đúng nhưng vẫn nằm riêng. Việc ghép gồm 4 bước, mỗi bước giải quyết một vấn đề (Bảng 3.3).

@bang Các bước ghép hai nguồn dữ liệu
| Bước | Vấn đề | Giải pháp | Kết quả |
|---|---|---|---|
| 1. Cùng cấp độ | Một bên mỗi dòng là một thí sinh, bên kia mỗi dòng là một tỉnh | Dùng Spark gom điểm của mọi thí sinh trong cùng tỉnh: điểm TB từng môn, tỷ lệ dưới 5, tỷ lệ chọn môn… | 1.200.202 dòng thành 34 dòng × 17 chỉ số |
| 2. Cùng chìa khóa | Tên tỉnh lệch, mã tỉnh cũ bị dùng lại | Lấy mã tỉnh mới (2 chữ số đầu của số báo danh) làm khóa | 34 mã khớp hoàn toàn |
| 3. Cùng đơn vị | Mỗi bảng Niên giám một đơn vị; thiếu tỷ lệ đô thị hóa | Đặt tên cột thống nhất, tự tính tỷ lệ đô thị hóa = dân thành thị / tổng dân số | 34 dòng × 24 chỉ tiêu |
| 4. Ghép | Hai bảng vẫn tách rời | Nối hai bảng theo mã tỉnh | Bảng chung 34 dòng × 43 cột |

Kết quả là một bảng chung, mỗi tỉnh nằm trên một dòng, vừa có điểm thi vừa có số liệu kinh tế – xã hội (Bảng 3.4).

@bang Ba dòng ví dụ của bảng dữ liệu sau khi ghép
| Tỉnh | Thu nhập BQ (nghìn đ/tháng) | HDI | Tỷ lệ đô thị | Số thí sinh | Toán TB | Văn TB | Thi Ngoại ngữ |
|---|---|---|---|---|---|---|---|
| Hà Nội | 8.374 | 0,84 | 47,8% | 125.419 | 6,17 | 7,02 | 47% |
| Hồ Chí Minh | 8.064 | 0,83 | 77,1% | 139.114 | 6,19 | 6,59 | 46% |
| Điện Biên | 2.583 | 0,66 | 13,9% | 7.947 | 4,46 | 6,32 | 8% |

## 3.3. Kiểm chứng

Vì các lỗi trên đều "im lặng", kết quả được kiểm tra bằng nhiều cách độc lập. Quan trọng nhất là **làm lại toàn bộ bằng hai công cụ khác nhau** (Spark và pandas) rồi so từng con số.

@bang Kết quả kiểm tra chất lượng dữ liệu
| Kiểm tra | Kết quả |
|---|---|
| Số báo danh trùng lặp | Không có (1.200.202 / 1.200.202) |
| Điểm nằm ngoài khoảng 0–10; thí sinh không có điểm nào | Không có |
| Tổng 34 tỉnh so với dòng "Cả nước" trong Niên giám | Khớp chính xác |
| Ghép hai nguồn theo tỉnh | 34 / 34 tỉnh, không ô trống |
| Kết quả Spark so với pandas | Khớp 60 / 60 cột số liệu |

# Chương 4. Pipeline xử lý bằng Apache Spark

## 4.1. Vì sao dùng Apache Spark

Apache Spark **chia dữ liệu thành nhiều phần và giao cho nhiều "người" làm cùng lúc**, rồi gộp kết quả. Giống như chấm 1,2 triệu bài thi: chia thành 8 chồng cho 8 giám khảo chấm song song thay vì một người chấm lần lượt. Máy chạy bài tập lớn có 8 nhân CPU, nên Spark chia dữ liệu làm 8 phần.

Nói thẳng, 1,2 triệu dòng (khoảng 115 MB) chưa phải dữ liệu quá lớn; pandas trên một máy vẫn xử lý được, và nhóm đã dùng pandas để kiểm chứng. Nhóm chọn Spark vì cùng một đoạn mã có thể chạy trên cụm nhiều máy khi dữ liệu tăng (ví dụ gộp nhiều năm thi), và vì yêu cầu của học phần. Spark chạy ở chế độ local (một máy, 8 nhân), phiên bản PySpark 4.0.

## 4.2. Năm bước của pipeline

Pipeline gồm 5 bước (Hình 4.1, Bảng 4.1). Ba bước đầu theo cách tổ chức ba tầng **Bronze → Silver → Gold**: dữ liệu thô → dữ liệu đã làm sạch → dữ liệu đã tổng hợp.

@hinh H4_1_pipeline.png | Sơ đồ pipeline xử lý dữ liệu | 15

@bang Năm bước của pipeline và thời gian chạy
| Bước | Làm gì | Tính năng Spark | Thời gian |
|---|---|---|---|
| 1. Đọc (Bronze) | Đọc 34 file CSV song song | Đọc nhiều file cùng lúc | 8 giây |
| 2. Làm sạch (Silver) | Giải mã cột extra, chuẩn hóa 11 môn, xóa số báo danh | pandas UDF (xử lý theo lô) | 16 giây |
| 3. Tổng hợp (Gold) | Gom theo tỉnh, tỉnh × môn; phổ điểm, tổ hợp môn | groupBy, unpivot | 19 giây |
| 4. Ghép | Nối với bảng Niên giám theo mã tỉnh | join | 3 giây |
| 5. Phân tích | Hồi quy, phân cụm tỉnh | Spark MLlib | khoảng 4 phút |

Bước 1–4 chạy trong khoảng 1 phút. Bước 5 lâu hơn vì mỗi mô hình được huấn luyện lại 25 lần để kiểm tra độ tin cậy.

## 4.3. Ba kỹ thuật Spark được sử dụng

- **Chia nhỏ dữ liệu (partition):** 1,2 triệu dòng được chia làm 8 phần, mỗi nhân CPU xử lý một phần. Thêm máy, thêm nhân là thêm "người làm".
- **Làm sau, tính trước (lazy evaluation):** Spark không chạy ngay từng lệnh mà ghi lại cả "công thức", đến khi cần kết quả mới tìm cách chạy hiệu quả nhất một lượt, giống ghi hết danh sách rồi mới đi chợ. Dữ liệu đã làm sạch được giữ trong bộ nhớ (cache) để dùng lại.
- **Xử lý theo lô (pandas UDF):** hàm giải mã cột `extra` viết bằng Python. Thay vì gọi 1,2 triệu lần cho từng dòng, Spark gửi dữ liệu sang Python theo từng lô khoảng 10.000 dòng qua định dạng Apache Arrow, giống chở hàng bằng xe tải thay vì cầm từng món.

## 4.4. Khó khăn khi triển khai trên Windows

Spark được thiết kế chủ yếu cho Linux. Trên Windows nhóm gặp 7 lỗi, phần lớn không báo nguyên nhân rõ ràng, chương trình chỉ treo hoặc dừng. Ba lỗi tiêu biểu: đường dẫn thư mục có dấu cách khiến Spark không khởi động được; Python 3.12 làm các hàm Python tự viết bị dừng đột ngột (phải dùng Python 3.11); việc đọc file theo mẫu `*.csv` bị treo vì thiếu công cụ phụ trợ của Hadoop trên Windows (phải liệt kê cụ thể 34 file). Toàn bộ cách xử lý được đóng gói vào một file khởi tạo dùng chung.

# Chương 5. Kết quả phân tích

## 5.1. Bức tranh chung về điểm thi 2026

Điểm trung bình toàn quốc môn Ngữ văn là **6,50**, Toán là **5,65** (Hình 5.1). Phổ điểm Toán có **hai đỉnh** (khoảng 4,5 và 7–7,75 điểm), cho thấy thí sinh chia thành hai nhóm khá rõ về năng lực Toán. Giữa 34 tỉnh, điểm Toán trung bình dao động từ 4,25 (Sơn La) đến 6,26 (Ninh Bình); điểm Văn từ 5,00 (Vĩnh Long) đến 7,26 (Ninh Bình). Tổ hợp tự chọn phổ biến nhất là Lịch sử + Địa lí (22,8%), tiếp theo là Vật lí + Hóa học (14,5%).

@hinh H5_1_pho_diem_mon.png | Phổ điểm toàn quốc theo môn, kỳ thi tốt nghiệp THPT 2026 | 13.5

## 5.2. Câu hỏi 1: Mức sống, đô thị hóa, điều kiện giáo dục và điểm thi

### 5.2.1. Tương quan: các tỉnh xếp hạng giống nhau đến đâu?

**Cách đo:** dùng **hệ số tương quan Spearman**. Tưởng tượng hai bảng xếp hạng 34 tỉnh, một theo **thu nhập**, một theo **điểm Toán**. Nếu tỉnh đứng đầu bảng này cũng đứng đầu bảng kia thì hai thứ "đi cùng nhau". Spearman đo **hai bảng xếp hạng giống nhau đến đâu**, chỉ xét thứ hạng chứ không xét con số. Ví dụ với 5 tỉnh (Bảng 5.1), hai bảng gần như trùng nhau, chỉ Quảng Ninh và Hà Tĩnh đổi chỗ, nên hệ số là 0,90.

@bang Ví dụ tính hệ số Spearman với 5 tỉnh
| Tỉnh | Thu nhập (nghìn đ/tháng) | Toán TB | Hạng thu nhập | Hạng Toán |
|---|---|---|---|---|
| Hà Nội | 8.374 | 6,17 | 1 | 1 |
| Quảng Ninh | 6.917 | 5,51 | 2 | 3 |
| Hà Tĩnh | 4.457 | 5,99 | 3 | 2 |
| Đắk Lắk | 4.421 | 5,14 | 4 | 4 |
| Điện Biên | 2.583 | 4,46 | 5 | 5 |

Hệ số chạy từ −1 đến 1: gần **1** là hai bảng xếp hạng gần trùng nhau, gần **0** là không liên quan, gần **−1** là ngược nhau. Với 34 tỉnh, hệ số cần lớn hơn khoảng 0,34 (âm hay dương) mới khó xảy ra do ngẫu nhiên.

**Kết quả** (Hình 5.2): tỉnh có thu nhập cao, HDI cao, ít hộ nghèo thì điểm Toán và tỷ lệ thí sinh chọn thi Ngoại ngữ cao hơn rõ rệt. Tương quan thu nhập – Toán là **0,76**, HDI – Toán **0,79**, hộ nghèo – Toán **−0,77**; tỷ lệ chọn thi Ngoại ngữ còn đi sát mức sống hơn (0,85–0,86). Điểm Văn chỉ liên quan yếu (0,35), còn số học sinh trên một giáo viên gần như không liên quan (0,15). Đáng chú ý, **thu nhập người dân** liên quan mạnh hơn **GRDP** (0,60): Quảng Ninh có GRDP bình quân đầu người cao nhất nước nhưng thu nhập người dân không cao tương ứng.

@hinh H5_3_heatmap_spearman.png | Tương quan Spearman giữa chỉ tiêu kinh tế – xã hội và kết quả thi | 14

### 5.2.2. Hồi quy: thu nhập dự đoán được bao nhiêu phần điểm thi?

**Cách đo:** dùng Spark MLlib xây công thức đoán điểm từ thu nhập, dạng "điểm Toán = a + b × thu nhập". Để biết công thức có thật sự tìm ra quy luật hay chỉ "học thuộc", nhóm kiểm tra bằng **"đề chưa gặp" (kiểm định chéo 5 phần)**: chia 34 tỉnh làm 5 nhóm, giấu 1 nhóm, xây công thức trên 4 nhóm còn lại rồi đoán điểm nhóm bị giấu; lần lượt giấu từng nhóm và lặp lại 5 lần. Chỉ số **R² ngoài mẫu** cho biết cách đoán này tốt hơn bao nhiêu so với đoán mọi tỉnh bằng điểm trung bình cả nước: R² = 1 là đoán đúng hoàn toàn, R² = 0 là không tốt hơn đoán bừa.

@bang R² ngoài mẫu của các mô hình hồi quy (kiểm định chéo 5 phần, lặp 5 lần)
| Mô hình (dùng chỉ tiêu nào để đoán) | Toán TB | Văn TB | Điểm TB chung |
|---|---|---|---|
| Chỉ thu nhập | **0,65** | 0,06 | **0,35** |
| Chỉ HDI | 0,56 | 0,04 | 0,30 |
| Chỉ GRDP | 0,26 | −0,02 | 0,08 |
| 4 chỉ tiêu: thu nhập, đô thị hóa, lao động qua đào tạo, HS/GV | 0,62 | −0,08 | 0,32 |

**Kết quả** (Bảng 5.2, Hình 5.3): chỉ riêng thu nhập đã giải thích được khoảng **65%** chênh lệch điểm Toán giữa các tỉnh; sai số trung bình khi đoán giảm từ 0,50 xuống 0,30 điểm. Với Văn, mô hình gần như không đoán được gì. Mô hình 4 chỉ tiêu khớp dữ liệu cũ tốt hơn (R² = 0,77 trên chính 34 tỉnh) nhưng đoán tỉnh mới lại **kém hơn** mô hình chỉ có thu nhập: với 34 tỉnh, thêm chỉ tiêu chỉ làm mô hình "học thuộc". Trong mô hình nhiều chỉ tiêu, thu nhập vẫn có ảnh hưởng mạnh nhất; đô thị hóa không cho thêm thông tin khi đã tính đến thu nhập.

@hinh H5_4_thu_nhap_toan_van.png | Thu nhập bình quân và điểm Toán, Ngữ văn của 34 tỉnh | 14

### 5.2.3. Phân cụm: các tỉnh tự chia thành mấy nhóm?

**Cách đo:** thuật toán **KMeans** của Spark MLlib tự xếp các tỉnh giống nhau vào cùng nhóm dựa trên 9 chỉ tiêu (thu nhập, HDI, đô thị hóa, hộ nghèo, điểm Toán, điểm Văn…), giống chia lớp thành các tổ theo đặc điểm. Số nhóm được chọn bằng **chỉ số silhouette**, đo mỗi tỉnh có "ngồi đúng bàn" không (giống nhóm mình hơn nhóm bên cạnh; càng gần 1 càng tốt). Chia 2 nhóm có silhouette cao nhất (0,54) nhưng chỉ tách 7 tỉnh miền núi phía Bắc, quá hiển nhiên; chia **3 nhóm** có silhouette gần bằng (0,49) và nhiều thông tin hơn nên được chọn.

@bang Đặc điểm ba nhóm tỉnh do thuật toán KMeans chia
| Nhóm | Số tỉnh | Thu nhập (nghìn đ/tháng) | Đô thị hóa | Hộ nghèo | Toán TB | Văn TB | Thi Ngoại ngữ |
|---|---|---|---|---|---|---|---|
| Đô thị – thu nhập cao | 9 | khoảng 6.800 | 55% | 0,5% | **5,88** | 6,53 | 34% |
| Trung bình | 18 | khoảng 5.100 | 27% | 1,7% | 5,44 | 6,42 | 21% |
| Miền núi phía Bắc | 7 | khoảng 3.100 | 15% | 8,6% | **4,71** | 6,09 | 12% |

**Kết quả** (Bảng 5.3, Hình 5.4): nhóm đô thị – thu nhập cao gồm Hà Nội, TP.HCM, Hải Phòng, Đà Nẵng, Bắc Ninh, Quảng Ninh, Đồng Nai, Huế, Ninh Bình; nhóm miền núi phía Bắc gồm Cao Bằng, Lai Châu, Lào Cai, Lạng Sơn, Sơn La, Tuyên Quang, Điện Biên. Hai nhóm này chênh nhau **1,17 điểm Toán** nhưng chỉ **0,44 điểm Văn**. Hình 5.4 dùng kỹ thuật **PCA** để "nén" 9 chỉ tiêu thành 2 trục vẽ được, giống chụp ảnh một vật từ góc thấy rõ hình dạng nhất. Trục ngang giữ 68% thông tin và là "trục mức sống"; trục dọc gần như chỉ do điểm Văn quyết định, tức điểm Văn tạo khác biệt riêng, không nằm trên trục mức sống.

@hinh H5_5_kmeans_pca.png | Ba nhóm tỉnh do KMeans chia, vẽ trên mặt phẳng PCA | 13

### 5.2.4. Trả lời câu hỏi 1

**Có.** Các tỉnh có thu nhập, mức sống và điều kiện tốt hơn có kết quả thi cao hơn, **rõ nhất ở Toán và việc chọn thi Ngoại ngữ**, yếu ở Văn. Thu nhập người dân là chỉ tiêu giải thích tốt nhất, tốt hơn GRDP; đô thị hóa chủ yếu đi kèm thu nhập; số học sinh trên một giáo viên gần như không liên quan.

## 5.3. Câu hỏi 2: Môn nào chênh lệch giữa các tỉnh nhiều nhất?

**Cách đo:** dùng chỉ số **eta²**. Điểm của 1,2 triệu thí sinh khác nhau vì hai nguồn: **khác tỉnh** (tỉnh này điểm trung bình cao, tỉnh kia thấp) và **khác người trong cùng tỉnh**. eta² cho biết bao nhiêu phần trăm sự khác nhau về điểm là do khác tỉnh. Nói cách khác: biết thí sinh ở tỉnh nào thì đoán điểm chính xác hơn bao nhiêu. Ví dụ ở Bảng 5.4: môn X thì biết tỉnh là đoán được điểm, môn Y thì không.

@bang Ví dụ eta² với 2 tỉnh, mỗi tỉnh 3 thí sinh (số liệu minh họa)
| | Tỉnh A | Tỉnh B | eta² | Ý nghĩa |
|---|---|---|---|---|
| Môn X | 7 – 8 – 9 | 3 – 4 – 5 | **86%** | Khác biệt chủ yếu do tỉnh |
| Môn Y | 3 – 6 – 9 | 2 – 5 – 8 | **4%** | Khác biệt chủ yếu giữa các bạn |

**Kết quả** (Hình 5.5): **Ngữ văn chênh lệch giữa các tỉnh nhiều nhất** với eta² = 16,3%, gấp gần 3 lần Toán (5,7%); điểm Văn trung bình thấp nhất là Vĩnh Long (5,00), cao nhất là Ninh Bình (7,26). **Lịch sử đồng đều nhất** (1,9%). Ngay cả với Văn, 84% khác biệt vẫn nằm giữa các bạn trong cùng một tỉnh. Sinh học (7,7%) và Tin học (7,2%) đứng thứ 2, 3 nhưng ít người thi và người chọn thường giỏi môn đó, nên kém chắc chắn hơn Toán và Văn.

@hinh H5_2_eta2_chenh_lech_mon.png | Mức chênh lệch giữa các tỉnh theo từng môn (eta²) | 13

## 5.4. Phát hiện chính

Đặt hai kết quả cạnh nhau: Toán có chênh lệch giữa tỉnh ở mức trung bình (5,7%) nhưng thu nhập dự đoán được 65%; còn **Ngữ văn chênh lệch nhiều nhất (16,3%) nhưng mức sống gần như không dự đoán được (R² = 0,06)**. Chênh lệch điểm Văn giữa các tỉnh là có thật nhưng đến từ yếu tố khác ngoài điều kiện kinh tế – xã hội, chẳng hạn cách dạy hay cách chấm bài tự luận ở từng địa phương. Dữ liệu hiện có chưa đủ để xác định yếu tố nào.

## 5.5. Quan sát thêm: điểm Văn dồn ở đúng 5,0

Văn được chấm theo nửa điểm nên các mức x,0 và x,5 luôn nhiều hơn mức x,25 và x,75 kề bên; vì vậy nhóm so mức 5,0 với các mức **cùng loại** là 4,5 và 5,5. Toàn quốc có 4,1% bài được đúng 5,0 điểm, trong khi 4,5 có 2,0% và 5,5 có 4,4%: mức 5,0 nhiều gấp **1,27 lần** trung bình hai mức lân cận, trong khi các mức đối chứng (4,5; 5,5; 6,0) không có hiện tượng này. Theo tỉnh, cao nhất là Lâm Đồng (1,82) và Đồng Nai (1,74); gần như không có ở Hưng Yên, Bắc Ninh, TP.HCM, Hà Nội (Hình 5.6). Đây chỉ là **quan sát thống kê về hình dạng phổ điểm**; nhóm không có dữ liệu để kết luận nguyên nhân.

@hinh H5_6_van_dinh_5.png | Số bài Ngữ văn dồn ở đúng 5,0 điểm | 13

# Chương 6. Thảo luận và hạn chế

## 6.1. Thảo luận

Dữ liệu chỉ cho thấy các đại lượng đi cùng nhau, không cho biết vì sao. Một số giả thuyết (chưa được kiểm chứng):

- **Toán và Ngoại ngữ** phụ thuộc nhiều vào luyện tập có hệ thống (học thêm, tài liệu, trung tâm ngoại ngữ), vốn tập trung ở nơi có thu nhập cao và đô thị hóa cao.
- **Ngữ văn** là môn tự luận, kết quả phụ thuộc nhiều vào cách dạy, cách ôn và việc chấm bài theo hướng dẫn chấm, những yếu tố có thể khác nhau giữa các địa phương mà không liên quan đến thu nhập.
- **Số học sinh trên một giáo viên** không liên quan đến điểm không có nghĩa giáo viên không quan trọng: chỉ tiêu này chỉ đo số lượng, không đo chất lượng, và chênh lệch ít giữa các tỉnh (17–26 học sinh/giáo viên).

## 6.2. Hạn chế

- **Tương quan không phải nhân quả**, và kết luận ở cấp tỉnh không áp dụng cho từng học sinh.
- **Chỉ có 34 tỉnh**, các con số có độ dao động; đã hạn chế bằng kiểm định chéo và mô hình đơn giản.
- **Môn tự chọn:** người chọn thường là người giỏi môn đó, nên so sánh giữa các tỉnh ở các môn này kém chắc chắn.
- **Tỉnh sau sáp nhập gồm nhiều vùng khác nhau**; con số trung bình của tỉnh che mất khác biệt bên trong.
- **Dữ liệu điểm thi lấy từ nguồn cộng đồng**, đã kiểm tra tính nhất quán nhưng chưa đối chiếu với số liệu chính thức của Bộ Giáo dục và Đào tạo.
- **Chỉ có một năm thi**, số liệu kinh tế – xã hội năm 2025 dùng cho kỳ thi 2026.

# Chương 7. Kết luận và hướng phát triển

## 7.1. Kết luận

Bài tập lớn đã **tích hợp hai nguồn dữ liệu rất khác nhau**: điểm thi tốt nghiệp THPT 2026 của 1.200.202 thí sinh và số liệu kinh tế – xã hội năm 2025 của 34 tỉnh, thành phố trích từ Niên giám thống kê dạng PDF, xử lý bằng Apache Spark. Quá trình tích hợp phát hiện và xử lý nhiều lỗi dữ liệu không gây báo lỗi, nổi bật là điểm thi bị giấu trong cột văn bản (tỷ lệ có điểm Toán từ 39,3% lên 98,6%) và 7 mã tỉnh bị dùng lại. Kết quả được kiểm chứng với số liệu cả nước và bằng một pipeline độc lập (khớp 60/60 cột).

Trả lời hai câu hỏi nghiên cứu:

1. **Tỉnh có mức sống tốt hơn có kết quả thi cao hơn, rõ nhất ở Toán và việc chọn thi Ngoại ngữ.** Chỉ riêng thu nhập bình quân đầu người giải thích được khoảng 65% chênh lệch điểm Toán giữa các tỉnh, tốt hơn nhiều so với GRDP.
2. **Ngữ văn là môn chênh lệch giữa các tỉnh nhiều nhất**, gấp gần 3 lần Toán; Lịch sử đồng đều nhất.

**Phát hiện chính:** Ngữ văn chênh lệch giữa các tỉnh nhiều nhất nhưng lại ít liên quan đến mức sống nhất.

## 7.2. Hướng phát triển

- Gộp điểm nhiều năm thi để kiểm tra các quan hệ có ổn định không; khi đó dữ liệu lớn hơn nhiều lần, đúng thế mạnh của Spark.
- Phân tích ở cấp nhỏ hơn tỉnh (cụm điểm thi, cấp xã), đặc biệt để tìm hiểu chênh lệch điểm Văn.
- Bổ sung chỉ tiêu giáo dục về chất lượng: trình độ giáo viên, chi tiêu cho giáo dục.

# Tài liệu tham khảo

**Tài liệu tiếng Việt**

@ref Bộ Giáo dục và Đào tạo. *Quy chế thi tốt nghiệp trung học phổ thông* (áp dụng từ năm 2025 theo chương trình giáo dục phổ thông 2018).

@ref Cục Thống kê. (2026). *Niên giám thống kê 2025*. Hà Nội. https://www.nso.gov.vn/wp-content/uploads/2026/07/NG-TOAN-QUOC-2025-1.pdf

@ref Quốc hội. (2025). *Nghị quyết số 202/2025/QH15 về việc sắp xếp đơn vị hành chính cấp tỉnh*. Hiệu lực từ ngày 01/07/2025.

**Tài liệu tiếng Anh**

@ref Apache Software Foundation. (2025). *Apache Spark 4.0 documentation and PySpark API reference*. https://spark.apache.org/docs/latest/

@ref duongtrongnguyen123. (2026). *diem-thi-thptqg-2026* [Bộ dữ liệu]. GitHub. https://github.com/duongtrongnguyen123/diem-thi-thptqg-2026

@ref Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The elements of statistical learning* (2nd ed.). Springer.

@ref Lloyd, S. (1982). Least squares quantization in PCM. *IEEE Transactions on Information Theory, 28*(2), 129–137.

@ref Meng, X., Bradley, J., Yavuz, B., Sparks, E., Venkataraman, S., Liu, D., … Talwalkar, A. (2016). MLlib: Machine learning in Apache Spark. *Journal of Machine Learning Research, 17*(34), 1–7.

@ref Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics, 20*, 53–65.

@ref Spearman, C. (1904). The proof and measurement of association between two things. *The American Journal of Psychology, 15*(1), 72–101.

@ref Zaharia, M., Xin, R. S., Wendell, P., Das, T., Armbrust, M., Dave, A., … Stoica, I. (2016). Apache Spark: A unified engine for big data processing. *Communications of the ACM, 59*(11), 56–65.
