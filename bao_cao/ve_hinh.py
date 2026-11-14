"""Vẽ toàn bộ hình cho báo cáo từ các bảng tổng hợp trong data/processed/spark/.

Quy ước (theo skill dataviz, đã chạy validate_palette.js trên nền trắng #ffffff):
  - 3 cụm KMeans: blue/orange/aqua (slot 1-3, đạt mọi cặp CVD ΔE>=9,2). Aqua chỉ 2,82:1 ->
    bù bằng hình dạng marker riêng + legend + nhãn trực tiếp + bảng cụm trong báo cáo.
  - Một chuỗi -> một màu (blue). Trước/sau -> 1 hue, 2 sắc độ (ordinal, đã kiểm).
  - Tương quan -> diverging blue (+) / red (-), điểm giữa xám.
  - Lưới/trục hairline, nhãn chữ dùng màu chữ (không dùng màu dữ liệu), số thập phân dấu phẩy.

Chạy: <python của venv> bao_cao/ve_hinh.py   -> bao_cao/hinh/*.png (200 dpi, rộng 16 cm)
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
from matplotlib.ticker import FuncFormatter, PercentFormatter  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SP = ROOT / "data" / "processed" / "spark"
OUT = ROOT / "bao_cao" / "hinh"

# ---- palette (references/palette.md) ----
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
BLUE_LIGHT, BLUE_DARK = "#86b6ef", "#1c5cab"
RED = "#e34948"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, NEUTRAL = "#e1e0d9", "#c3c2b7", "#f0efec"
DEEMPH = "#c3c2b7"
CUM = {  # màu theo thực thể (cụm), cố định; marker là kênh thứ 2
    "Đô thị – thu nhập cao": (BLUE, "o"),
    "Trung bình": (ORANGE, "s"),
    "Miền núi phía Bắc": (AQUA, "^"),
}
W = 16 / 2.54  # 16 cm

plt.rcParams.update({
    "font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 9,
    "text.color": INK, "axes.labelcolor": INK2, "axes.edgecolor": AXIS, "axes.linewidth": 0.8,
    "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK2, "ytick.labelcolor": INK2,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "grid.linestyle": "-",
    "axes.spines.top": False, "axes.spines.right": False, "axes.axisbelow": True,
    "axes.titlesize": 10, "axes.titleweight": "semibold", "axes.titlelocation": "left",
    "legend.frameon": False, "figure.dpi": 100, "savefig.dpi": 200, "savefig.facecolor": "white",
    "lines.linewidth": 2, "lines.solid_capstyle": "round",
})


def vn(x, nd=2):
    """Định dạng số kiểu Việt Nam: 1.234,5"""
    s = f"{x:,.{nd}f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def vn_fmt(nd=1):
    return FuncFormatter(lambda x, _: vn(x, nd))


def vn_pct(nd=0):
    return FuncFormatter(lambda x, _: vn(x * 100, nd) + "%")


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.png", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print(f"  [hinh] bao_cao/hinh/{name}.png")


def ten_cum():
    """Gán tên mô tả cho cụm k=3 theo thu nhập TB (không phụ thuộc số thứ tự KMeans)."""
    hs = pd.read_csv(SP / "ml_kmeans_k3_ho_so_cum.csv").sort_values("thu_nhap_bq_nguoi_thang")
    names = ["Miền núi phía Bắc", "Trung bình", "Đô thị – thu nhập cao"]
    return dict(zip(hs["cum"], names))


# ============================================================================ H3.1
def h3_1():
    d = pd.read_csv(SP / "co_diem_theo_mon.csv").sort_values("ty_le_sau")
    fig, ax = plt.subplots(figsize=(W, 3.6))
    y = np.arange(len(d))
    ax.hlines(y, d.ty_le_truoc, d.ty_le_sau, color=DEEMPH, lw=2, zorder=1)
    ax.scatter(d.ty_le_truoc, y, s=46, color=BLUE_LIGHT, edgecolor="white", lw=1.5, zorder=2,
               label="Đọc thẳng các cột điểm")
    ax.scatter(d.ty_le_sau, y, s=46, color=BLUE_DARK, edgecolor="white", lw=1.5, zorder=3,
               label="Sau khi giải mã và tách cột extra")
    for _, r in d.iterrows():
        if r.mon in ("toan", "ngu_van", "gdktpl", "lich_su"):
            ax.annotate(f"{vn(r.ty_le_truoc * 100, 1)}% → {vn(r.ty_le_sau * 100, 1)}%",
                        (r.ty_le_sau, y[d.index.get_loc(_)]), xytext=(8, 0),
                        textcoords="offset points", va="center", fontsize=8, color=INK2)
    ax.set_yticks(y, d.ten_mon)
    ax.xaxis.set_major_formatter(vn_pct())
    ax.set_xlim(0, 1.22)
    ax.set_xticks(np.arange(0, 1.01, 0.2))
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Tỷ lệ thí sinh có điểm môn")
    ax.legend(loc="lower right", fontsize=8)
    ax.set_title("Tỷ lệ thí sinh có điểm theo môn, trước và sau khi xử lý cột extra")
    save(fig, "H3_1_co_diem_truoc_sau")


# ============================================================================ H4.1
def h4_1():
    fig, ax = plt.subplots(figsize=(W, 3.3))
    ax.set_axis_off(); ax.set_xlim(0, 100); ax.set_ylim(0, 46)

    def box(x, y, w, h, title, body, fill="#f4f8fd", edge=BLUE_LIGHT):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                                    fc=fill, ec=edge, lw=1))
        ax.text(x + 1.5, y + h - 2.2, title, fontsize=8.5, weight="semibold", va="top")
        ax.text(x + 1.5, y + h - 7, body, fontsize=7, color=INK2, va="top", linespacing=1.35)

    def arrow(x0, y0, x1, y1):
        ax.annotate("", (x1, y1), (x0, y0), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1))

    grey = dict(fill="#f7f7f5", edge=AXIS)
    box(0, 25, 19, 20, "Điểm thi 2026", "34 CSV, 1,2 triệu dòng\n~115 MB (GitHub)", **grey)
    box(0, 1, 19, 20, "Niên giám TK 2025", "PDF 1.557 trang\nphụ lục 34 tỉnh", **grey)
    box(24, 25, 18, 20, "Bronze", "spark.read.csv\nlược đồ chuỗi\n+ cột nguồn file")
    box(24, 1, 18, 20, "Trích PDF", "pypdf layout mode\ngán cột theo vị trí\n→ bảng KT-XH 34 tỉnh", **grey)
    box(47, 25, 18, 20, "Silver", "pandas UDF (Arrow)\ngiải mã extra\ntry_cast, bỏ SBD")
    box(70, 25, 15, 20, "Gold", "tỉnh, tỉnh×môn\neta², tổ hợp\nphổ điểm")
    box(70, 1, 15, 20, "Ghép", "join ma_tinh\nkiểm 34/34\nđối chiếu pandas")
    box(88.5, 1, 11.5, 44, "MLlib", "Pipeline\nchuẩn hóa\n\nhồi quy\nk-fold\n\nKMeans\nsilhouette\n\nPCA")
    for (x0, y0, x1, y1) in [(19, 35, 24, 35), (42, 35, 47, 35), (65, 35, 70, 35),
                             (19, 11, 24, 11), (42, 11, 70, 11), (77.5, 25, 77.5, 21),
                             (85, 11, 88.5, 11)]:
        arrow(x0, y0, x1, y1)
    ax.text(0, -2.5, "Khối xanh: chạy trên Apache Spark (PySpark 4.0, local[*]).  Khối xám: nguồn và tiền xử lý ngoài Spark.",
            fontsize=7, color=MUTED, va="top")
    save(fig, "H4_1_pipeline")


# ============================================================================ H5.1
def h5_1():
    p = pd.read_csv(SP / "pho_diem.csv")
    ten = pd.read_csv(SP / "co_diem_theo_mon.csv").set_index("mon")["ten_mon"]
    cl = pd.read_csv(SP / "chenh_lech_giua_tinh_theo_mon.csv").set_index("mon")
    # Đề trắc nghiệm mới (đúng/sai, trả lời ngắn) cho điểm lẻ như 6,1; 7,35 -> KHÔNG lọc theo
    # bội 0,25 mà gom vào khoảng rộng 0,25 (tâm ở các mức 0; 0,25; ...; 10).
    p["bin"] = (p.diem * 4).round() / 4
    order = cl.sort_values("so_bai", ascending=False).index
    fig, axes = plt.subplots(4, 3, figsize=(W, 7.4), sharex=True)
    for ax, mon in zip(axes.flat, order):
        g = p[p.mon == mon].groupby("bin").so_bai.sum()
        g = g / g.sum()
        ax.bar(g.index, g.values, width=0.2, color=BLUE, lw=0)
        ax.set_title(f"{ten[mon]} · TB {vn(cl.loc[mon, 'tb_toan_quoc'])} · {vn(cl.loc[mon, 'so_bai'], 0)} bài",
                     fontsize=7)
        ax.yaxis.set_major_formatter(vn_pct())
        ax.grid(axis="x", visible=False)
        ax.tick_params(labelsize=7)
    last = axes.flat[-1]
    last.set_axis_off()
    last.text(0.02, 0.5, "Trục ngang: điểm (0–10)\nTrục dọc: % số bài của môn\nMỗi cột = khoảng rộng 0,25 điểm",
              fontsize=7.5, color=INK2, va="center", transform=last.transAxes)
    for ax in axes[-1]:
        ax.set_xticks(range(0, 11, 2))
    axes[-2, -1].tick_params(labelbottom=True)
    fig.suptitle("Phổ điểm toàn quốc theo môn, kỳ thi tốt nghiệp THPT 2026", x=0.01, ha="left",
                 fontsize=10, weight="semibold")
    fig.tight_layout()
    save(fig, "H5_1_pho_diem_mon")


# ============================================================================ H5.2
def h5_2():
    d = pd.read_csv(SP / "chenh_lech_giua_tinh_theo_mon.csv").sort_values("eta2")
    fig, ax = plt.subplots(figsize=(W, 3.6))
    y = np.arange(len(d))
    colors = [BLUE if m == "ngu_van" else BLUE_LIGHT for m in d.mon]  # nhấn mạnh 1 thanh
    ax.barh(y, d.eta2, height=0.6, color=colors)
    for yi, (v, lo, hi) in enumerate(zip(d.eta2, d.tinh_thap_nhat, d.tinh_cao_nhat)):
        ax.text(v + 0.002, yi, f"{vn(v * 100, 1)}%", va="center", fontsize=8, color=INK)
    ax.set_yticks(y, d.ten_mon)
    ax.xaxis.set_major_formatter(vn_pct())
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, d.eta2.max() * 1.15)
    ax.set_xticks(np.arange(0, 0.181, 0.03))
    ax.set_xlabel("eta² — tỷ lệ phương sai điểm thí sinh nằm ở chênh lệch giữa các tỉnh")
    ax.set_title("Ngữ văn là môn chênh lệch giữa các tỉnh nhiều nhất")
    save(fig, "H5_2_eta2_chenh_lech_mon")


# ============================================================================ H5.3
def h5_3():
    J = pd.read_csv(SP / "diemthi_x_ktxh_34tinh.csv")
    X = {"thu_nhap_bq_nguoi_thang": "Thu nhập BQ/người", "hdi": "HDI",
         "grdp_nguoi_2025": "GRDP/người", "ty_le_do_thi_pct": "Tỷ lệ đô thị",
         "ty_le_ld_qua_dao_tao": "LĐ qua đào tạo", "ty_le_dung_internet": "Dùng internet",
         "ty_le_ho_ngheo": "Tỷ lệ hộ nghèo", "hs_tren_gv_thpt": "HS/GV THPT"}
    Y = {"toan_tb": "Toán TB", "van_tb": "Văn TB", "anh_tb": "Ngoại ngữ TB",
         "diem_tb_chung": "Điểm TB chung", "ty_le_thi_ngoai_ngu": "Tỷ lệ thi\nNgoại ngữ",
         "ty_le_toan_duoi_5": "Tỷ lệ Toán\ndưới 5"}
    C = J[list(X) + list(Y)].corr(method="spearman").loc[list(X), list(Y)]
    C.round(3).to_csv(SP / "tuong_quan_spearman.csv")
    cmap = LinearSegmentedColormap.from_list("div", ["#a3302f", RED, NEUTRAL, BLUE, BLUE_DARK])
    fig, ax = plt.subplots(figsize=(W, 3.9))
    im = ax.imshow(C.values, cmap=cmap, vmin=-1, vmax=1, aspect="auto")
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    for i in range(C.shape[0]):
        for j in range(C.shape[1]):
            v = C.values[i, j]
            ax.text(j, i, vn(v), ha="center", va="center", fontsize=8,
                    color="white" if abs(v) >= 0.5 else INK)
    ax.set_xticks(range(len(Y)), Y.values(), fontsize=8)
    ax.set_yticks(range(len(X)), X.values(), fontsize=8)
    ax.tick_params(length=0)
    ax.xaxis.tick_top()
    # khe trắng 2px giữa các ô
    ax.set_xticks(np.arange(-0.5, len(Y)), minor=True); ax.set_yticks(np.arange(-0.5, len(X)), minor=True)
    ax.grid(which="minor", color="white", lw=2); ax.tick_params(which="minor", length=0)
    cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02, ticks=[-1, -0.5, 0, 0.5, 1])
    cb.ax.yaxis.set_major_formatter(vn_fmt(1)); cb.outline.set_visible(False)
    cb.ax.tick_params(labelsize=7, length=0)
    ax.set_title("Tương quan hạng Spearman giữa chỉ tiêu KT-XH và kết quả thi (34 tỉnh)", pad=34)
    save(fig, "H5_3_heatmap_spearman")


# ============================================================================ H5.4
def h5_4():
    J = pd.read_csv(SP / "diemthi_x_ktxh_34tinh.csv", dtype={"ma_tinh": str})
    g = pd.read_csv(SP / "ml_kmeans_k3_cum_tinh.csv", dtype={"ma_tinh": str})[["ma_tinh", "cum"]]
    J = J.merge(g, on="ma_tinh")
    J["ten_cum"] = J.cum.map(ten_cum())
    kf = pd.read_csv(SP / "ml_hoi_quy_kfold.csv").query("mo_hinh == 'M1_thu_nhap'").set_index("bien_phu_thuoc")
    x = J.thu_nhap_bq_nguoi_thang / 1000  # triệu đồng
    fig, axes = plt.subplots(1, 2, figsize=(W, 3.7), sharey=True)
    for ax, (col, lab) in zip(axes, [("toan_tb", "Toán"), ("van_tb", "Ngữ văn")]):
        b = np.polyfit(np.log(x), J[col], 1)
        xs = np.linspace(x.min(), x.max(), 100)
        ax.plot(xs, np.polyval(b, np.log(xs)), color=MUTED, lw=1.2, zorder=1)
        for name, (c, m) in CUM.items():
            s = J.ten_cum == name
            ax.scatter(x[s], J.loc[s, col], s=40, color=c, marker=m, edgecolor="white", lw=1.2,
                       zorder=3, label=f"{name} ({s.sum()})")
        resid = J[col] - np.polyval(b, np.log(x))
        nhan = set(J.loc[resid.abs().nlargest(3).index, "ten_tinh"]) | \
            set(J.loc[x.nlargest(1).index, "ten_tinh"]) | set(J.loc[x.nsmallest(1).index, "ten_tinh"])
        for i, r in J[J.ten_tinh.isin(nhan)].iterrows():
            ax.annotate(r.ten_tinh, (x[i], r[col]), xytext=(4, 3), textcoords="offset points",
                        fontsize=7, color=INK2)
        ax.set_xscale("log")
        ax.set_xticks([3, 4, 5, 6, 8, 10], ["3", "4", "5", "6", "8", "10"])
        ax.minorticks_off()
        ax.set_title(f"{lab}  ·  R² ngoài mẫu (5-fold) = {vn(kf.loc[col, 'r2_cv_tb'])}", fontsize=9)
        ax.yaxis.set_major_formatter(vn_fmt(1))
    axes[0].set_ylabel("Điểm trung bình tỉnh")
    axes[1].tick_params(labelleft=True)
    fig.supxlabel("Thu nhập BQ/người/tháng 2025 (triệu đồng, thang log)", fontsize=9, color=INK2, y=0.06)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, fontsize=8, bbox_to_anchor=(0.5, -0.04))
    fig.suptitle("Thu nhập giải thích tốt điểm Toán nhưng gần như không giải thích điểm Văn",
                 x=0.01, ha="left", fontsize=10, weight="semibold")
    fig.tight_layout()
    save(fig, "H5_4_thu_nhap_toan_van")


# ============================================================================ H5.5
def h5_5():
    g = pd.read_csv(SP / "ml_kmeans_k3_cum_tinh.csv", dtype={"ma_tinh": str})
    g["ten_cum"] = g.cum.map(ten_cum())
    tai = pd.read_csv(SP / "ml_pca_tai.csv").set_index("bien")
    ev = tai.loc["__ty_le_phuong_sai__"]
    fig, ax = plt.subplots(figsize=(W, 4.2))
    for name, (c, m) in CUM.items():
        s = g[g.ten_cum == name]
        ax.scatter(s.pc1, s.pc2, s=46, color=c, marker=m, edgecolor="white", lw=1.2, zorder=3,
                   label=f"{name} ({len(s)} tỉnh)")
    # nhãn có chọn lọc: các điểm xa tâm nhất
    dist = np.hypot(g.pc1, g.pc2)
    for _, r in g.loc[dist.nlargest(12).index].iterrows():
        ax.annotate(r.ten_tinh, (r.pc1, r.pc2), xytext=(4, 3), textcoords="offset points", fontsize=7, color=INK2)
    ax.axhline(0, color=AXIS, lw=0.8, zorder=1); ax.axvline(0, color=AXIS, lw=0.8, zorder=1)
    ax.set_xlabel(f"Thành phần chính 1 ({vn(ev.pc1 * 100, 0)}% phương sai)")
    ax.set_ylabel(f"Thành phần chính 2 ({vn(ev.pc2 * 100, 0)}% phương sai)")
    ax.xaxis.set_major_formatter(vn_fmt(0)); ax.yaxis.set_major_formatter(vn_fmt(0))
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=3, fontsize=8)
    ax.set_title("Phân cụm KMeans (k = 3) 34 tỉnh, chiếu lên 2 thành phần chính")
    save(fig, "H5_5_kmeans_pca")


# ============================================================================ H5.6
def h5_6():
    """Mức 5,0 môn Văn so với các mức cùng độ chẵn 4,5 và 5,5.

    Văn có thói quen chấm theo nửa điểm: mức x,0/x,5 luôn cao hơn x,25/x,75 kề bên, nên so 5,0
    với 4,75/5,25 sẽ phóng đại hiện tượng -> mốc là TB(4,5; 5,5). Tỷ số 1 = không có đỉnh.
    """
    p = pd.read_csv(SP / "pho_diem.csv", dtype={"ma_tinh": str})
    ten = pd.read_csv(SP / "diemthi_theo_tinh.csv", dtype={"ma_tinh": str}).set_index("ma_tinh")["ten_tinh"]
    v = p[(p.mon == "ngu_van") & ((p.diem * 4).round(6) % 1 == 0)]
    tq = v.groupby("diem").so_bai.sum(); tq = tq / tq.sum()
    w = v.pivot_table(index="ma_tinh", columns="diem", values="so_bai", fill_value=0)
    w = w.div(w.sum(axis=1), axis=0)

    def ti_so(f, d):
        return f[d] / ((f[d - 0.5] + f[d + 0.5]) / 2)

    ts = ti_so(w, 5.0).rename("ti_so").to_frame()
    ts["ten"] = ts.index.map(ten)
    ts = ts.sort_values("ti_so")
    tq_ts = ti_so(tq, 5.0)
    print(f"  [Van 5,0] toàn quốc {tq_ts:.2f}; đối chứng 4,5: {ti_so(tq, 4.5):.2f}, "
          f"5,5: {ti_so(tq, 5.5):.2f}, 6,0: {ti_so(tq, 6.0):.2f}")
    pd.DataFrame({"ma_tinh": ts.index, "ten_tinh": ts.ten, "ty_le_4_5": w.loc[ts.index, 4.5],
                  "ty_le_5": w.loc[ts.index, 5.0], "ty_le_5_5": w.loc[ts.index, 5.5],
                  "ti_so_dinh_5": ts.ti_so}).to_csv(SP / "van_dinh_5_theo_tinh.csv", index=False)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(W, 5.2), gridspec_kw=dict(width_ratios=[1.1, 1]))
    z = tq.loc[2.0:8.0]
    mau = [BLUE if d == 5.0 else (BLUE_LIGHT if (d * 2) % 1 == 0 else "#cde2fb") for d in z.index]
    a1.bar(z.index, z.values, width=0.2, color=mau, lw=0)
    a1.annotate(f"5,0 điểm: {vn(tq[5.0] * 100, 1)}%\n(4,5: {vn(tq[4.5] * 100, 1)}%;  5,5: {vn(tq[5.5] * 100, 1)}%)",
                (5.0, tq[5.0]), xytext=(-95, 30), textcoords="offset points", fontsize=7.5, color=INK2,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    a1.text(0.02, 0.98, "Cột xanh vừa: mức x,0 và x,5\nCột nhạt: mức x,25 và x,75", transform=a1.transAxes,
            fontsize=7, color=INK2, va="top")
    a1.yaxis.set_major_formatter(vn_pct()); a1.grid(axis="x", visible=False)
    a1.set_xlabel("Điểm Ngữ văn (đoạn 2–8)")
    a1.set_title("Toàn quốc: % bài theo mức điểm", fontsize=9)

    y = np.arange(len(ts))
    a2.barh(y, ts.ti_so, height=0.62, color=BLUE)
    a2.axvline(1, color=INK2, lw=1)
    a2.axvline(tq_ts, color=MUTED, lw=1)
    a2.text(tq_ts, len(ts) - 0.2, f" toàn quốc {vn(tq_ts)}", fontsize=7, color=INK2, va="bottom")
    a2.text(1, -1.6, "1 = không có đỉnh ", fontsize=7, color=INK2, ha="right", va="bottom")
    a2.set_yticks(y, ts.ten, fontsize=6.5)
    a2.set_ylim(-1.8, len(ts) + 0.6)
    a2.xaxis.set_major_formatter(vn_fmt(1)); a2.grid(axis="y", visible=False)
    a2.set_xlabel("Tỷ số: % bài đúng 5,0 / TB(% ở 4,5 và 5,5)")
    a2.set_title("Theo tỉnh: độ nhô của mức 5,0", fontsize=9)
    fig.suptitle("Ngữ văn: số bài dồn ở đúng 5,0 điểm (quan sát thống kê)", x=0.01, ha="left",
                 fontsize=10, weight="semibold")
    fig.tight_layout()
    save(fig, "H5_6_van_dinh_5")


if __name__ == "__main__":
    chon = sys.argv[1:] or ["h3_1", "h4_1", "h5_1", "h5_2", "h5_3", "h5_4", "h5_5", "h5_6"]
    for f in chon:
        globals()[f]()
