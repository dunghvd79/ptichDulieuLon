# Đặt vấn đề, Dữ liệu và Tích hợp dữ liệu

Phần A, C, E dùng cho báo cáo (chương 1, 2, 3). Phần B, D, F là lời nói mẫu khi thuyết trình.
Số liệu lấy từ `data/processed/spark/` và các ghi chép trong `bao_cao/DE_CUONG.md`.

---

## A. Đoạn đặt vấn đề cho báo cáo

### Bối cảnh

Năm 2026 là năm thứ hai kỳ thi tốt nghiệp THPT tổ chức theo chương trình giáo dục phổ thông mới. Mỗi thí sinh thi 4 môn: Toán, Ngữ văn và 2 môn tự chọn. Cũng từ ngày 01/07/2025, cả nước sắp xếp lại từ 63 còn 34 tỉnh, thành phố (Nghị quyết 202/2025/QH15). Kỳ thi 2026 là kỳ thi đầu tiên diễn ra hoàn toàn trên bản đồ hành chính mới.

Bộ dữ liệu điểm thi 2026 gồm 1.200.202 thí sinh của 34 tỉnh, thành phố. Từ bộ dữ liệu này có thể biết tỉnh nào có điểm cao, tỉnh nào có điểm thấp. Tuy nhiên bộ điểm thi không chứa thông tin gì về điều kiện sống của từng địa phương, nên **không trả lời được câu hỏi vì sao các tỉnh lại khác nhau.**

### Vì sao cần thêm dữ liệu kinh tế – xã hội

Để tìm hiểu điểm thi có đi cùng điều kiện của địa phương hay không, đồ án bổ sung một nguồn dữ liệu thứ hai là **Niên giám thống kê 2025** của Cục Thống kê. Niên giám có phụ lục số liệu cho đúng 34 tỉnh, thành phố mới, gồm thu nhập bình quân, chỉ số phát triển con người (HDI), tỷ lệ dân số thành thị, tỷ lệ hộ nghèo, số học sinh trên một giáo viên THPT và nhiều chỉ tiêu khác.

Số liệu năm 2025 được chọn vì đây là số liệu mới nhất có tại thời điểm thi. Mặt khác, mức sống của một địa phương thay đổi chậm, và điều kiện tác động đến học sinh lớp 12 năm 2026 là những năm học trước đó.

Hai nguồn dữ liệu được ghép với nhau theo tỉnh. Đây là phần **tích hợp dữ liệu** của đồ án. Việc ghép không đơn giản vì:
- tên và mã tỉnh thay đổi sau sắp xếp;
- điểm thi của 14 tỉnh bị dồn vào một cột văn bản mã hóa;
- số liệu kinh tế – xã hội chỉ có trong file PDF.

Dữ liệu được xử lý bằng Apache Spark, một công cụ xử lý dữ liệu lớn.

### Câu hỏi nghiên cứu

1. **Các tỉnh có thu nhập, mức sống, mức độ đô thị hóa và điều kiện giáo dục tốt hơn thì kết quả thi tốt nghiệp THPT 2026 có cao hơn không?**
2. **Môn thi nào có mức chênh lệch giữa các tỉnh lớn nhất?**

### Phạm vi và giới hạn

- **Đơn vị phân tích là tỉnh, không phải từng thí sinh.** Kết luận có dạng "tỉnh có thu nhập cao hơn thì điểm trung bình của tỉnh cao hơn". Không suy ra rằng mọi học sinh nhà khá giả đều điểm cao.
- **Kết quả mang tính tương quan, không phải nhân quả.** Hai đại lượng cùng tăng giảm chưa có nghĩa là cái này gây ra cái kia.
- **Chỉ có 34 tỉnh**, nên các mô hình được kiểm tra trên dữ liệu không dùng để xây dựng chúng, để tránh kết luận quá đà.
- **Quyền riêng tư:** dữ liệu điểm thi là dữ liệu cá nhân. Số báo danh bị xóa ngay ở bước làm sạch, và báo cáo chỉ dùng số liệu tổng hợp theo tỉnh.

---

## B. Lời nói mẫu khi thuyết trình

### Mở đầu (khoảng 30 giây)

> "Nhóm em có trong tay điểm thi tốt nghiệp năm 2026 của 1,2 triệu thí sinh trên 34 tỉnh, thành. Nhìn vào đó thì biết tỉnh nào điểm cao, tỉnh nào điểm thấp, nhưng không biết **vì sao**. Bộ điểm không có gì về chuyện tỉnh đó giàu hay nghèo, ở thành phố hay miền núi.
>
> Vì vậy nhóm lấy thêm Niên giám thống kê 2025, có số liệu thu nhập, mức sống, đô thị hóa và trường lớp của đúng 34 tỉnh mới, rồi ghép hai nguồn lại với nhau. Từ đó nhóm trả lời hai câu hỏi: tỉnh giàu hơn có điểm cao hơn không, và môn nào các tỉnh chênh nhau nhiều nhất."

### Câu hỏi 1: Mức sống và điểm thi (khoảng 45 giây, chiếu hình H5.4)

> "Câu hỏi đầu tiên: tỉnh có mức sống tốt hơn thì thi có tốt hơn không?
>
> Câu trả lời là **có, và rõ nhất ở môn Toán.** Nhóm chia 34 tỉnh thành ba nhóm.
> - Nhóm thành phố lớn như Hà Nội, TP.HCM, Hải Phòng, Đà Nẵng: thu nhập bình quân khoảng 6,8 triệu đồng một người một tháng, điểm Toán trung bình 5,9.
> - Nhóm 7 tỉnh miền núi phía Bắc như Điện Biên, Lai Châu, Sơn La: thu nhập chỉ khoảng 3,1 triệu, điểm Toán trung bình 4,7.
>
> Hai nhóm chênh nhau hơn 1 điểm Toán. Nếu chỉ biết thu nhập của một tỉnh, nhóm đã đoán được khoảng **hai phần ba** sự chênh lệch điểm Toán giữa các tỉnh.
>
> Nhưng với **môn Văn thì gần như không đoán được gì.** Hai nhóm tỉnh giàu và nghèo chỉ chênh nhau chưa tới nửa điểm Văn.
>
> Nhóm cũng thấy ba điều nữa:
> - Thu nhập của người dân nói lên nhiều hơn GRDP của tỉnh. Có tỉnh làm ra rất nhiều của cải, như Quảng Ninh, nhưng thu nhập người dân không cao tương ứng.
> - Đô thị hóa chủ yếu đi kèm với thu nhập. Khi đã tính đến thu nhập thì đô thị hóa không cho thêm thông tin gì.
> - Số học sinh trên một giáo viên gần như không liên quan đến điểm thi."

**Nếu thầy hỏi "hai phần ba là đo thế nào?":**

> "Nhóm lấy thu nhập để dự đoán điểm Toán của từng tỉnh, nhưng mỗi lần đều giấu đi một vài tỉnh, xây công thức trên các tỉnh còn lại rồi đoán thử các tỉnh bị giấu. Cách đoán này giảm được khoảng 65% sai số so với việc đoán mọi tỉnh bằng điểm trung bình cả nước. Làm vậy để chắc rằng công thức đoán được cả những tỉnh nó chưa từng thấy, chứ không chỉ khớp với dữ liệu đã có."

### Câu hỏi 2: Môn nào chênh lệch nhiều nhất (khoảng 30 giây, chiếu hình H5.2)

> "Câu hỏi thứ hai: môn nào có điểm chênh lệch giữa các tỉnh nhiều nhất?
>
> Hãy tưởng tượng em chỉ cho thầy biết một bạn thí sinh đến từ tỉnh nào, rồi nhờ thầy đoán điểm của bạn ấy. Nếu các tỉnh có điểm gần như nhau, biết tỉnh cũng chẳng giúp thầy đoán được gì. Nếu có tỉnh rất cao, có tỉnh rất thấp, thì chỉ cần biết tỉnh là thầy đã đoán gần đúng hơn nhiều.
>
> Nhóm đo đúng điều đó cho từng môn. **Ngữ văn là môn chênh lệch giữa các tỉnh nhiều nhất**, gấp gần 3 lần môn Toán. Điểm Văn trung bình cao nhất là Ninh Bình, 7,26 điểm; thấp nhất là Vĩnh Long, 5,0 điểm. Ngược lại, Lịch sử là môn các tỉnh đều nhau nhất."

**Nếu thầy hỏi "đo bằng cách nào?":**

> "Nhóm dùng chỉ số eta bình phương. Hiểu đơn giản: điểm của 1,2 triệu thí sinh khác nhau rất nhiều, và chỉ số này cho biết bao nhiêu phần trăm sự khác nhau đó là do các bạn ở tỉnh khác nhau. Với Văn là 16%, Toán 6%, Lịch sử 2%. Nhóm không chỉ lấy tỉnh cao nhất trừ tỉnh thấp nhất, vì như vậy chỉ nhìn hai tỉnh ở hai đầu và bỏ qua 32 tỉnh còn lại."

Lưu ý khi nói: luôn nói đủ cụm "16% **sự khác nhau về điểm**", để người nghe không hiểu nhầm thành "16% thí sinh".

### Ghép hai câu hỏi: phát hiện chính (khoảng 20 giây)

> "Đặt hai kết quả cạnh nhau thì thấy một điều bất ngờ. Môn Văn là môn các tỉnh chênh nhau nhiều nhất, nhưng lại là môn **ít liên quan đến giàu nghèo nhất**. Nghĩa là chênh lệch điểm Văn giữa các tỉnh là có thật, nhưng đến từ một nguyên nhân khác, chứ không phải điều kiện kinh tế. Nhóm cho rằng đây là điều đáng chú ý nhất của đồ án, và là hướng để tìm hiểu thêm."

---

# Dữ liệu

Phần C dùng cho báo cáo (chương 2). Phần D là lời nói mẫu khi thuyết trình, nói ngay sau phần đặt vấn đề.

## C. Đoạn mô tả dữ liệu cho báo cáo

Đồ án sử dụng hai bộ dữ liệu có bản chất rất khác nhau. Điểm chung duy nhất giữa chúng là **tỉnh**, nên tỉnh được dùng làm khóa để ghép hai bộ.

| | Bộ 1: Điểm thi tốt nghiệp THPT 2026 | Bộ 2: Niên giám thống kê 2025 |
|---|---|---|
| Nguồn | Dữ liệu chia sẻ công khai trên GitHub, thu thập từ trang tra cứu điểm ngày 01/07/2026 | Cục Thống kê (nso.gov.vn), phần phụ lục 34 tỉnh, thành phố |
| Dạng | 34 file CSV, mỗi tỉnh một file | 1 file PDF, 1.557 trang |
| Quy mô | 1.200.202 thí sinh, khoảng 115 MB | Dùng 15 bảng, lấy ra 24 chỉ tiêu |
| Mỗi dòng là | Một thí sinh | Một tỉnh |
| Nội dung | Mã tỉnh, điểm 11 môn thi | Thu nhập, mức sống, đô thị hóa, giáo dục… |
| Dùng để đo | Kết quả thi của từng tỉnh | Điều kiện kinh tế – xã hội của từng tỉnh |

### Bộ 1: Điểm thi tốt nghiệp THPT 2026

Mỗi dòng ứng với một thí sinh, gồm số báo danh, mã tỉnh, tên tỉnh và điểm các môn:
- 2 môn bắt buộc: Toán, Ngữ văn.
- 9 môn tự chọn (mỗi thí sinh chọn 2): Ngoại ngữ, Vật lí, Hóa học, Sinh học, Lịch sử, Địa lí, Giáo dục kinh tế và pháp luật, Tin học, Công nghệ.

Đây là dữ liệu cá nhân. Nhóm xóa số báo danh ngay ở bước làm sạch, không công bố dữ liệu cấp thí sinh, và chỉ sử dụng số liệu tổng hợp theo tỉnh.

### Bộ 2: Niên giám thống kê 2025

Từ phần phụ lục số liệu 34 tỉnh, thành phố, nhóm lấy 15 bảng, xếp thành 4 nhóm chỉ tiêu tương ứng với câu hỏi nghiên cứu:

| Nhóm | Chỉ tiêu | Dùng để đo |
|---|---|---|
| 1. Thu nhập và mức sống | Thu nhập bình quân đầu người/tháng; thu nhập bình quân một lao động; GRDP bình quân đầu người 2020–2025; chỉ số phát triển con người (HDI); tỷ lệ hộ nghèo; hệ số GINI | Tỉnh giàu hay nghèo |
| 2. Đô thị hóa và dân số | Dân số; dân số thành thị (tính ra tỷ lệ đô thị hóa); diện tích; mật độ dân số | Tỉnh thành thị hay nông thôn |
| 3. Điều kiện giáo dục | Số trường, số giáo viên, số học sinh THPT (tính ra số học sinh trên một giáo viên); tỷ lệ lao động đã qua đào tạo | Trường lớp và trình độ dân cư |
| 4. Tiếp cận thông tin | Tỷ lệ người sử dụng internet | Mức tiếp cận công nghệ |

Khi phân tích, nhóm dùng **8 chỉ tiêu chính**: thu nhập bình quân đầu người, HDI, GRDP bình quân đầu người, tỷ lệ hộ nghèo, tỷ lệ đô thị hóa, tỷ lệ lao động qua đào tạo, số học sinh trên một giáo viên THPT và tỷ lệ sử dụng internet. Các chỉ tiêu còn lại dùng để tính ra các tỷ lệ, hoặc để kiểm tra độ chính xác khi trích số liệu: tổng của 34 tỉnh phải bằng đúng dòng "Cả nước" trong Niên giám.

