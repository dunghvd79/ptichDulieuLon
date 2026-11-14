"""Tạo SparkSession chạy local, đã xử lý sẵn các bẫy khi chạy PySpark trên Windows.

Những lỗi đã gặp và cách tránh (chi tiết trong spark/README.md):
  1. Đường dẫn có dấu cách ("E:\\2026 Year\\...") làm spark-class.cmd không gọi được
     Python  -> venv phải nằm ở đường dẫn KHÔNG có dấu cách (vd. C:\\Users\\<you>\\venvs\\ptdl).
  2. Python 3.12+ trên Windows làm Python worker crash ("Python worker exited unexpectedly")
     -> dùng Python 3.11.
  3. Docker Desktop thêm "host.docker.internal" vào file hosts -> ép driver dùng 127.0.0.1.
  4. Không có winutils.exe -> không ghi parquet/CSV bằng Spark; kết quả (nhỏ) được xuất
     qua .toPandas().to_csv(...).
"""
import glob
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))  # dùng chung common.py với pipeline pandas


def _setup_env():
    if not os.environ.get("JAVA_HOME"):
        cands = sorted(glob.glob(r"C:\Program Files\Java\jdk-*") +
                       glob.glob(r"C:\Program Files\Eclipse Adoptium\jdk-*"))
        if cands:
            os.environ["JAVA_HOME"] = cands[-1]
    os.environ.setdefault("PYSPARK_PYTHON", sys.executable)
    os.environ.setdefault("PYSPARK_DRIVER_PYTHON", sys.executable)
    os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    # UDF dùng hàm trong scripts/: Python worker kế thừa PYTHONPATH từ JVM.
    # (sc.addPyFile cần winutils.exe trên Windows nên không dùng.)
    pp = os.environ.get("PYTHONPATH", "")
    if str(ROOT / "scripts") not in pp:
        os.environ["PYTHONPATH"] = os.pathsep.join(filter(None, [str(ROOT / "scripts"), pp]))
    if " " in sys.executable:
        print(f"[canh bao] Python nằm ở đường dẫn có dấu cách ({sys.executable}); "
              "Spark trên Windows sẽ lỗi. Xem spark/README.md.", file=sys.stderr)


def get_spark(app="ptdl"):
    _setup_env()
    from pyspark.sql import SparkSession

    spark = (
        SparkSession.builder.master("local[*]").appName(app)
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.driver.memory", "4g")
        .config("spark.sql.shuffle.partitions", "16")   # dữ liệu ~1,2 triệu dòng, không cần 200
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark
