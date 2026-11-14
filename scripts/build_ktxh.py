"""Bước 2: trích số liệu kinh tế – xã hội 34 tỉnh từ Niên giám thống kê 2025.

Nguồn: "Phụ lục số liệu một số chỉ tiêu kinh tế – xã hội chủ yếu của 34 tỉnh,
thành phố trực thuộc Trung ương" (trang 1142–1555 của file PDF, 209 biểu).
Cục Thống kê đã tự quy đổi số liệu cũ (63 tỉnh) sang 34 tỉnh mới.

Khó khăn khi trích từ PDF:
  - Số kiểu Việt Nam: "1.234,5" -> 1234.5; "-" hoặc ".." = không có số liệu.
  - Ô trống (giá trị 0) làm lệch cột -> gán số vào cột theo VỊ TRÍ KÝ TỰ,
    dùng các dòng đủ cột trên cùng trang làm mốc (số được căn phải).
  - Mỗi biểu trải 2 trang (trang "Tiếp theo") với lề lệch nhau -> mốc tính theo từng trang.

Đầu ra:
  data/processed/ktxh_34tinh_long.csv        tỉnh – chỉ tiêu – năm – giá trị – đơn vị – số biểu
  data/processed/ktxh_34tinh_2025_wide.csv   mỗi tỉnh một dòng (năm 2025 + chuỗi GRDP/người)

Chạy:  python scripts/build_ktxh.py            (thêm --bieu 52 60 để xem nhanh biểu bất kỳ)
"""
import re, sys
import pandas as pd
from pypdf import PdfReader
from common import NIENGIAM_PDF, PROCESSED, MAP_63_34, PROVINCES_34

APPENDIX_PAGES = range(1141, 1556)   # chỉ số 0-based, tương ứng trang 1142–1555
NUM = re.compile(r"(?<![\w])(-?\d[\d\.]*(?:,\d+)?|-|\.\.)(?![\w])")
YRS = [2020, 2021, 2022, 2023, 2024, 2025]

# (số biểu, tên chỉ tiêu, đơn vị, {chỉ số cột: năm})
SPEC = [
    (6,   "dan_so_tb",                  "nghìn người", dict(enumerate(YRS))),
    (9,   "dan_so_thanh_thi",           "nghìn người", dict(enumerate(YRS))),
    (43,  "grdp_binh_quan_nguoi",       "triệu đồng",  dict(enumerate(YRS))),
    (34,  "ty_le_ld_qua_dao_tao",       "%",           dict(enumerate(YRS))),
    (163, "thu_nhap_bq_lao_dong_thang", "nghìn đồng",  dict(enumerate(YRS))),
    (164, "hdi",                        "chỉ số",      dict(enumerate(YRS))),
    (166, "gini",                       "hệ số",       dict(enumerate(YRS))),
    (173, "ty_le_ho_ngheo",             "%",           dict(enumerate(YRS))),
    (186, "ty_le_dung_internet",        "%",           {0: 2024, 1: 2025}),
    (158, "thu_nhap_bq_nguoi_thang",    "nghìn đồng",  {0: 2025}),
    (5,   "dien_tich",                  "km2",         {0: 2025}),
    (5,   "mat_do_dan_so",              "người/km2",   {2: 2025}),
    (140, "so_truong_thpt",             "trường",      {3: 2025}),
    (142, "so_gv_thpt",                 "người",       {3: 2025}),
    (143, "so_hs_thpt",                 "người",       {3: 2025}),
    (147, "hs_tren_gv_thpt",            "người",       {3: 2025}),
]


def load_pages():
    reader = PdfReader(NIENGIAM_PDF)
    print(f"[pdf] {len(reader.pages)} trang, đọc phụ lục 34 tỉnh...")
    return {i: reader.pages[i].extract_text(extraction_mode="layout") for i in APPENDIX_PAGES}


def table_pages(pages, n):
    """Trang đầu của biểu n và trang 'Tiếp theo'; bỏ trang mục lục."""
    out = []
    for i, txt in pages.items():
        head = "\n".join(l for l in txt.splitlines()[:5] if l.strip())
        if re.search(rf"^\s*(\(Tiếp theo\).*\n\s*)?{n}\s", head, re.M) or re.search(rf"^\s*{n}\s+\S", head, re.M):
            if "Trang" not in txt and "Page" not in txt[:400]:
                out.append(i)
    return out


def to_float(v):
    if v is None or v in ("-", ".."):
        return None
    return float(v.replace(".", "").replace(",", "."))


def parse_table(pages, n):
    rows, ends, page_of = {}, {}, {}
    for i in table_pages(pages, n):
        for line in pages[i].splitlines():
            s = line.strip()
            for p in PROVINCES_34:
                if p in rows or not s.startswith(p):
                    continue
                if len(s) > len(p) and s[len(p)] not in " (*":
                    continue  # tránh nhầm "Hà Nội" với tên dài hơn
                off = line.index(p) + len(p)
                ms = list(NUM.finditer(line[off:].replace("(*)", "   ")))
                if ms:
                    rows[p] = [m.group(1) for m in ms]
                    ends[p] = [off + m.end() for m in ms]
                    page_of[p] = i
    if not rows:
        return rows
    width = max(map(len, rows.values()))
    for page in set(page_of.values()):  # căn lại cột cho dòng thiếu ô
        full = [ends[p] for p in rows if page_of[p] == page and len(rows[p]) == width] \
            or [ends[p] for p in rows if len(rows[p]) == width]
        anchors = [sum(c) / len(c) for c in zip(*full)]
        for p in rows:
            if page_of[p] == page and len(rows[p]) < width:
                fixed = ["-"] * width
                for v, e in zip(rows[p], ends[p]):
                    fixed[min(range(width), key=lambda k: abs(anchors[k] - e))] = v
                rows[p] = fixed
    return rows


def build(pages):
    long = []
    for n, name, unit, cols in SPEC:
        rows = parse_table(pages, n)
        assert len(rows) == 34, f"Biểu {n}: chỉ đọc được {len(rows)}/34 tỉnh"
        for prov, vals in rows.items():
            for ci, yr in cols.items():
                long.append(dict(ten_tinh=prov, chi_tieu=name, nam=yr,
                                 gia_tri=to_float(vals[ci]), don_vi=unit, bieu_nien_giam=n))
    L = pd.DataFrame(long)
    L["ten_tinh"] = L["ten_tinh"].replace({"TP. Hồ Chí Minh": "Hồ Chí Minh"})
    codes = pd.read_csv(MAP_63_34, dtype=str).drop_duplicates("ma_tinh_moi")
    codes = dict(zip(codes.ten_tinh_moi, codes.ma_tinh_moi))
    L.insert(0, "ma_tinh", L["ten_tinh"].map(codes))
    assert L["ma_tinh"].notna().all(), "Có tỉnh không khớp mã"
    return L.sort_values(["ma_tinh", "chi_tieu", "nam"])


def to_wide(L):
    W = L[L.nam == 2025].pivot(index=["ma_tinh", "ten_tinh"], columns="chi_tieu", values="gia_tri")
    W["ty_le_do_thi_pct"] = (W.dan_so_thanh_thi / W.dan_so_tb * 100).round(1)
    W["hs_thpt_tren_1000_dan"] = (W.so_hs_thpt / W.dan_so_tb).round(1)
    g = L[L.chi_tieu == "grdp_binh_quan_nguoi"].pivot(index="ma_tinh", columns="nam", values="gia_tri")
    g.columns = [f"grdp_nguoi_{c}" for c in g.columns]
    return W.join(g, on="ma_tinh").reset_index()


def validate(W):
    """Tổng 34 tỉnh phải khớp dòng 'Cả nước' trong Niên giám."""
    ca_nuoc = {"dan_so_tb": 102345.3, "so_gv_thpt": 148396, "so_hs_thpt": 3082574}
    for k, v in ca_nuoc.items():
        s = W[k].sum()
        print(f"[check] {k}: tổng 34 tỉnh = {s:,.1f} | cả nước = {v:,}  {'OK' if abs(s - v) < 1 else 'LỆCH'}")


if __name__ == "__main__":
    pages = load_pages()
    if "--bieu" in sys.argv:
        for n in sys.argv[sys.argv.index("--bieu") + 1:]:
            r = parse_table(pages, int(n))
            print(f"Biểu {n}: {len(r)} tỉnh"); [print("  ", k, v) for k, v in list(r.items())[:5]]
        sys.exit()
    PROCESSED.mkdir(parents=True, exist_ok=True)
    L = build(pages); W = to_wide(L)
    L.to_csv(PROCESSED / "ktxh_34tinh_long.csv", index=False)
    W.to_csv(PROCESSED / "ktxh_34tinh_2025_wide.csv", index=False)
    print(f"[save] ktxh_34tinh_long.csv ({len(L)} dòng), ktxh_34tinh_2025_wide.csv ({W.shape})")
    validate(W)