Nhóm không lấy toàn bộ 209 bảng của phụ lục. Chỉ có 34 tỉnh để phân tích, nên dùng quá nhiều chỉ tiêu sẽ khiến mô hình "học thuộc" dữ liệu thay vì tìm ra quy luật chung.

## D. Lời nói mẫu khi thuyết trình (khoảng 30 giây)

> "Để trả lời hai câu hỏi đó, nhóm em sử dụng hai bộ dữ liệu.
>
> **Bộ thứ nhất** là điểm thi tốt nghiệp THPT 2026 của từng thí sinh, hơn 1,2 triệu bạn trên 34 tỉnh. Mỗi dòng gồm mã tỉnh và điểm các môn thi. Vì đây là dữ liệu cá nhân, nhóm đã xóa số báo danh và chỉ dùng số liệu tổng hợp theo tỉnh.
>
> **Bộ thứ hai** là Niên giám thống kê 2025 của Cục Thống kê. Từ đó nhóm lấy số liệu của 34 tỉnh theo ba nhóm chính:
> - **thu nhập và mức sống**, như thu nhập bình quân đầu người, HDI, tỷ lệ hộ nghèo;
> - **đô thị hóa**, tức tỷ lệ dân sống ở thành thị;
> - **điều kiện giáo dục**, như số học sinh trên một giáo viên THPT và tỷ lệ lao động đã qua đào tạo.
>
> Hai bộ dữ liệu rất khác nhau, một bên là bảng dữ liệu lớn, một bên là sách PDF. Điểm chung duy nhất giữa chúng là tỉnh, và việc ghép chúng lại không hề đơn giản, phần tiếp theo nhóm sẽ trình bày."

**Nếu thầy hỏi "vì sao không lấy hết 209 bảng?":**

> "Nhóm chỉ lấy những chỉ tiêu trả lời trực tiếp câu hỏi nghiên cứu. Chỉ có 34 tỉnh, nên lấy quá nhiều chỉ tiêu thì mô hình dễ học thuộc dữ liệu thay vì tìm ra quy luật."

---

# Tích hợp dữ liệu

Phần E dùng cho báo cáo (chương 3). Phần F là lời nói mẫu khi thuyết trình, nói ngay sau phần dữ liệu.
Số liệu: `data/processed/spark/chat_luong_du_lieu.csv`, `co_diem_theo_mon.csv`, `doi_chieu_pandas.csv`; hình H3.1.

## E. Đoạn tích hợp dữ liệu cho báo cáo

Phần này gồm hai bước: **E.1 làm sạch** từng nguồn, rồi **E.2 ghép** hai nguồn thành một bảng chung.

### E.1. Làm sạch dữ liệu
Ghép hai bộ dữ liệu theo tỉnh nghe đơn giản, nhưng nhóm gặp 5 vấn đề. Phần lớn trong số đó **không gây ra lỗi nào khi chạy chương trình**: nếu không kiểm tra kỹ, kết quả vẫn ra nhưng sai. Mỗi vấn đề dưới đây được trình bày theo ba bước: vấn đề gặp phải, giải pháp và kết quả.

#### Vấn đề 1: Điểm thi bị "giấu" trong một cột văn bản

**1. Vấn đề gặp phải**

Ở 14 tỉnh, trong đó có TP.HCM, Hải Phòng, Đồng Nai, Cần Thơ, An Giang và Huế, các cột điểm Toán, Văn, Ngoại ngữ… đều trống. Toàn bộ điểm bị dồn vào một cột phụ tên `extra`, dưới dạng chuỗi chữ mã hóa kiểu trang web:

```
To&#xE1;n=8; V&#x103;n=7; S&#x1EED;=9      (nghĩa là: Toán=8; Văn=7; Sử=9)
```

Môn Giáo dục kinh tế và pháp luật **chỉ** nằm trong cột này ở cả 34 tỉnh. Nếu đọc thẳng các cột điểm, chỉ 39,3% thí sinh có điểm Toán. Kết quả này sai, vì gần như ai cũng thi Toán.

**2. Giải pháp**

- Giải mã chuỗi về tiếng Việt bình thường: `To&#xE1;n` thành `Toán`.
- Tách chuỗi thành từng cặp "môn = điểm".
- Điền điểm vào đúng cột môn. Ô nào đã có điểm thì giữ nguyên, ô trống thì lấy điểm từ `extra`.

**3. Kết quả**

| Môn | Trước | Sau |
|---|---|---|
| Toán | 39,3% | **98,6%** |
| Ngữ văn | 39,6% | **99,0%** |
| GD kinh tế và pháp luật | 0% | **23,4%** |

96,4% thí sinh có đủ 4 môn, đúng với cấu trúc thi mới. Sinh học và Tin học không bao giờ nằm trong `extra`, nên tỷ lệ có điểm hai môn này không đổi; nhóm đã kiểm tra là không bị mất dữ liệu (hình H3.1).

