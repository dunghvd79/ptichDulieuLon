# Nội dung báo cáo và thuyết trình: Đặt vấn đề → Dữ liệu → Tích hợp → Pipeline → Kết quả → Thảo luận, Kết luận

Phần A, C, E, G, I, K dùng cho báo cáo (chương 1–7 và tài liệu tham khảo). Phần B, D, F, H, J, L là lời nói mẫu khi thuyết trình.
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

> "Nhóm lấy thu nhập để dự đoán điểm Toán của từng tỉnh, nhưng mỗi lần đều giấu đi một vài tỉnh, xây công thức trên các tỉnh còn lại rồi đoán thử các tỉnh bị giấu. Cách đoán này giải thích được khoảng 65% sự chênh lệch điểm Toán giữa các tỉnh; sai số trung bình giảm từ 0,5 điểm (khi đoán mọi tỉnh bằng điểm trung bình cả nước) xuống còn 0,3 điểm. Làm vậy để chắc rằng công thức đoán được cả những tỉnh nó chưa từng thấy, chứ không chỉ khớp với dữ liệu đã có."

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

Trước khi ghép được hai bộ dữ liệu, nhóm gặp 5 vấn đề. Phần lớn trong số đó **không gây ra lỗi nào khi chạy chương trình**: nếu không kiểm tra kỹ, kết quả vẫn ra nhưng sai. Mỗi vấn đề dưới đây được trình bày theo ba bước: vấn đề gặp phải, giải pháp và kết quả.

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

---

# Pipeline xử lý bằng Apache Spark

Phần G dùng cho báo cáo (chương 4). Phần H là lời nói mẫu khi thuyết trình, chiếu hình H4.1.
Số liệu: `data/processed/spark/thoi_gian_chay.csv`, `doi_chieu_pandas.csv`; mã nguồn trong `spark/`.

## G. Đoạn pipeline cho báo cáo

### G.1. Vì sao dùng Apache Spark

**Apache Spark** là công cụ xử lý dữ liệu lớn. Ý tưởng cốt lõi: thay vì một người làm từ đầu đến cuối, Spark **chia dữ liệu thành nhiều phần và giao cho nhiều "người" làm cùng lúc**, rồi gộp kết quả lại.

> Ví dụ: chấm 1,2 triệu bài thi. Một giám khảo chấm lần lượt từng bài sẽ rất lâu. Chia thành 8 chồng, giao cho 8 giám khảo chấm song song, rồi cộng kết quả, sẽ nhanh hơn nhiều. Spark làm đúng việc chia chồng, giao việc và cộng kết quả đó một cách tự động.

Trong đồ án, "người làm" là các nhân CPU. Máy chạy đồ án có 8 nhân, nên Spark chia dữ liệu thành 8 phần xử lý song song.

**Một điều cần nói thẳng:** 1,2 triệu dòng (khoảng 115 MB) chưa phải là "dữ liệu lớn" theo nghĩa chặt. Công cụ thông thường như pandas vẫn xử lý được trên một máy. Nhóm chọn Spark vì:
- **Mở rộng được:** cùng một đoạn mã, nếu dữ liệu tăng lên nhiều năm thi hoặc cả điểm từng câu hỏi, chỉ cần chạy trên một cụm nhiều máy, không phải viết lại.
- **Yêu cầu của môn học:** thể hiện được việc dùng công cụ dữ liệu lớn cho cả xử lý (Spark SQL / DataFrame) và học máy (Spark MLlib).
- **Kiểm chứng chéo:** có sẵn bản xử lý bằng pandas, nên nhóm so sánh được hai cách làm độc lập (mục G.4).

Spark trong đồ án chạy ở **chế độ local** (một máy, 8 nhân), phiên bản PySpark 4.0.

### G.2. Năm bước của pipeline

Pipeline có 5 bước, khớp với hình H4.1. Ba bước đầu đi theo cách tổ chức dữ liệu phổ biến gồm ba tầng **Bronze → Silver → Gold**: dữ liệu thô → dữ liệu đã làm sạch → dữ liệu đã tổng hợp, tầng sau "tinh" hơn tầng trước.

| Bước | Tầng | Làm gì | Tính năng Spark dùng | Kết quả | Thời gian |
|---|---|---|---|---|---|
| 1. Đọc | Bronze | Đọc 34 file CSV, giữ nguyên mọi giá trị dạng chữ | Đọc nhiều file song song | 1.200.202 dòng, chia 8 phần | 8 giây |
| 2. Làm sạch | Silver | Giải mã cột `extra`, chuẩn hóa 11 môn, xóa số báo danh | pandas UDF (xử lý theo lô) | 1.200.202 thí sinh, có điểm Toán 98,6% | 16 giây |
| 3. Tổng hợp | Gold | Gom theo tỉnh, theo tỉnh × môn; tính phổ điểm, eta², tổ hợp môn | groupBy, unpivot, window | 34 tỉnh × 11 môn, 8 bảng tổng hợp | 19 giây |
| 4. Ghép | — | Nối bảng điểm thi với bảng Niên giám theo mã tỉnh | join | Bảng chung 34 × 43 | 3 giây |
| 5. Phân tích | — | Hồi quy, phân cụm tỉnh | Spark MLlib | Trả lời 2 câu hỏi nghiên cứu | khoảng 4 phút |

Toàn bộ bước 1–4 chạy trong **khoảng 1 phút**, kể cả 6 giây khởi động Spark. Bước 5 lâu hơn vì mỗi mô hình được huấn luyện lại 25 lần để kiểm tra độ tin cậy (5 phần × 5 lần lặp).

#### Ba kỹ thuật Spark quan trọng, giải thích đơn giản

**a) Chia nhỏ dữ liệu (partition)**

Spark chia 1,2 triệu dòng thành 8 phần, mỗi nhân CPU xử lý một phần. Đây là lý do Spark nhanh hơn khi dữ liệu lớn: thêm máy, thêm nhân là thêm "người làm".

**b) Làm sau, tính trước (lazy evaluation)**

Khi viết lệnh "đọc file → giải mã → gom theo tỉnh", Spark **chưa làm ngay** mà chỉ ghi lại "công thức". Đến khi thật sự cần kết quả, ví dụ xuất ra file, Spark mới xem toàn bộ công thức, tìm cách làm hiệu quả nhất rồi chạy một lần.

> Ví dụ: đi chợ. Thay vì nhớ ra món nào chạy đi mua món đó, ta ghi hết danh sách rồi mới đi, sắp xếp đường đi hợp lý và mua một lượt.

Nhóm cũng **giữ dữ liệu đã làm sạch trong bộ nhớ** (cache), để bước tổng hợp dùng lại nhiều lần mà không phải đọc và giải mã lại từ đầu.

**c) Xử lý theo lô bằng pandas UDF**

Giải mã cột `extra` cần một hàm viết riêng bằng Python. Nếu gọi hàm đó cho từng dòng, 1,2 triệu lần, thì rất chậm. Nhóm dùng **pandas UDF**: Spark gửi dữ liệu sang Python theo **từng lô khoảng 10.000 dòng** qua định dạng Apache Arrow, Python xử lý cả lô một lần rồi trả về.

> Ví dụ: chuyển hàng bằng xe tải thay vì cầm từng món một.

#### Bước 5: Phân tích bằng Spark MLlib

MLlib là thư viện học máy của Spark. Nhóm dùng hai việc:
- **Hồi quy tuyến tính:** tìm xem thu nhập, đô thị hóa, điều kiện giáo dục giải thích được bao nhiêu phần chênh lệch điểm thi giữa các tỉnh. Các chỉ tiêu được đưa về cùng thang đo trước khi đưa vào mô hình. Ví dụ thu nhập tính bằng nghìn đồng còn HDI chỉ từ 0 đến 1; không đưa về cùng thang thì không so sánh được.
- **Phân cụm KMeans:** tự động chia 34 tỉnh thành các nhóm có đặc điểm giống nhau.

