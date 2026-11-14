# Pipeline PySpark

| File | Việc |
|---|---|
| `_session.py` | Tạo SparkSession local, đã xử lý các lỗi khi chạy trên Windows |
| `etl_diemthi.py` | Bronze → Silver → Gold: 34 CSV điểm thi → bảng tổng hợp + ghép KT-XH |
| `doi_chieu_pandas.py` | So kết quả Spark với bản pandas (`scripts/`). Hiện tại 60/60 cột khớp |
| `mllib_tinh.py` | MLlib trên 34 tỉnh: hồi quy (Pipeline + repeated k-fold), VIF, KMeans + silhouette, PCA → `ml_*.csv`. Cờ `--chi-phan-cum` chỉ chạy phần phân cụm |

Đầu ra (chỉ có số liệu tổng hợp, không có SBD): `data/processed/spark/`

| File | Nội dung |
|---|---|
| `chat_luong_du_lieu.csv` | Chỉ số chất lượng dữ liệu trước/sau làm sạch |
| `diemthi_theo_tinh.csv` | 34 tỉnh, cùng định nghĩa cột với bản pandas |
| `diemthi_tinh_x_mon.csv` | Tỉnh × môn: số bài, TB, trung vị, độ lệch chuẩn, p25/p75, tỷ lệ <5, ≥8, ≤1, tỷ lệ chọn |
| `chenh_lech_giua_tinh_theo_mon.csv` | Mỗi môn: độ lệch chuẩn giữa tỉnh, khoảng cách, hệ số biến thiên, **eta²** |
| `to_hop_toan_quoc.csv`, `to_hop_theo_tinh.csv` | Tỷ lệ chọn tổ hợp 2 môn tự chọn |
| `diemthi_x_ktxh_34tinh.csv` | Ghép với `ktxh_34tinh_2025_wide.csv` |
| `thoi_gian_chay.csv` | Thời gian từng bước |

## Cài đặt (Windows)

```powershell
uv venv --python 3.11 C:\Users\DELL\venvs\ptdl      # ĐƯỜNG DẪN KHÔNG CÓ DẤU CÁCH
uv pip install --python C:\Users\DELL\venvs\ptdl\Scripts\python.exe -r requirements-spark.txt
# chạy từ thư mục gốc repo
C:\Users\DELL\venvs\ptdl\Scripts\python.exe spark\etl_diemthi.py
C:\Users\DELL\venvs\ptdl\Scripts\python.exe spark\doi_chieu_pandas.py
```

Cấu hình đã chạy được: **PySpark 4.0.1, Python 3.11, JDK 22**, không cần Hadoop/winutils. `JAVA_HOME` được tự dò trong `C:\Program Files\Java`.

## Các lỗi đã gặp khi dựng môi trường (có thể đưa vào báo cáo, mục 4.3)

| Triệu chứng | Nguyên nhân | Cách xử lý |
|---|---|---|
| `Missing Python executable ...`, `The system cannot find the path specified` | Repo nằm trong `E:\2026 Year\...`; `spark-class.cmd` không chịu đường dẫn có dấu cách | Đặt venv ở đường dẫn không có dấu cách |
| `Python worker exited unexpectedly (crashed)` ở mọi UDF/RDD | Python 3.12 trên Windows | Dùng Python 3.11 |
| Worker kết nối chậm, hostname `host.docker.internal` | Docker Desktop ghi đè file hosts | Ép `spark.driver.host`, `SPARK_LOCAL_IP` về `127.0.0.1` |
| Treo im lặng khi `read.csv("…/*.csv")`; log có `UnsatisfiedLinkError NativeIO$Windows.access0` | Glob của Hadoop gọi hàm native cần winutils | Truyền danh sách file tường minh |
| `Path does not exist: file:/E:/2026%20Year/...` | `Path.as_uri()` mã hóa dấu cách hai lần | Dùng `Path.as_posix()` |
| `ModuleNotFoundError: clean_diemthi` trong worker | Worker không có `scripts/` trên sys.path; `addPyFile` lại cần winutils | Đặt `PYTHONPATH` trước khi JVM khởi động (`_session.py`) |
| Chỉ số tổng ra null | `sum()` các cột có null | `coalesce(..., 0)` |

Ghi file bằng Spark (`df.write`) trên Windows vẫn cần winutils. Kết quả đều nhỏ nên xuất qua `toPandas().to_csv()`.