#### Vấn đề 2: Môn thi thay đổi theo chương trình mới

**1. Vấn đề gặp phải**

Dữ liệu còn cột của môn cũ Giáo dục công dân, gần như trống, trong khi môn mới Giáo dục kinh tế và pháp luật lại không có cột riêng. Môn Công nghệ được ghi thành hai tên khác nhau: "công nghệ công nghiệp" và "công nghệ nông nghiệp".

**2. Giải pháp**

- Đổi tên cột Giáo dục công dân thành Giáo dục kinh tế và pháp luật.
- Gộp hai phân môn Công nghệ làm một.
- Chuẩn hóa về một danh sách 11 môn thống nhất.

**3. Kết quả**

Cả 34 tỉnh dùng chung một danh sách 11 môn: Toán, Ngữ văn, Ngoại ngữ, Vật lí, Hóa học, Sinh học, Lịch sử, Địa lí, GD kinh tế và pháp luật, Tin học, Công nghệ. So sánh giữa các tỉnh là so cùng một môn.

#### Vấn đề 3: Mã tỉnh cũ bị dùng lại cho tỉnh khác

**1. Vấn đề gặp phải**

Sau sắp xếp, 63 tỉnh còn 34. Có **7 mã số cũ nay trỏ sang một tỉnh khác hẳn**:

| Mã | Trước 01/07/2025 | Nay |
|---|---|---|
| 15 | Yên Bái | Lào Cai |
| 24 | Bắc Giang | Bắc Ninh |
| 44 | Quảng Bình | Quảng Trị |
| 52 | Bình Định | Gia Lai |
| 80 | Long An | Tây Ninh |
| 82 | Tiền Giang | Đồng Tháp |
| 91 | Kiên Giang | An Giang |

Nếu ghép số liệu cũ theo mã số, số liệu của Bình Định sẽ bị gán nhầm cho Gia Lai mà **không có thông báo lỗi nào**. Tên tỉnh giữa hai nguồn cũng lệch nhau, ví dụ "TP. Hồ Chí Minh" và "Hồ Chí Minh".

**2. Giải pháp**

- Tự xây bảng ánh xạ 63 tỉnh cũ sang 34 tỉnh mới theo Nghị quyết 202/2025/QH15.
- Chỉ dùng **mã tỉnh mới** làm khóa để ghép, không ghép theo tên.
- Chuẩn hóa tên tỉnh, ví dụ bỏ tiền tố "TP.".

**3. Kết quả**

34 mã tỉnh mới khớp 100% với mã tỉnh nằm trong số báo danh của thí sinh. Ghép hai nguồn được đủ **34 / 34 tỉnh**, không tỉnh nào bị gán nhầm.

#### Vấn đề 4: Số liệu kinh tế – xã hội nằm trong file PDF

**1. Vấn đề gặp phải**

Niên giám không có bản Excel, chỉ có file PDF 1.557 trang. Lấy số liệu từ bảng trong PDF gặp các khó khăn:
- **Số viết kiểu Việt Nam:** `1.234,5` (dấu chấm phân cách nghìn, dấu phẩy thập phân). Dấu `-` hoặc `..` nghĩa là không có số liệu.
- **Ô trống làm lệch cột.** Khi một ô không có số, các số phía sau bị dồn sang trái và rơi nhầm vào cột khác.
- **Mỗi bảng trải trên 2 trang** với lề khác nhau, và có các trang mục lục trùng tiêu đề với bảng.

**2. Giải pháp**

- Chuyển số kiểu Việt Nam sang dạng số máy tính hiểu được; coi `-` và `..` là "không có số liệu".
- Xác định cột dựa trên **vị trí của từng con số trên trang**, không dựa trên thứ tự, lấy các dòng đầy đủ số làm mốc.
- Xử lý riêng từng trang để chịu được lề khác nhau, bỏ qua các trang mục lục.

**3. Kết quả**

Trích được 24 chỉ tiêu cho 34 tỉnh. Cộng số liệu 34 tỉnh, so với dòng "Cả nước" có sẵn trong Niên giám, **khớp chính xác**: dân số 102.345,3 nghìn người, giáo viên THPT 148.396, học sinh THPT 3.082.574.

#### Vấn đề 5: Lỗi "im lặng" khó phát hiện

**1. Vấn đề gặp phải**

Bốn vấn đề trên đều không làm chương trình báo lỗi. Ngoài ra có những hiện tượng trông giống lỗi nhưng không phải: nhiều môn có điểm lẻ như 6,1 hay 7,35, không phải bội số của 0,25. Nếu không kiểm tra, nhóm có thể sửa nhầm dữ liệu đúng, hoặc bỏ sót dữ liệu sai.