Chi tiết kết quả ở chương 5.

### G.3. Khó khăn khi cài đặt Spark trên Windows

Spark được thiết kế chủ yếu cho Linux. Chạy trên Windows, nhóm gặp 7 lỗi. Phần lớn lỗi **không báo nguyên nhân rõ ràng**: chương trình treo hoặc dừng với thông báo chung chung.

| Hiện tượng | Nguyên nhân | Cách xử lý |
|---|---|---|
| Không khởi động được, báo không tìm thấy Python | Thư mục dự án có dấu cách (`2026 Year`) | Cài môi trường Python ở thư mục không có dấu cách |
| Mọi hàm Python tự viết đều bị dừng đột ngột | Python 3.12 chưa tương thích với Spark trên Windows | Dùng Python 3.11 |
| Kết nối nội bộ chậm, sai địa chỉ | Docker Desktop thay đổi cấu hình mạng của máy | Ép Spark dùng địa chỉ nội bộ 127.0.0.1 |
| Treo không báo lỗi khi đọc `*.csv` | Spark cần một công cụ phụ (winutils) để tìm file theo mẫu trên Windows | Truyền danh sách 34 file cụ thể |
| Báo không tìm thấy file | Đường dẫn có dấu cách bị mã hóa hai lần | Đổi cách viết đường dẫn |
| Hàm Python không tìm thấy mã nguồn dùng chung | Tiến trình con của Spark không biết thư mục `scripts/` | Khai báo đường dẫn trước khi khởi động Spark |
| Một chỉ số tổng ra rỗng | Cộng các ô trống làm cả tổng thành rỗng | Coi ô trống là 0 khi đếm |

Toàn bộ cách xử lý được đóng gói vào một file dùng chung (`spark/_session.py`), nên các bước sau chỉ cần gọi một lệnh là có Spark chạy đúng.

### G.4. Kiểm chứng và hiệu năng

**Kiểm chứng:** cùng dữ liệu, nhóm xử lý bằng hai chương trình độc lập, một bằng Spark và một bằng pandas, rồi so từng con số. Kết quả **khớp 60 / 60 cột**, sai số dưới 0,001. Nếu một trong hai bên có lỗi logic thì kết quả sẽ lệch.

**Thời gian chạy từng bước** (máy 8 nhân, chế độ local):

| Bước | Thời gian |
|---|---|
| Khởi động Spark | 6 giây |
| 1. Đọc 34 file | 8 giây |
| 2. Làm sạch | 16 giây |
| 3. Tổng hợp | 19 giây |
| 4. Ghép | 3 giây |
| **Tổng bước 1–4** | **khoảng 52 giây** |
| 5. Phân tích (MLlib) | khoảng 4 phút |

Với lượng dữ liệu nhỏ như hiện tại, một phần đáng kể thời gian là chi phí cố định: khởi động Spark (6 giây) và chia, gộp việc giữa các nhân. Lợi thế của Spark thể hiện rõ khi dữ liệu lớn hơn nhiều lần, lúc một máy không còn chứa nổi toàn bộ dữ liệu trong bộ nhớ. Nhóm chưa đo so sánh thời gian chạy giữa Spark và pandas; đây là một hướng bổ sung.

## H. Lời nói mẫu khi thuyết trình (khoảng 60 giây, chiếu hình H4.1)

> "Để xử lý dữ liệu, nhóm dùng **Apache Spark**, một công cụ xử lý dữ liệu lớn. Ý tưởng của Spark giống như chấm 1,2 triệu bài thi: thay vì một giám khảo chấm lần lượt, ta chia thành 8 chồng, giao cho 8 giám khảo chấm cùng lúc rồi cộng kết quả. Máy của nhóm có 8 nhân, nên Spark chia dữ liệu làm 8 phần chạy song song.
>
> Pipeline gồm 5 bước như trên hình. **Bước 1, đọc** 34 file điểm thi. **Bước 2, làm sạch**: lấy điểm bị giấu ra và xóa số báo danh. **Bước 3, tổng hợp** điểm theo từng tỉnh. **Bước 4, ghép** với số liệu Niên giám theo mã tỉnh. **Bước 5, phân tích** bằng thư viện học máy MLlib của Spark. Bốn bước đầu chạy hết khoảng một phút.
>
> Để chắc chắn kết quả đúng, nhóm làm lại toàn bộ bằng một công cụ khác là pandas, và hai bên khớp nhau 60 trên 60 cột số liệu.
>
> Nhóm cũng xin nói thẳng: 1,2 triệu dòng chưa thật sự là dữ liệu quá lớn. Nhóm chọn Spark vì cùng một đoạn mã có thể chạy trên nhiều máy khi dữ liệu tăng lên, ví dụ gộp nhiều năm thi, mà không phải viết lại."

**Nếu thầy hỏi "115 MB thì sao gọi là dữ liệu lớn?":**

> "Đúng là với dữ liệu hiện tại, pandas trên một máy vẫn chạy được, và nhóm đã dùng pandas để kiểm chứng. Điểm nhấn của đồ án là phần tích hợp nhiều nguồn và một pipeline có thể mở rộng. Nếu thêm điểm các năm trước hoặc điểm từng câu hỏi, dữ liệu sẽ lớn gấp nhiều lần, lúc đó chỉ cần chạy cùng đoạn mã trên một cụm máy."

**Nếu thầy hỏi "Spark chạy trên mấy máy?":**

> "Trong đồ án, Spark chạy ở chế độ local, trên một máy với 8 nhân CPU. Mỗi nhân đóng vai một 'máy con'. Chuyển lên cụm nhiều máy chỉ cần đổi cấu hình, không cần sửa mã xử lý."

**Nếu thầy hỏi "lazy evaluation là gì?":**

> "Spark không làm ngay từng lệnh mà ghi lại toàn bộ công thức, đến khi cần kết quả mới xem cả công thức để tìm cách chạy hiệu quả nhất. Giống như ghi hết danh sách đồ cần mua rồi mới đi chợ một lượt, thay vì nhớ ra món nào chạy đi mua món đó."

**Nếu thầy hỏi "Bronze, Silver, Gold là gì?":**

> "Đó là ba tầng của dữ liệu: Bronze là dữ liệu thô vừa đọc vào, Silver là dữ liệu đã làm sạch, Gold là dữ liệu đã tổng hợp sẵn để phân tích. Tách tầng như vậy thì khi có lỗi, nhóm biết ngay lỗi nằm ở tầng nào."

---

# Kết quả phân tích

Phần I dùng cho báo cáo (chương 5). Phần J là lời nói mẫu khi thuyết trình.
Số liệu: các file `data/processed/spark/ml_*.csv`, `tuong_quan_spearman.csv`, `chenh_lech_giua_tinh_theo_mon.csv`, `van_dinh_5_theo_tinh.csv`; hình H5.1–H5.6.
Mỗi mục viết theo thứ tự: **kết luận bằng lời → số liệu → cách đo**.

## I. Đoạn kết quả cho báo cáo

### I.1. Bức tranh chung về điểm thi 2026

**Kết luận:** Ngữ văn có điểm trung bình cao nhất trong hai môn bắt buộc, Toán thấp hơn và phân tán hơn. Tổ hợp tự chọn phổ biến nhất là Lịch sử + Địa lí.

**Số liệu** (hình H5.1):
- Điểm trung bình toàn quốc: Ngữ văn **6,50**, Toán **5,65**.
- Phổ điểm Toán có **hai đỉnh**, khoảng 4,5 điểm và khoảng 7–7,75 điểm. Điều này cho thấy thí sinh chia thành hai nhóm khá rõ về năng lực Toán. Phổ điểm Văn lệch về phía điểm cao, đỉnh ở 7,0.
- Giữa 34 tỉnh: điểm Toán trung bình dao động từ 4,25 (Sơn La) đến 6,26 (Ninh Bình); điểm Văn từ 5,00 (Vĩnh Long) đến 7,26 (Ninh Bình).

Tổ hợp 2 môn tự chọn, tính trên thí sinh thi đủ 4 môn:

| Tổ hợp | Tỷ lệ |
|---|---|
| Lịch sử + Địa lí | 22,8% |
| Vật lí + Hóa học | 14,5% |
| Ngoại ngữ + Vật lí | 12,2% |
| Lịch sử + GD kinh tế và pháp luật | 10,2% |
| Địa lí + GD kinh tế và pháp luật | 8,8% |
| Ngoại ngữ + Lịch sử | 7,6% |

### I.2. Câu hỏi 1: Mức sống, đô thị hóa, điều kiện giáo dục và điểm thi

#### a) Tương quan: các tỉnh xếp hạng giống nhau đến đâu?

**Kết luận:** Tỉnh có thu nhập cao, HDI cao, ít hộ nghèo thì điểm Toán và tỷ lệ thí sinh chọn thi Ngoại ngữ cao hơn rõ rệt. Điểm Văn chỉ liên quan yếu. Số học sinh trên một giáo viên gần như không liên quan.

**Cách đo: hệ số tương quan Spearman**

*Ý tưởng:* hãy tưởng tượng hai bảng xếp hạng 34 tỉnh, một bảng xếp theo **thu nhập**, một bảng xếp theo **điểm Toán**. Nếu tỉnh đứng đầu bảng này cũng đứng đầu bảng kia, tỉnh đứng cuối cũng đứng cuối, thì hai thứ "đi cùng nhau". Spearman chính là con số đo **hai bảng xếp hạng giống nhau đến đâu**. Nó không quan tâm thu nhập là bao nhiêu tiền hay điểm là bao nhiêu, chỉ quan tâm **thứ hạng**.

*Ví dụ với 5 tỉnh thật:*

| Tỉnh | Thu nhập (nghìn đ/tháng) | Điểm Toán TB | Hạng thu nhập | Hạng Toán | Lệch hạng |
|---|---|---|---|---|---|
| Hà Nội | 8.374 | 6,17 | 1 | 1 | 0 |
| Quảng Ninh | 6.917 | 5,51 | 2 | 3 | 1 |
| Hà Tĩnh | 4.457 | 5,99 | 3 | 2 | 1 |
| Đắk Lắk | 4.421 | 5,14 | 4 | 4 | 0 |
| Điện Biên | 2.583 | 4,46 | 5 | 5 | 0 |

Hai bảng xếp hạng gần như trùng nhau. Chỉ Quảng Ninh và Hà Tĩnh đổi chỗ cho nhau: Quảng Ninh giàu hơn nhưng điểm Toán thấp hơn Hà Tĩnh. Hệ số Spearman của 5 tỉnh này là **0,90**, rất gần 1.

Cách tính: lấy độ lệch hạng của từng tỉnh, bình phương lên rồi cộng lại (ở đây 0 + 1 + 1 + 0 + 0 = 2), sau đó đưa vào công thức

ρ = 1 − 6 × (tổng lệch hạng bình phương) / (n × (n² − 1)) = 1 − 6 × 2 / (5 × 24) = 0,90

với n là số tỉnh. Hai bảng càng lệch nhau thì tổng càng lớn và hệ số càng nhỏ. Trên thực tế, nhóm để máy tính làm việc này cho cả 34 tỉnh.

*Cách đọc con số:* hệ số luôn nằm trong khoảng từ −1 đến 1.

| Giá trị | Ý nghĩa | Ví dụ trong đồ án |
|---|---|---|
| Gần **1** | Hai bảng xếp hạng gần như trùng nhau: tỉnh giàu hơn thì điểm cao hơn | Thu nhập – Toán: 0,76 |
| Gần **0** | Hai bảng không liên quan gì nhau | Học sinh/giáo viên – Toán: 0,15 |
| Gần **−1** | Hai bảng ngược nhau: tỉnh đứng đầu bên này lại đứng cuối bên kia | Hộ nghèo – Toán: −0,77 (tỉnh càng nhiều hộ nghèo, điểm càng thấp) |

Với 34 tỉnh, hệ số cần lớn hơn khoảng **0,34** (dương hay âm đều được) thì mới khó xảy ra do ngẫu nhiên, ở mức tin cậy 95% thường dùng. Dưới mức này, có thể hai thứ chỉ tình cờ trùng nhau.

*Vì sao dùng Spearman mà không so trực tiếp con số?* Thu nhập của Hà Nội và TP.HCM cao vượt trội so với các tỉnh còn lại. Nếu so trực tiếp con số, vài tỉnh này có thể kéo lệch kết quả. Spearman chỉ xét thứ hạng, nên Hà Nội chỉ là "hạng 1" dù giàu hơn hạng 2 bao nhiêu đi nữa; kết quả vì thế công bằng với cả 34 tỉnh. (Để đối chiếu: so trực tiếp con số theo cách thông thường, gọi là tương quan Pearson, ra 0,81, gần với Spearman 0,76, nên kết luận không thay đổi.)

**Số liệu** (hình H5.3):

| Chỉ tiêu | Toán TB | Văn TB | Tỷ lệ thi Ngoại ngữ |
|---|---|---|---|
| Thu nhập bình quân đầu người | **0,76** | 0,35 | **0,85** |
| HDI | **0,79** | 0,36 | **0,86** |
| Tỷ lệ hộ nghèo | **−0,77** | −0,31 | **−0,79** |
| GRDP bình quân đầu người | 0,60 | 0,20 | 0,78 |
| Tỷ lệ đô thị hóa | 0,57 | 0,16 | 0,80 |
| Tỷ lệ lao động qua đào tạo | 0,58 | 0,39 | 0,62 |
| Tỷ lệ dùng internet | 0,60 | 0,30 | 0,75 |
| Học sinh / giáo viên THPT | 0,15 | 0,24 | 0,17 |

Ba điểm đáng chú ý:
- **Thu nhập người dân và HDI** liên quan mạnh hơn **GRDP**, tức giá trị kinh tế tỉnh làm ra. Ví dụ Quảng Ninh có GRDP bình quân đầu người cao nhất cả nước, nhưng thu nhập của người dân không cao tương ứng. Điều tác động đến học sinh là đời sống của gia đình, không phải sản lượng kinh tế của tỉnh.
- **Tỷ lệ chọn thi Ngoại ngữ** đi theo mức sống còn sát hơn cả điểm Toán (0,85–0,86).
- **Số học sinh trên một giáo viên** gần như không liên quan (0,15). Có thể vì chỉ tiêu này chênh lệch ít giữa các tỉnh, từ 17 đến 26 học sinh/giáo viên, một nửa số tỉnh nằm trong khoảng 18–22.

#### b) Hồi quy: thu nhập dự đoán được bao nhiêu phần điểm thi?

**Kết luận:** Chỉ cần biết thu nhập của một tỉnh, mô hình dự đoán được khoảng **hai phần ba** sự chênh lệch điểm Toán giữa các tỉnh. Với Văn, mô hình gần như không dự đoán được gì.

**Cách đo: hồi quy tuyến tính, kiểm định chéo và R² ngoài mẫu**

*Hồi quy tuyến tính là gì?* Là tìm một công thức đơn giản để **đoán** điểm từ thu nhập, dạng "điểm Toán = a + b × thu nhập". Máy tự chọn a và b sao cho công thức đoán sát nhất với 34 tỉnh. Trên hình H5.4, công thức chính là đường thẳng màu xám.

*Kiểm định chéo: kiểm tra bằng "đề chưa gặp".* Một học sinh có thể làm đúng 100% đề cũ chỉ vì đã thuộc đáp án. Muốn biết em ấy có thật sự hiểu bài không, phải cho làm **đề mới**. Mô hình cũng vậy: chấm nó trên chính dữ liệu dùng để xây thì dễ "đẹp" giả tạo. Vì vậy nhóm làm như sau:
1. Chia 34 tỉnh thành 5 nhóm, mỗi nhóm khoảng 7 tỉnh.
2. **Giấu 1 nhóm**, xây công thức trên 4 nhóm còn lại, rồi dùng công thức đoán điểm của các tỉnh bị giấu.
3. Lần lượt giấu từng nhóm, để tỉnh nào cũng được đoán đúng một lần khi "chưa gặp".
4. Làm lại toàn bộ 5 lần với cách chia khác nhau rồi lấy trung bình, để kết quả không phụ thuộc vào may rủi của một lần chia.

*R² ngoài mẫu: đoán tốt hơn "đoán bừa" bao nhiêu?* Cách đoán đơn giản nhất là đoán mọi tỉnh bằng điểm trung bình cả nước. R² so cách đoán của mô hình với cách đó.

Ví dụ với 3 tỉnh (số liệu minh họa), điểm thật là 5, 6, 7:

| | Tỉnh 1 | Tỉnh 2 | Tỉnh 3 | Tổng sai số (bình phương) |
|---|---|---|---|---|
| Điểm thật | 5 | 6 | 7 | |
| Đoán bằng trung bình (6) | sai 1 | sai 0 | sai 1 | 1 + 0 + 1 = **2** |
| Đoán bằng mô hình | 5,2 (sai 0,2) | 6,0 (sai 0) | 6,8 (sai 0,2) | 0,04 + 0 + 0,04 = **0,08** |

R² = 1 − 0,08 / 2 = **0,96**: mô hình loại bỏ được 96% phần sai của cách đoán bừa.

*Cách đọc con số:*

| R² | Ý nghĩa | Ví dụ trong đồ án |
|---|---|---|
| Gần 1 | Đoán gần như đúng hoàn toàn | — |
| Khoảng 0,5–0,7 | Giải thích được phần lớn chênh lệch | Thu nhập → Toán: **0,65** |
| Gần 0 | Không tốt hơn đoán bừa bằng trung bình | Thu nhập → Văn: 0,06 |
| Âm | Còn tệ hơn đoán bừa (mô hình "học thuộc", gặp tỉnh mới thì đoán sai) | 4 chỉ tiêu → Văn: −0,08 |

Chữ "ngoài mẫu" nghĩa là R² được tính trên **các tỉnh bị giấu**, tức đúng kiểu "đề chưa gặp". Đây là con số trung thực về khả năng dự đoán.

**Số liệu** (hình H5.4):

| Mô hình (dùng chỉ tiêu nào để đoán) | Toán TB | Văn TB | Điểm TB chung |
|---|---|---|---|
| Chỉ thu nhập | **0,65** | 0,06 | **0,35** |
| Chỉ HDI | 0,56 | 0,04 | 0,30 |
| Chỉ GRDP | 0,26 | −0,02 | 0,08 |
| 4 chỉ tiêu: thu nhập, đô thị hóa, lao động qua đào tạo, HS/GV | 0,62 | −0,08 | 0,32 |
| 4 chỉ tiêu, có thêm ràng buộc chống học thuộc (ridge) | 0,48 | 0,08 | 0,27 |

Với Toán, sai số trung bình khi đoán giảm từ 0,50 điểm (đoán bằng trung bình cả nước) xuống **0,30 điểm** (đoán bằng thu nhập).

**Bài học về "học thuộc" (overfitting):** mô hình 4 chỉ tiêu, nếu chấm điểm ngay trên chính 34 tỉnh dùng để xây nó, có R² = 0,77, trông tốt hơn mô hình chỉ có thu nhập. Nhưng khi kiểm tra trên các tỉnh bị giấu, nó chỉ đạt 0,62, **thấp hơn** mô hình một biến (0,65). Thêm chỉ tiêu làm mô hình khớp dữ liệu cũ hơn, nhưng đoán tỉnh mới không tốt hơn. Với chỉ 34 tỉnh, mô hình đơn giản là lựa chọn đúng.

**Khi xét cùng lúc 4 chỉ tiêu** (điểm Toán, các chỉ tiêu đã đưa về cùng thang đo để so sánh được độ lớn):

| Chỉ tiêu | Mức ảnh hưởng | Có ý nghĩa thống kê? |
|---|---|---|
| Thu nhập | **+0,46** (mạnh nhất) | Có (p < 0,001) |
| Lao động qua đào tạo | +0,17 | Có (p = 0,005) |
| Tỷ lệ đô thị hóa | −0,15 | Có, nhưng yếu (p = 0,04) |
| Học sinh / giáo viên | −0,10 | Không (p = 0,06) |

- p-value nhỏ hơn 0,05 nghĩa là kết quả khó xảy ra do ngẫu nhiên.
- Hệ số âm của đô thị hóa **không** có nghĩa đô thị hóa làm giảm điểm. Nó có nghĩa: **khi hai tỉnh có cùng mức thu nhập**, tỉnh đô thị hóa cao hơn không có điểm cao hơn. Đô thị hóa chủ yếu "đi kèm" thu nhập; tính thu nhập rồi thì đô thị hóa không cho thêm thông tin.
- Các chỉ tiêu này không trùng lặp thông tin quá nhiều với nhau. Chỉ số kiểm tra trùng lặp (VIF) đều dưới 2,5, mức an toàn.

#### c) Phân cụm: các tỉnh tự chia thành mấy nhóm?

**Kết luận:** 34 tỉnh chia thành **3 nhóm rõ rệt**: nhóm đô thị – thu nhập cao, nhóm trung bình, và nhóm miền núi phía Bắc. Khoảng cách về Toán giữa nhóm đầu và nhóm cuối lớn gấp gần 3 lần khoảng cách về Văn.

**Cách đo: thuật toán KMeans và chỉ số silhouette**

*KMeans: tự chia nhóm mà không cần ai gán nhãn trước.* Mỗi tỉnh được mô tả bằng 9 chỉ tiêu: thu nhập, HDI, đô thị hóa, lao động qua đào tạo, hộ nghèo, internet, điểm Toán, điểm Văn, tỷ lệ thi Ngoại ngữ. Các chỉ tiêu được đưa về cùng thang đo trước, để thu nhập (hàng nghìn) không lấn át HDI (từ 0 đến 1). Hai tỉnh có 9 chỉ tiêu càng gần nhau thì càng "giống nhau".

Thuật toán chạy giống cách chia lớp thành 3 tổ:
1. Chọn tạm 3 "tỉnh tiêu biểu" làm tâm của 3 nhóm.
2. Mỗi tỉnh về nhóm có tâm giống mình nhất.
3. Dời tâm mỗi nhóm về chính giữa các tỉnh vừa vào nhóm đó.
4. Lặp lại bước 2–3 đến khi không tỉnh nào đổi nhóm nữa.

Thuật toán không biết tên tỉnh hay vùng miền; nhóm "miền núi phía Bắc" hoàn toàn do số liệu tự gom lại.

*Silhouette: mỗi tỉnh có "ngồi đúng bàn" không?* Với từng tỉnh, so hai khoảng cách:
- **a** = tỉnh đó khác các tỉnh **cùng nhóm** bao nhiêu (trung bình);
- **b** = tỉnh đó khác các tỉnh của **nhóm gần nhất bên cạnh** bao nhiêu.

Nếu a nhỏ hơn hẳn b, tỉnh nằm đúng nhóm. Silhouette của tỉnh = (b − a) / (giá trị lớn hơn trong a và b), rồi lấy trung bình cho cả 34 tỉnh.

| Silhouette | Ý nghĩa |
|---|---|
| Gần 1 | Các nhóm tách bạch rõ, tỉnh nào cũng giống nhóm mình hơn hẳn nhóm khác |
| Khoảng 0 | Tỉnh nằm ở ranh giới giữa hai nhóm |
| Âm | Tỉnh bị xếp nhầm nhóm |

Nhóm thử chia từ 2 đến 6 nhóm:

| Số nhóm | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| Silhouette | **0,54** | 0,49 | 0,36 | 0,39 | 0,35 |