**2. Giải pháp**

Kiểm tra kết quả bằng nhiều cách độc lập. Quan trọng nhất là **làm lại toàn bộ bằng hai công cụ khác nhau** (Spark và pandas) rồi so sánh. Với điểm lẻ, nhóm tìm hiểu và xác nhận đây là do đề trắc nghiệm mới có phần đúng/sai và trả lời ngắn, nên giữ nguyên.

**3. Kết quả**

| Kiểm tra | Kết quả |
|---|---|
| Cộng 34 tỉnh, so với dòng "Cả nước" trong Niên giám | Khớp chính xác |
| Số báo danh trùng lặp | Không có (1.200.202 / 1.200.202) |
| Mã tỉnh trong số báo danh so với cột mã tỉnh | Khớp 100% |
| Điểm nằm ngoài khoảng 0–10 | Không có |
| Thí sinh không có điểm môn nào | Không có |
| Ghép hai nguồn theo tỉnh | 34 / 34 tỉnh |
| Spark so với pandas | Khớp 60 / 60 cột số liệu |

#### Tóm tắt E.1

| # | Vấn đề | Giải pháp | Kết quả |
|---|---|---|---|
| 1 | Điểm bị giấu trong cột `extra` | Giải mã, tách, điền vào đúng cột | Có điểm Toán: 39,3% → 98,6% |
| 2 | Môn thi thay đổi | Đổi tên, gộp, chuẩn hóa 11 môn | 34 tỉnh dùng chung danh sách môn |
| 3 | Mã tỉnh cũ bị dùng lại | Bảng ánh xạ 63 → 34, ghép theo mã mới | 34 / 34 tỉnh, không gán nhầm |
| 4 | Số liệu nằm trong PDF | Đọc số theo vị trí trên trang | Tổng 34 tỉnh = số cả nước |
| 5 | Lỗi im lặng | Kiểm tra chéo bằng 2 công cụ | Khớp 60 / 60 cột |

### E.2. Ghép dữ liệu

Sau E.1, mỗi nguồn đã sạch và đúng, nhưng **hai nguồn vẫn nằm riêng**, chưa thể đặt cạnh nhau để so sánh. Phần này trình bày cách ghép chúng thành một bảng chung.

| | Làm sạch (E.1) | Ghép dữ liệu (E.2) |
|---|---|---|
| Làm với | Từng nguồn riêng lẻ | Hai nguồn cùng lúc |
| Câu hỏi | Dữ liệu trong nguồn này đúng chưa? | Nối hai nguồn lại bằng cách nào? |

Toàn bộ quy trình ghép:

```
NGUỒN 1: Điểm thi (đã làm sạch)              NGUỒN 2: Niên giám 2025 (đã trích từ PDF)
1.200.202 dòng, mỗi dòng 1 thí sinh           34 dòng, mỗi dòng 1 tỉnh
        │                                             │
        │ Bước 1. Gom về cấp tỉnh                     │ Bước 3. Thống nhất tên cột, đơn vị
        ▼                                             ▼
34 tỉnh × 17 chỉ số điểm thi                   34 tỉnh × 24 chỉ tiêu
        │                                             │
        └──────── Bước 2 + 4. Ghép theo MÃ TỈNH ───────┘
                               ▼
              BẢNG CHUNG: 34 dòng × 43 cột
       mỗi tỉnh vừa có điểm thi, vừa có số liệu KT-XH
                               │
                     Bước 5. Kiểm tra sau ghép
```

#### Bước 1: Đưa hai nguồn về cùng một cấp độ

**1. Vấn đề gặp phải**

Hai nguồn mô tả hai thứ khác nhau. Nguồn 1 có 1.200.202 dòng, **mỗi dòng là một thí sinh**. Nguồn 2 có 34 dòng, **mỗi dòng là một tỉnh**. Không thể nối từng thí sinh với "thu nhập của thí sinh đó", vì Niên giám không có số liệu cho từng người.

**2. Giải pháp**

Dùng Apache Spark gom điểm của tất cả thí sinh trong cùng một tỉnh lại, tính ra các chỉ số đại diện cho tỉnh:
- số thí sinh;
- điểm trung bình Toán, Văn, Ngoại ngữ và điểm trung bình chung;
- điểm Toán trung vị, tỷ lệ thí sinh dưới 5 điểm Toán và từ 8 điểm trở lên;
- tỷ lệ thí sinh chọn từng môn tự chọn.

**3. Kết quả**

1.200.202 dòng thí sinh trở thành **34 dòng, mỗi dòng một tỉnh, 17 chỉ số điểm thi**. Hai nguồn giờ có cùng cấp độ: mỗi dòng là một tỉnh.

#### Bước 2: Chọn "chìa khóa" để ghép

**1. Vấn đề gặp phải**

Muốn ghép hai bảng, cần một cột chung để biết dòng nào của bảng này ứng với dòng nào của bảng kia. Ứng viên tự nhiên là tỉnh, nhưng tên tỉnh lệch nhau giữa hai nguồn ("TP. Hồ Chí Minh" và "Hồ Chí Minh"), và có 7 mã tỉnh cũ bị dùng lại cho tỉnh khác (xem Vấn đề 3, mục E.1).

**2. Giải pháp**

- Chọn **mã tỉnh mới (2 chữ số)** theo Nghị quyết 202/2025/QH15 làm chìa khóa duy nhất, không ghép theo tên.
- Với dữ liệu điểm thi, mã tỉnh lấy từ 2 chữ số đầu của số báo danh.
- Với Niên giám, gán mã tỉnh mới cho từng dòng nhờ bảng ánh xạ 63 → 34 tỉnh.

**3. Kết quả**

Mỗi tỉnh có đúng một mã, giống nhau ở cả hai nguồn. 34 mã của hai bảng trùng khớp hoàn toàn.

#### Bước 3: Thống nhất tên cột và đơn vị

**1. Vấn đề gặp phải**

Mỗi bảng trong Niên giám dùng đơn vị riêng: nghìn người, nghìn đồng, phần trăm, triệu đồng. Một số chỉ tiêu cần dùng không có sẵn mà phải tự tính. Chẳng hạn Niên giám chỉ cho số dân thành thị, không cho tỷ lệ đô thị hóa.

**2. Giải pháp**

- Đặt tên cột thống nhất, có ghi đơn vị.
- Tính các chỉ tiêu dẫn xuất: **tỷ lệ đô thị hóa** = dân số thành thị / tổng dân số; số học sinh THPT trên 1.000 dân.
- Niên giám 2025 đã có sẵn số liệu cho đúng 34 tỉnh mới, nên nhóm không phải tự gộp từ 63 tỉnh cũ. Nếu phải gộp (ví dụ khi dùng số liệu các năm trước), chỉ tiêu dạng tổng như dân số thì cộng lại, còn chỉ tiêu bình quân như thu nhập bình quân thì phải tính lại theo trọng số dân số, không được lấy trung bình cộng.

**3. Kết quả**

Một bảng Niên giám gọn gàng: **34 dòng × 24 chỉ tiêu**, mỗi cột một ý nghĩa và một đơn vị rõ ràng.

#### Bước 4: Ghép hai bảng theo mã tỉnh

**1. Vấn đề gặp phải**

Có hai bảng cùng 34 dòng, cùng chìa khóa mã tỉnh, nhưng vẫn đang tách rời. Muốn trả lời "tỉnh giàu hơn có điểm cao hơn không", cần đặt điểm thi và thu nhập của cùng một tỉnh **trên cùng một dòng**.

**2. Giải pháp**

Nối hai bảng theo mã tỉnh: dòng có mã `01` của bảng điểm thi được nối với dòng có mã `01` của bảng Niên giám, và tương tự với 33 tỉnh còn lại. Phép ghép được cài đặt để báo lỗi ngay nếu một mã tỉnh xuất hiện hai lần hoặc chỉ có ở một bên.

**3. Kết quả**

**Bảng chung 34 dòng × 43 cột.** Ví dụ ba dòng:

| Mã | Tỉnh | Thu nhập BQ (nghìn đ/tháng) | HDI | Tỷ lệ đô thị | HS/GV THPT | Số thí sinh | Toán TB | Văn TB | Tỷ lệ thi Ngoại ngữ |
|---|---|---|---|---|---|---|---|---|---|
| 01 | Hà Nội | 8.374 | 0,84 | 47,8% | 24 | 125.419 | 6,17 | 7,02 | 47% |
| 79 | Hồ Chí Minh | 8.064 | 0,83 | 77,1% | 20 | 139.114 | 6,19 | 6,59 | 46% |
| 11 | Điện Biên | 2.583 | 0,66 | 13,9% | 17 | 7.947 | 4,46 | 6,32 | 8% |

Các cột thu nhập, HDI, tỷ lệ đô thị, HS/GV đến từ Niên giám; các cột số thí sinh, điểm TB và tỷ lệ thi Ngoại ngữ đến từ dữ liệu điểm thi. Đây là bảng dùng cho toàn bộ phần phân tích ở chương sau.

#### Bước 5: Kiểm tra sau khi ghép

**1. Vấn đề gặp phải**