Chia 2 nhóm có điểm cao nhất, nhưng chỉ tách 7 tỉnh miền núi phía Bắc ra khỏi 27 tỉnh còn lại, quá hiển nhiên. Chia **3 nhóm** có điểm gần bằng (0,49) và cho nhiều thông tin hơn, nên nhóm chọn 3. Từ 4 nhóm trở lên, điểm giảm rõ, nghĩa là chia nhỏ hơn bắt đầu tách cả những tỉnh vốn giống nhau.

**Số liệu** (hình H5.5):

| Nhóm | Số tỉnh | Thu nhập (khoảng, nghìn đ/tháng) | Đô thị hóa | Hộ nghèo | Toán TB | Văn TB | Thi Ngoại ngữ |
|---|---|---|---|---|---|---|---|
| Đô thị – thu nhập cao | 9 | 6.800 | 55% | 0,5% | **5,88** | 6,53 | 34% |
| Trung bình | 18 | 5.100 | 27% | 1,7% | 5,44 | 6,42 | 21% |
| Miền núi phía Bắc | 7 | 3.100 | 15% | 8,6% | **4,71** | 6,09 | 12% |

- Nhóm đô thị – thu nhập cao: Hà Nội, TP.HCM, Hải Phòng, Đà Nẵng, Bắc Ninh, Quảng Ninh, Đồng Nai, Huế, Ninh Bình.
- Nhóm miền núi phía Bắc: Cao Bằng, Lai Châu, Lào Cai, Lạng Sơn, Sơn La, Tuyên Quang, Điện Biên.

Nhóm đầu và nhóm cuối chênh nhau **1,17 điểm Toán** nhưng chỉ **0,44 điểm Văn**.

**Cách vẽ hình H5.5: kỹ thuật PCA**

Mỗi tỉnh có 9 chỉ tiêu, tức 9 chiều, nhưng giấy chỉ vẽ được 2 chiều. **PCA** (phân tích thành phần chính) là cách "nén" 9 chỉ tiêu thành 2 trục mà mất ít thông tin nhất.

> Ví dụ: chụp ảnh một chiếc ô tô. Ảnh chỉ có 2 chiều nên luôn mất bớt thông tin. Chụp từ chính diện thì khó nhận ra đó là xe gì; chụp chéo từ bên hông thì nhìn là biết ngay. PCA tự tìm "góc chụp" cho 9 chỉ tiêu sao cho ảnh 2 chiều giữ được nhiều hình dạng nhất.

Kết quả:
- **Trục ngang** giữ được **68%** thông tin của cả 9 chỉ tiêu. Trên trục này, thu nhập, HDI, đô thị hóa, internet, điểm Toán và tỷ lệ thi Ngoại ngữ cùng tăng về một phía, hộ nghèo tăng về phía ngược lại. Vì vậy có thể gọi nó là **"trục mức sống"**: bên trái là các tỉnh khá giả (Hà Nội, TP.HCM), bên phải là các tỉnh khó khăn (Điện Biên, Lai Châu).
- **Trục dọc** giữ thêm **12%** thông tin, và gần như **chỉ do điểm Văn** quyết định: tỉnh càng nằm cao thì điểm Văn càng thấp. Tỉnh nằm tách hẳn ở trên cùng là Vĩnh Long, tỉnh có điểm Văn trung bình thấp nhất (5,00). Việc điểm Văn "tách" ra thành một trục riêng, không nằm trên trục mức sống, là một cách nhìn khác của phát hiện chính (mục I.4): chênh lệch điểm Văn giữa các tỉnh không đi theo giàu nghèo.

Hai trục cộng lại giữ 80% thông tin, đủ để các tỉnh trên hình nằm đúng vị trí tương đối với nhau. Ba nhóm do KMeans chia, phân biệt bằng màu và hình dạng điểm, tách nhau khá rõ chủ yếu theo trục mức sống.

#### d) Trả lời câu hỏi 1

**Có.** Các tỉnh có thu nhập, mức sống và điều kiện tốt hơn có kết quả thi cao hơn, nhưng mức độ khác nhau rõ rệt giữa các môn:
- **Rõ nhất ở Toán và việc chọn thi Ngoại ngữ.** Chỉ thu nhập đã dự đoán được khoảng 65% chênh lệch điểm Toán giữa các tỉnh.
- **Yếu ở Văn:** mức sống gần như không dự đoán được điểm Văn.
- **Thu nhập người dân** là chỉ tiêu giải thích tốt nhất, tốt hơn GRDP. **Đô thị hóa** chủ yếu đi kèm thu nhập. **Số học sinh trên một giáo viên** gần như không liên quan.

Đây là quan hệ **tương quan ở cấp tỉnh**, không chứng minh thu nhập là nguyên nhân trực tiếp, và không áp dụng cho từng học sinh.

### I.3. Câu hỏi 2: Môn nào chênh lệch giữa các tỉnh nhiều nhất?

**Kết luận:** **Ngữ văn** chênh lệch giữa các tỉnh nhiều nhất, gấp gần 3 lần Toán. Lịch sử là môn các tỉnh đồng đều nhất.

**Cách đo: chỉ số eta² (đọc là "eta bình phương")**

*Ý tưởng:* điểm của 1,2 triệu thí sinh khác nhau rất nhiều, có bạn 3 điểm, có bạn 9 điểm. Sự khác nhau đó đến từ hai nguồn:
- **Khác nhau giữa các tỉnh:** tỉnh này điểm trung bình cao, tỉnh kia thấp.
- **Khác nhau giữa các bạn trong cùng một tỉnh:** cùng tỉnh nhưng bạn học giỏi, bạn học yếu.

eta² trả lời câu hỏi: **trong toàn bộ sự khác nhau về điểm, bao nhiêu phần trăm là do khác tỉnh?** Môn nào có eta² càng cao thì các tỉnh càng chênh lệch nhau.

Một cách hiểu khác: nếu phải đoán điểm của một thí sinh bất kỳ, biết thêm **bạn ấy ở tỉnh nào** thì đoán chính xác hơn bao nhiêu? eta² cao nghĩa là biết tỉnh giúp đoán tốt hơn nhiều. Đây cũng chính là ý tưởng của R² ở mục I.2b, chỉ khác là thông tin dùng để đoán ở đây là "tỉnh".

*Ví dụ với 2 tỉnh, mỗi tỉnh 3 thí sinh (số liệu minh họa):*

| | Tỉnh A | Tỉnh B | Điểm TB của tỉnh | eta² | Ý nghĩa |
|---|---|---|---|---|---|
| **Môn X** | 7 – 8 – 9 | 3 – 4 – 5 | A: 8, B: 4 | **86%** | Trong mỗi tỉnh các bạn gần nhau, nhưng hai tỉnh cách xa nhau. Hầu hết khác biệt là **do tỉnh**. |
| **Môn Y** | 3 – 6 – 9 | 2 – 5 – 8 | A: 6, B: 5 | **4%** | Hai tỉnh gần như ngang nhau, nhưng trong mỗi tỉnh các bạn rất khác nhau. Khác biệt chủ yếu là **giữa các bạn**, không phải do tỉnh. |

Ở môn X, chỉ cần biết thí sinh ở tỉnh A là đoán được điểm khoảng 8, sai không quá 1 điểm. Ở môn Y, biết thí sinh ở tỉnh A cũng chẳng giúp gì, vì điểm trong tỉnh A trải từ 3 đến 9.

Cách tính (cho môn X):
1. Điểm trung bình chung của cả 6 bạn là 6.
2. **Tổng khác biệt:** mỗi bạn lệch bao nhiêu so với 6, bình phương lên rồi cộng lại: 1 + 4 + 9 + 9 + 4 + 1 = **28**.
3. **Phần do tỉnh:** điểm trung bình mỗi tỉnh lệch bao nhiêu so với 6, bình phương, nhân với số bạn của tỉnh rồi cộng lại: 3 × (8 − 6)² + 3 × (4 − 6)² = **24**.
4. **eta² = 24 / 28 = 86%.**