Phép ghép có thể "lặng lẽ" làm mất hoặc nhân đôi dữ liệu: một tỉnh có mã viết khác, ví dụ `1` và `01`, sẽ bị rơi mất mà không báo lỗi.

**2. Giải pháp**

Kiểm tra bảng chung ngay sau khi ghép, và làm lại toàn bộ quy trình bằng hai công cụ khác nhau (xem Vấn đề 5, mục E.1).

**3. Kết quả**

| Kiểm tra | Kết quả |
|---|---|
| Số tỉnh ghép được | 34 / 34, không tỉnh nào bị mất hay trùng |
| Ô trống trong bảng chung | Không có |
| Kết quả Spark so với kết quả pandas | Khớp 60 / 60 cột số liệu |

#### Tóm tắt E.2

| Bước | Vấn đề | Giải pháp | Kết quả |
|---|---|---|---|
| 1. Cùng cấp độ | Thí sinh và tỉnh | Spark gom 1,2 triệu thí sinh theo tỉnh | 34 dòng × 17 chỉ số điểm |
| 2. Cùng chìa khóa | Tên lệch, mã tỉnh bị dùng lại | Ghép theo mã tỉnh mới | 34 mã khớp hoàn toàn |
| 3. Cùng đơn vị | Đơn vị khác nhau, thiếu tỷ lệ | Chuẩn hóa, tự tính tỷ lệ | 34 × 24 chỉ tiêu |
| 4. Ghép | Hai bảng tách rời | Nối theo mã tỉnh | Bảng chung 34 × 43 cột |
| 5. Kiểm tra | Lỗi im lặng khi ghép | Kiểm tra ngay + kiểm tra chéo | 34/34 tỉnh, khớp 60/60 cột |

## F. Lời nói mẫu khi thuyết trình (khoảng 60 giây, chiếu hình H4.1 hoặc sơ đồ quy trình ở trên)

> "Phần tiếp theo là làm sao ghép hai bộ dữ liệu lại với nhau. Nhóm chia làm hai việc: **làm sạch** từng nguồn, rồi mới **tích hợp** hai nguồn.
>
> **Về làm sạch**, vấn đề lớn nhất là điểm thi bị giấu. Ở 14 tỉnh, trong đó có TP.HCM, điểm bị dồn vào một cột chữ mã hóa. Đọc thẳng thì chỉ 39% thí sinh có điểm Toán; sau khi giải mã thì lên 98,6%. Còn số liệu kinh tế nằm trong file PDF, chỉ cần một ô trống là cả hàng số lệch cột, nên nhóm phải đọc số theo vị trí trên trang.
>
> **Về tích hợp**, khó khăn đầu tiên là hai nguồn không cùng cấp độ: một bên là 1,2 triệu thí sinh, một bên là 34 tỉnh. Nên nhóm dùng Spark gom điểm của từng tỉnh lại, ra 34 dòng.
>
> Khó khăn thứ hai là chìa khóa để ghép. Sau sáp nhập có 7 mã tỉnh cũ nay thuộc về tỉnh khác, ví dụ mã 52 trước là Bình Định, nay là Gia Lai. Ghép không cẩn thận thì số liệu tỉnh này gán sang tỉnh kia mà máy không báo gì. Nhóm tự xây bảng chuyển đổi 63 sang 34 tỉnh và chỉ ghép theo mã tỉnh mới.
>
> Kết quả là **một bảng chung 34 dòng**, mỗi tỉnh vừa có điểm thi, vừa có thu nhập, mức sống, đô thị hóa. Nhóm kiểm tra lại: đủ 34 trên 34 tỉnh, cộng lại khớp số cả nước, và làm lại bằng hai công cụ khác nhau thì kết quả trùng khớp hoàn toàn."

**Nếu thầy hỏi "tích hợp khác làm sạch ở chỗ nào?":**

> "Làm sạch là sửa lỗi bên trong từng nguồn, ví dụ lấy điểm bị giấu ra. Tích hợp là đưa hai nguồn khác nhau về cùng cấp độ, cùng chìa khóa, cùng đơn vị, rồi nối lại thành một bảng. Phải làm sạch trước, vì ghép hai nguồn còn lỗi thì chỉ ra một bảng lỗi lớn hơn."

**Nếu thầy hỏi "làm sao biết số liệu trích từ PDF là đúng?":**

> "Niên giám có sẵn dòng 'Cả nước'. Nhóm cộng số liệu của 34 tỉnh vừa trích ra và so với dòng đó. Dân số, số giáo viên và số học sinh THPT đều khớp đến từng đơn vị. Nếu có ô nào bị lệch cột thì tổng sẽ sai ngay."