Với dữ liệu thật, máy tính làm đúng như vậy cho từng môn, trên toàn bộ 1,2 triệu thí sinh và 34 tỉnh.

*Cách đọc con số:*

| eta² | Ý nghĩa | Ví dụ trong đồ án |
|---|---|---|
| 0% | Các tỉnh có điểm trung bình y hệt nhau, biết tỉnh không giúp gì | — |
| Thấp (dưới 5%) | Các tỉnh khá đồng đều | Lịch sử 1,9%, Hóa học 2,1% |
| Cao hơn hẳn các môn khác | Các tỉnh chênh lệch rõ rệt | **Ngữ văn 16,3%**, gấp gần 3 lần Toán 5,7% |

**Lưu ý khi đọc:** ngay cả với Văn, 84% sự khác biệt điểm vẫn là khác biệt giữa các bạn **trong cùng một tỉnh**. Tỉnh có ảnh hưởng, nhưng năng lực của từng học sinh vẫn quan trọng hơn nhiều. Khi nói nên dùng đủ cụm "16% **sự khác nhau về điểm**", không nói "16% thí sinh".

*Vì sao không dùng cách đơn giản "tỉnh cao nhất trừ tỉnh thấp nhất"?*
- Cách đó chỉ nhìn **2 tỉnh ở hai đầu** và bỏ qua 32 tỉnh còn lại. Chỉ cần một tỉnh bất thường là kết quả lệch.
- Mỗi môn có độ "rộng" điểm khác nhau. Chênh 1 điểm ở môn mà điểm thí sinh vốn trải rộng thì không đáng kể bằng chênh 1 điểm ở môn mà điểm thí sinh vốn sát nhau. eta² tự tính đến điều này vì nó so chênh lệch giữa các tỉnh với độ rộng điểm của chính môn đó, nên **so sánh được giữa các môn**.

**Số liệu** (hình H5.2):

| Môn | eta² | Tỉnh thấp nhất → cao nhất (điểm TB) |
|---|---|---|
| **Ngữ văn** | **16,3%** | Vĩnh Long 5,00 → Ninh Bình 7,26 |
| Sinh học | 7,7% | Cao Bằng 4,49 → Bắc Ninh 6,91 |
| Tin học | 7,2% | Sơn La 4,86 → Hà Tĩnh 7,50 |
| Toán | 5,7% | Sơn La 4,25 → Ninh Bình 6,26 |
| Công nghệ | 4,2% | |
| GD kinh tế và pháp luật | 4,1% | |
| Ngoại ngữ | 3,7% | |
| Vật lí | 3,6% | |
| Địa lí | 2,6% | |
| Hóa học | 2,1% | |
| **Lịch sử** | **1,9%** | |

Hai lưu ý:
- Ngay cả với Văn, 84% sự khác biệt điểm vẫn nằm **trong** từng tỉnh. Khác biệt giữa các bạn cùng tỉnh lớn hơn nhiều so với khác biệt giữa các tỉnh.
- Sinh học và Tin học đứng thứ 2, thứ 3 nhưng có ít thí sinh (68.436 và 18.141 bài), và người chọn thường là người giỏi môn đó. Kết quả hai môn này kém chắc chắn hơn Toán và Văn, vốn gần như ai cũng thi.

### I.4. Phát hiện chính: ghép hai câu hỏi lại

Đặt hai kết quả cạnh nhau:

| | Chênh lệch giữa các tỉnh (eta²) | Mức sống dự đoán được (R² ngoài mẫu) |
|---|---|---|
| **Toán** | 5,7%, trung bình | **0,65**, cao |
| **Ngữ văn** | **16,3%, cao nhất** | 0,06, gần như không |

**Văn là môn các tỉnh chênh nhau nhiều nhất, nhưng lại là môn ít liên quan đến giàu nghèo nhất.** Chênh lệch điểm Văn giữa các tỉnh là có thật, nhưng đến từ một yếu tố khác ngoài điều kiện kinh tế – xã hội. Đó có thể là cách dạy, cách ra đề ôn tập, hay cách chấm thi tự luận ở từng địa phương. Dữ liệu hiện có chưa đủ để xác định yếu tố nào.

### I.5. Một quan sát thêm: điểm Văn dồn ở đúng 5,0

**Quan sát:** ở một số tỉnh, số bài Văn được đúng 5,0 điểm nhiều hơn hẳn so với các mức điểm lân cận.

**Cách đo:** Văn là môn tự luận, và giám khảo có thói quen cho điểm chẵn nửa điểm, nên các mức x,0 và x,5 luôn nhiều hơn các mức x,25 và x,75 kề bên. Vì vậy nhóm so mức 5,0 với các mức **cùng loại** là 4,5 và 5,5:

> tỷ số = (% bài được 5,0) ÷ (trung bình % bài được 4,5 và 5,5)

Tỷ số = 1 nghĩa là không có gì bất thường; lớn hơn 1 nghĩa là mức 5,0 "nhô" lên.

**Số liệu** (hình H5.6):
- Toàn quốc: 4,1% bài được 5,0, trong khi 4,5 có 2,0% và 5,5 có 4,4%. Tỷ số = **1,27**.
- Để đối chứng, các mức 4,5 / 5,5 / 6,0 có tỷ số lần lượt 0,73 / 0,86 / 1,04. Như vậy **chỉ riêng mức 5,0 nhô lên**.
- Theo tỉnh: cao nhất là **Lâm Đồng 1,82** và Đồng Nai 1,74; gần như không có hiện tượng (khoảng 1,0) ở Hưng Yên, Bắc Ninh, TP.HCM, Hà Nội.

**Cách hiểu đúng:** đây chỉ là **quan sát thống kê về hình dạng phổ điểm**. Nhóm không có dữ liệu để biết nguyên nhân và **không đưa ra kết luận** về cách chấm thi của bất kỳ địa phương nào. Quan sát này gợi ý một hướng tìm hiểu tiếp, liên quan đến phát hiện ở mục I.4.

### I.6. Tóm tắt kết quả

| Câu hỏi | Trả lời | Bằng chứng |
|---|---|---|
| Tỉnh có mức sống tốt hơn thì thi tốt hơn? | **Có**, rõ ở Toán và Ngoại ngữ, yếu ở Văn | Tương quan thu nhập – Toán 0,76; thu nhập dự đoán 65% chênh lệch Toán |
| Chỉ tiêu nào giải thích tốt nhất? | **Thu nhập người dân**, tốt hơn GRDP; đô thị hóa chỉ đi kèm | R² ngoài mẫu: thu nhập 0,65, GRDP 0,26 |
| Môn nào chênh lệch giữa các tỉnh nhiều nhất? | **Ngữ văn**; đều nhất là Lịch sử | eta²: Văn 16,3%, Toán 5,7%, Sử 1,9% |
| Phát hiện chính | Văn chênh lệch nhiều nhất nhưng ít liên quan đến mức sống nhất | eta² cao nhất, R² gần 0 |

## J. Lời nói mẫu khi thuyết trình (khoảng 2 phút)

Phần câu hỏi 1 và câu hỏi 2 đã có trong mục B. Dưới đây là bản đầy đủ theo thứ tự trình chiếu.

**1. Bức tranh chung (15 giây, hình H5.1)**

> "Trước hết là bức tranh chung. Điểm Văn trung bình cả nước là 6,5, Toán là 5,65. Phổ điểm Toán có hai đỉnh, cho thấy thí sinh chia thành hai nhóm khá rõ về năng lực Toán."

**2. Câu hỏi 1 (45 giây, hình H5.3 rồi H5.4)**

> "Câu hỏi thứ nhất: tỉnh có mức sống tốt hơn thì thi có tốt hơn không? Câu trả lời là **có, và rõ nhất ở môn Toán**.
>
> Nếu xếp hạng 34 tỉnh theo thu nhập rồi xếp hạng theo điểm Toán, hai bảng xếp hạng khá giống nhau. Chỉ cần biết thu nhập của một tỉnh, nhóm đã dự đoán được khoảng **hai phần ba** chênh lệch điểm Toán giữa các tỉnh. Nhóm kiểm tra bằng cách giấu bớt tỉnh đi rồi đoán thử, nên con số này đáng tin.
>
> Thu nhập của người dân giải thích tốt hơn nhiều so với GRDP của tỉnh. Có tỉnh làm ra nhiều của cải như Quảng Ninh, nhưng thu nhập người dân không cao tương ứng.
>
> Còn với **môn Văn thì mức sống gần như không dự đoán được gì**."

**3. Phân cụm (20 giây, hình H5.5)**

> "Khi để máy tự chia nhóm, 34 tỉnh tách thành 3 nhóm: nhóm đô thị thu nhập cao như Hà Nội, TP.HCM; nhóm trung bình; và nhóm 7 tỉnh miền núi phía Bắc. Nhóm đầu và nhóm cuối chênh nhau hơn 1 điểm Toán, nhưng chỉ chưa tới nửa điểm Văn."

**4. Câu hỏi 2 (30 giây, hình H5.2)**

> "Câu hỏi thứ hai: môn nào chênh lệch giữa các tỉnh nhiều nhất? Giả sử chỉ biết một bạn đến từ tỉnh nào, ta đoán được điểm của bạn ấy tốt hơn bao nhiêu? Đo theo cách đó, **Ngữ văn là môn chênh lệch nhiều nhất**, gấp gần 3 lần Toán. Văn trung bình cao nhất là Ninh Bình 7,26, thấp nhất là Vĩnh Long 5,0. Lịch sử là môn các tỉnh đều nhau nhất."

**5. Phát hiện chính (20 giây)**

> "Đặt hai kết quả cạnh nhau thì thấy điều bất ngờ: **Văn là môn các tỉnh chênh nhau nhiều nhất, nhưng lại ít liên quan đến giàu nghèo nhất**. Chênh lệch điểm Văn là có thật, nhưng đến từ một yếu tố khác, có thể là cách dạy hay cách chấm tự luận ở từng nơi. Dữ liệu hiện tại chưa đủ để biết chính xác."

**6. Quan sát điểm 5,0 (20 giây, hình H5.6, tùy thời gian)**

> "Nhóm còn quan sát thấy ở một số tỉnh, số bài Văn được đúng 5 điểm nhiều hơn hẳn các mức lân cận, cao nhất là Lâm Đồng. Nhóm xin nhấn mạnh đây chỉ là quan sát về hình dạng phổ điểm, nhóm không có dữ liệu để kết luận nguyên nhân."

**Câu trả lời dự phòng:**

**"R² là gì?"**
> "R² cho biết cách đoán của mô hình tốt hơn bao nhiêu so với đoán đại bằng điểm trung bình cả nước. R² bằng 0,65 nghĩa là mô hình giải thích được khoảng 65% sự chênh lệch điểm Toán giữa các tỉnh; tính theo điểm, sai số trung bình giảm từ 0,5 xuống 0,3 điểm. Nhóm tính R² trên các tỉnh bị giấu đi, nên đây là khả năng đoán tỉnh mới, không phải độ khớp với dữ liệu cũ."

**"Vì sao không dùng nhiều chỉ tiêu hơn cho mô hình tốt hơn?"**
> "Nhóm đã thử. Mô hình 4 chỉ tiêu khớp dữ liệu cũ tốt hơn, nhưng khi đoán các tỉnh bị giấu thì lại kém hơn mô hình chỉ có thu nhập. Với 34 tỉnh, thêm chỉ tiêu chỉ làm mô hình học thuộc dữ liệu."

**"Như vậy giàu thì học giỏi à?"**
> "Không hẳn. Nhóm chỉ thấy các **tỉnh** có thu nhập cao thì điểm **trung bình của tỉnh** cao hơn. Đó là tương quan, không chứng minh thu nhập là nguyên nhân, và cũng không áp dụng cho từng học sinh. Trong tỉnh nghèo vẫn có nhiều bạn điểm rất cao."

**"Điểm Văn dồn ở 5,0 có phải gian lận không?"**
> "Nhóm không kết luận như vậy. Đây chỉ là quan sát thống kê về hình dạng phổ điểm. Có nhiều cách giải thích khác nhau, và nhóm không có dữ liệu để biết đâu là nguyên nhân."

---

# Thảo luận, Kết luận và Tài liệu tham khảo

Phần K dùng cho báo cáo (chương 6, 7 và tài liệu tham khảo). Phần L là lời kết khi thuyết trình.

## K. Đoạn thảo luận, kết luận cho báo cáo

### K.1. Thảo luận (chương 6)

#### Vì sao Toán và Ngoại ngữ đi theo mức sống, còn Văn thì không?

Dữ liệu chỉ cho thấy các đại lượng **đi cùng nhau**, không cho biết **vì sao**. Dưới đây là một số cách giải thích có thể có. Chúng là **giả thuyết**, đồ án chưa kiểm chứng.

- **Toán và Ngoại ngữ** là các môn mà kết quả phụ thuộc nhiều vào việc luyện tập có hệ thống: học thêm, tài liệu, trung tâm ngoại ngữ, giáo viên chuyên sâu. Những điều kiện này thường tập trung ở nơi có thu nhập cao và đô thị hóa cao.
- **Tỷ lệ chọn thi Ngoại ngữ** đi theo mức sống còn sát hơn cả điểm Toán (Spearman 0,85 so với 0,76). Ở nhiều tỉnh khó khăn, phần lớn thí sinh không chọn thi Ngoại ngữ, có thể vì ít cơ hội tiếp cận tiếng Anh từ sớm.
- **Ngữ văn** là môn tự luận. Kết quả phụ thuộc nhiều vào cách dạy, cách ôn và việc chấm bài theo hướng dẫn chấm. Đây là những yếu tố có thể khác nhau giữa các địa phương mà không liên quan đến thu nhập. Điều này phù hợp với việc Văn chênh lệch giữa các tỉnh nhiều nhất nhưng mức sống không dự đoán được.

#### Điều kiện giáo dục đo được còn hạn chế

Chỉ tiêu "số học sinh trên một giáo viên THPT" gần như không liên quan đến điểm thi. Điều này **không có nghĩa** là giáo viên không quan trọng. Chỉ tiêu này chỉ đo **số lượng** giáo viên, không đo **chất lượng**, và lại chênh lệch ít giữa các tỉnh (17–26 học sinh/giáo viên). Để đánh giá đúng vai trò của điều kiện giáo dục, cần các chỉ tiêu tốt hơn, như trình độ giáo viên, chi tiêu cho giáo dục hay tỷ lệ trường đạt chuẩn.

### K.2. Hạn chế (chương 6)

| # | Hạn chế | Ảnh hưởng đến kết luận |
|---|---|---|
| 1 | **Tương quan không phải nhân quả.** | Chỉ nói được "tỉnh giàu hơn có điểm cao hơn", không nói được "vì giàu nên điểm cao". |
| 2 | **Kết luận ở cấp tỉnh, không áp dụng cho từng người.** | Tỉnh có thu nhập cao thì điểm trung bình cao, nhưng không suy ra học sinh nhà khá giả nào cũng điểm cao. Suy luận từ nhóm sang cá nhân là một lỗi thường gặp trong thống kê. |
| 3 | **Chỉ có 34 tỉnh.** | Mô hình dễ "học thuộc" dữ liệu. Nhóm đã hạn chế bằng kiểm định chéo và ưu tiên mô hình đơn giản, nhưng các con số vẫn có độ dao động. |
| 4 | **Môn tự chọn: người chọn thường là người giỏi môn đó.** | So sánh giữa các tỉnh ở Sinh, Tin, Ngoại ngữ… kém chắc chắn hơn Toán và Văn. Ví dụ tỉnh có ít người thi Ngoại ngữ thì những người thi thường là người giỏi, làm điểm trung bình Ngoại ngữ của tỉnh "đẹp" hơn thực tế. |
| 5 | **Tỉnh sau sáp nhập gồm nhiều vùng rất khác nhau.** | Ví dụ một tỉnh mới có thể gồm cả vùng đô thị ven biển lẫn vùng núi. Con số trung bình của tỉnh che mất sự khác biệt bên trong. |
| 6 | **Dữ liệu điểm thi lấy từ nguồn cộng đồng**, thu thập từ trang tra cứu điểm. | Nhóm đã kiểm tra tính nhất quán (không trùng số báo danh, không có điểm ngoài 0–10), nhưng chưa đối chiếu với số liệu chính thức của Bộ Giáo dục và Đào tạo. |
| 7 | **Số liệu kinh tế – xã hội năm 2025, điểm thi năm 2026**, và một số chỉ tiêu năm 2025 trong Niên giám có thể là số sơ bộ. | Mức sống thay đổi chậm nên ảnh hưởng nhỏ, nhưng vẫn là một độ lệch thời gian. |
| 8 | **Chỉ có một năm thi.** | Chưa biết các quan hệ này ổn định qua các năm hay chỉ riêng năm 2026. |
| 9 | **Spark chạy trên một máy (chế độ local).** | Chưa kiểm chứng hiệu năng thực tế trên cụm nhiều máy. |

### K.3. Kết luận (chương 7)

Đồ án đã **tích hợp hai nguồn dữ liệu rất khác nhau**: điểm thi tốt nghiệp THPT 2026 của 1.200.202 thí sinh (34 file CSV) và số liệu kinh tế – xã hội năm 2025 của 34 tỉnh, thành phố trích từ Niên giám thống kê dạng PDF. Toàn bộ quá trình được xử lý bằng Apache Spark.

Quá trình tích hợp phát hiện và xử lý nhiều vấn đề dữ liệu **không gây báo lỗi**, đáng chú ý nhất là:
- điểm thi của 14 tỉnh bị giấu trong một cột văn bản mã hóa (tỷ lệ có điểm Toán từ 39,3% lên 98,6% sau xử lý);
- 7 mã tỉnh cũ bị dùng lại cho tỉnh khác sau sắp xếp hành chính.

Kết quả được kiểm chứng bằng đối chiếu với số liệu cả nước và bằng một pipeline độc lập viết bằng pandas (khớp 60/60 cột).

Trả lời hai câu hỏi nghiên cứu:

1. **Các tỉnh có mức sống tốt hơn có kết quả thi cao hơn, rõ nhất ở Toán và việc chọn thi Ngoại ngữ.** Chỉ riêng thu nhập bình quân đầu người đã giải thích được khoảng 65% chênh lệch điểm Toán giữa các tỉnh. Thu nhập của người dân giải thích tốt hơn GRDP; đô thị hóa chủ yếu đi kèm thu nhập; số học sinh trên một giáo viên gần như không liên quan.
2. **Ngữ văn là môn chênh lệch giữa các tỉnh nhiều nhất** (16,3% sự khác nhau về điểm là do khác tỉnh, gấp gần 3 lần Toán); Lịch sử đồng đều nhất.

**Phát hiện chính:** Ngữ văn chênh lệch giữa các tỉnh nhiều nhất nhưng lại **ít liên quan đến mức sống nhất**. Chênh lệch điểm Văn là có thật nhưng đến từ yếu tố khác ngoài điều kiện kinh tế – xã hội. Hiện tượng số bài Văn dồn ở đúng 5,0 điểm, rõ ở một số tỉnh, là một quan sát gợi ý hướng tìm hiểu tiếp.

### K.4. Hướng phát triển (chương 7)

- **Nhiều năm thi:** gộp điểm các năm 2025, 2026 và các năm sau để xem các quan hệ có ổn định không. Khi đó dữ liệu lớn hơn nhiều lần, đúng với thế mạnh của Spark.
- **Đơn vị nhỏ hơn tỉnh:** phân tích theo cụm điểm thi hoặc cấp xã để thấy sự khác biệt bên trong các tỉnh mới sáp nhập.
- **Thêm chỉ tiêu giáo dục chất lượng hơn:** trình độ giáo viên, chi tiêu giáo dục, tỷ lệ trường đạt chuẩn.
- **Tìm hiểu chênh lệch điểm Văn:** xem hiện tượng dồn ở 5,0 ở cấp cụm điểm thi, và so sánh với năm trước.
- **Chạy trên cụm nhiều máy** để đo hiệu năng thực tế của Spark với dữ liệu lớn hơn.

### K.5. Tài liệu tham khảo

*Ghi chú cho người viết: các mục đánh dấu (\*) cần kiểm tra lại số hiệu, ngày ban hành hoặc thông tin xuất bản trước khi nộp.*

**Văn bản và nguồn dữ liệu**

1. Quốc hội (2025). *Nghị quyết số 202/2025/QH15 về việc sắp xếp đơn vị hành chính cấp tỉnh*. Hiệu lực từ 01/07/2025. (\*)
2. Cục Thống kê (2026). *Niên giám thống kê 2025*. Hà Nội. https://www.nso.gov.vn/wp-content/uploads/2026/07/NG-TOAN-QUOC-2025-1.pdf
3. Bộ Giáo dục và Đào tạo. *Quy chế thi tốt nghiệp trung học phổ thông* (áp dụng từ năm 2025, theo chương trình giáo dục phổ thông 2018). (\*)
4. Dữ liệu điểm thi tốt nghiệp THPT 2026: kho dữ liệu `duongtrongnguyen123/diem-thi-thptqg-2026` trên GitHub, thu thập ngày 01/07/2026.

**Công cụ**

5. Zaharia, M. et al. (2016). Apache Spark: A unified engine for big data processing. *Communications of the ACM*, 59(11), 56–65.
6. Meng, X. et al. (2016). MLlib: Machine learning in Apache Spark. *Journal of Machine Learning Research*, 17(34), 1–7.
7. Apache Software Foundation. *Apache Spark 4.0 documentation* và *PySpark API reference*. https://spark.apache.org/docs/latest/
8. McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference*, 56–61. (thư viện pandas)

**Phương pháp**

9. Spearman, C. (1904). The proof and measurement of association between two things. *The American Journal of Psychology*, 15(1), 72–101.
10. Lloyd, S. (1982). Least squares quantization in PCM. *IEEE Transactions on Information Theory*, 28(2), 129–137. (thuật toán KMeans)
11. Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics*, 20, 53–65.
12. Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer. (hồi quy, kiểm định chéo, PCA)
13. Robinson, W. S. (1950). Ecological correlations and the behavior of individuals. *American Sociological Review*, 15(3), 351–357. (lỗi suy luận từ nhóm sang cá nhân)

## L. Lời kết khi thuyết trình (khoảng 30 giây)

> "Tóm lại, nhóm đã ghép hai bộ dữ liệu rất khác nhau, điểm của 1,2 triệu thí sinh và Niên giám thống kê dạng PDF, xử lý bằng Apache Spark, và kiểm chứng kết quả bằng hai cách độc lập.
>
> Kết quả cho thấy tỉnh có mức sống tốt hơn thì điểm Toán và tỷ lệ thi Ngoại ngữ cao hơn rõ rệt. Nhưng môn Văn, môn chênh lệch giữa các tỉnh nhiều nhất, lại gần như không liên quan đến giàu nghèo.
>
> Nhóm cũng xin lưu ý: đây là tương quan ở cấp tỉnh, không phải nhân quả và không áp dụng cho từng học sinh. Hướng tiếp theo là gộp nhiều năm thi và phân tích ở cấp nhỏ hơn tỉnh, đặc biệt để tìm hiểu vì sao điểm Văn chênh lệch.
>
> Nhóm em xin cảm ơn thầy cô và các bạn đã lắng nghe."
