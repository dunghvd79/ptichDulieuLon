/**
 * Dựng báo cáo Word từ bao_cao/bao_cao.md.
 *
 *   cd bao_cao && npm install && node build_docx.js
 *   -> bao_cao/BaoCao_DiemThi2026_KTXH.docx
 *
 * Cú pháp riêng trong bao_cao.md:
 *   @bang <chú thích>            chú thích cho bảng ngay bên dưới (tự đánh số theo chương)
 *   @hinh <file.png> | <chú thích>  chèn hình từ bao_cao/hinh/ (tự đánh số theo chương)
 *   @ref <tài liệu>              một mục tài liệu tham khảo (thụt dòng treo)
 * Chỗ cần người dùng tự điền được in đậm trong ngoặc vuông: [ ... ].
 */
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType,
  AlignmentType, HeadingLevel, ShadingType, BorderStyle, PageNumber, Footer, TableOfContents,
  StyleLevel, LevelFormat, PageBreak, VerticalAlign, NumberFormat,
} = require("docx");

const DIR = __dirname;
const MD = fs.readFileSync(path.join(DIR, "bao_cao.md"), "utf8").replace(/\r\n/g, "\n");
const OUT = path.join(DIR, "BaoCao_DiemThi2026_KTXH.docx");

// ------------------------------------------------------------------ hằng số trình bày
const FONT = "Times New Roman";
const SZ = 26;                       // 13 pt (đơn vị nửa point)
const CM = 567;                      // 1 cm = 567 DXA
const TEXT_W = 16 * CM;              // A4 21 cm - lề trái 3 cm - lề phải 2 cm
const PAGE = {
  size: { width: 11906, height: 16838 },
  margin: { top: 2 * CM, bottom: 2 * CM, left: 3 * CM, right: 2 * CM },
};
const HEADER_FILL = "DCE6F2";
const COVER_TITLE =
  "TÍCH HỢP DỮ LIỆU ĐIỂM THI TỐT NGHIỆP THPT 2026 VỚI ĐIỀU KIỆN KINH TẾ – XÃ HỘI CỦA 34 TỈNH, THÀNH PHỐ VÀ PHÂN TÍCH BẰNG APACHE SPARK";

// ------------------------------------------------------------------ chữ trong dòng
/** "**đậm** *nghiêng* `mã`" -> TextRun[]; chuỗi [..] trong ngoặc vuông được in đậm (chỗ cần điền). */
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*\s][^*]*?\*|`[^`]+`)/g;
  let last = 0, m;
  const push = (t, extra = {}) => { if (t) out.push(new TextRun({ text: t, font: FONT, ...base, ...extra })); };
  while ((m = re.exec(text))) {
    push(text.slice(last, m.index));
    const tok = m[0];
    if (tok.startsWith("**")) push(tok.slice(2, -2), { bold: true });
    else if (tok.startsWith("`")) push(tok.slice(1, -1), { font: "Consolas", size: (base.size || SZ) - 4 });
    else push(tok.slice(1, -1), { italics: true });
    last = m.index + tok.length;
  }
  push(text.slice(last));
  return out;
}
const ph = (t, extra = {}) => new TextRun({ text: t, bold: true, font: FONT, ...extra }); // chỗ cần điền

// ------------------------------------------------------------------ đánh số danh sách
let listInstance = 0;
const numberingConfig = [
  {
    reference: "bullets",
    levels: [0, 1].map((lv) => ({
      level: lv, format: LevelFormat.BULLET, text: lv === 0 ? "•" : "–", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720 + lv * 360, hanging: 360 } } },
    })),
  },
  {
    reference: "numbers",
    levels: [{
      level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } },
    }],
  },
];

// ------------------------------------------------------------------ hình
function pngSize(file) {
  const b = fs.readFileSync(file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20), data: b };
}
const counters = { hinh: 0, bang: 0 };
let chapter = "";      // "1".."7", "A", "B" hoặc "" (phần không đánh số)
const figList = [];

function figure(file, caption) {
  const { w, h, data } = pngSize(path.join(DIR, "hinh", file));
  const widthPx = Math.round((16 / 2.54) * 96);
  counters.hinh += 1;
  const label = `Hình ${chapter}.${counters.hinh}. `;
  figList.push(label + caption);
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 120, after: 60 },
      children: [new ImageRun({ type: "png", data, transformation: { width: widthPx, height: Math.round(widthPx * h / w) } })],
    }),
    new Paragraph({ style: "HinhCaption", children: [new TextRun({ text: label, bold: true }), ...runs(caption)] }),
  ];
}

function tableCaption(caption) {
  counters.bang += 1;
  return new Paragraph({
    style: "BangCaption",
    children: [new TextRun({ text: `Bảng ${chapter}.${counters.bang}. `, bold: true }), ...runs(caption)],
  });
}

// ------------------------------------------------------------------ bảng
function splitRow(line) {
  return line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());
}
function mdTable(lines) {
  const rows = lines.filter((l) => !/^\|\s*-/.test(l)).map(splitRow);
  const n = rows[0].length;
  const long = rows.length > 30;          // bảng dài (phụ lục 34 tỉnh): chữ nhỏ, đệm ít để vừa một trang
  const size = long ? 16 : n >= 8 ? 18 : 22;   // 8 / 9 / 11 pt
  const pad = long ? 10 : 40;
  // độ rộng cột theo độ dài chữ dài nhất (có chặn trên/dưới)
  const len = Array.from({ length: n }, (_, j) =>
    Math.min(42, Math.max(4, ...rows.map((r) => (r[j] || "").replace(/\*\*/g, "").length))));
  const total = len.reduce((a, b) => a + b, 0);
  const widths = len.map((x) => Math.floor((x / total) * TEXT_W));
  widths[n - 1] += TEXT_W - widths.reduce((a, b) => a + b, 0);
  const border = { style: BorderStyle.SINGLE, size: 4, color: "808080" };
  const borders = { top: border, bottom: border, left: border, right: border };
  return new Table({
    width: { size: TEXT_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: rows.map((r, i) => new TableRow({
      tableHeader: i === 0,
      cantSplit: true,
      children: widths.map((wd, j) => new TableCell({
        width: { size: wd, type: WidthType.DXA },
        borders,
        verticalAlign: VerticalAlign.CENTER,
        shading: i === 0 ? { fill: HEADER_FILL, type: ShadingType.CLEAR, color: "auto" } : undefined,
        margins: { top: pad, bottom: pad, left: 80, right: 80 },
        children: [new Paragraph({
          alignment: i === 0 ? AlignmentType.CENTER : AlignmentType.LEFT,
          spacing: { before: 0, after: 0, line: long ? 228 : 264 },
          children: runs(r[j] || "", { size, bold: i === 0 ? true : undefined }),
        })],
      })),
    })),
  });
}

// ------------------------------------------------------------------ chuyển markdown -> các khối Word
function convert(md) {
  const L = md.split("\n");
  const blocks = [];
  let i = 0;
  let para = [];
  const flush = () => {
    if (para.length) blocks.push(new Paragraph({ children: runs(para.join(" ")) }));
    para = [];
  };
  while (i < L.length) {
    const line = L[i];
    const t = line.trim();
    if (!t || /^-{3,}$/.test(t)) { flush(); i++; continue; }   // dòng trống / đường kẻ phân cách

    let m;
    if ((m = /^(#{1,4}) (.*)$/.exec(line))) {
      flush();
      const level = m[1].length;
      let text = m[2];
      if (level === 1) {
        const c = /^Chương (\d+)\./.exec(text) || /^Phụ lục ([A-Z])\./.exec(text);
        chapter = c ? c[1] : "";
        counters.hinh = 0; counters.bang = 0;
      }
      const H = [HeadingLevel.HEADING_1, HeadingLevel.HEADING_2, HeadingLevel.HEADING_3, HeadingLevel.HEADING_4][level - 1];
      blocks.push(new Paragraph({ heading: H, children: runs(text) }));
      i++; continue;
    }
    if (t.startsWith("```")) {
      flush();
      i++;
      const code = [];
      while (i < L.length && !L[i].trim().startsWith("```")) code.push(L[i++]);
      i++;
      code.forEach((c, k) => blocks.push(new Paragraph({
        keepNext: k < code.length - 1, keepLines: true,   // giữ cả khối trên cùng một trang
        shading: { fill: "F2F2F2", type: ShadingType.CLEAR, color: "auto" },
        spacing: { before: k === 0 ? 120 : 0, after: k === code.length - 1 ? 160 : 0, line: 240 },
        alignment: AlignmentType.LEFT,
        children: [new TextRun({ text: c.length ? c : " ", font: "Consolas", size: 17 })],
      })));
      continue;
    }
    if (t.startsWith("@bang ")) { flush(); blocks.push(tableCaption(t.slice(6))); i++; continue; }
    if (t.startsWith("@hinh ")) {
      flush();
      const [file, cap] = t.slice(6).split("|").map((s) => s.trim());
      blocks.push(...figure(file, cap));
      i++; continue;
    }
    if (t.startsWith("@ref ")) {
      flush();
      blocks.push(new Paragraph({ indent: { left: 720, hanging: 720 }, alignment: AlignmentType.LEFT, children: runs(t.slice(5)) }));
      i++; continue;
    }
    if (t.startsWith("|")) {
      flush();
      const tl = [];
      while (i < L.length && L[i].trim().startsWith("|")) tl.push(L[i++]);
      blocks.push(mdTable(tl));
      blocks.push(new Paragraph({ spacing: { before: 0, after: 120 }, children: [] }));
      continue;
    }
    if (t.startsWith(">")) {
      flush();
      const q = [];
      while (i < L.length && L[i].trim().startsWith(">")) { q.push(L[i].trim().replace(/^>\s?/, "")); i++; }
      q.filter((x) => x).forEach((x) => blocks.push(new Paragraph({
        indent: { left: 567, right: 284 },
        border: { left: { style: BorderStyle.SINGLE, size: 12, color: "86B6EF", space: 8 } },
        children: runs(x, { italics: true }),
      })));
      continue;
    }
    if ((m = /^(\s*)- (.*)$/.exec(line))) {
      flush();
      blocks.push(new Paragraph({ numbering: { reference: "bullets", level: m[1].length >= 2 ? 1 : 0 }, children: runs(m[2]) }));
      i++; continue;
    }
    if ((m = /^\d+\. (.*)$/.exec(t))) {
      flush();
      listInstance += 1;
      const inst = listInstance;
      while (i < L.length && (m = /^\d+\. (.*)$/.exec(L[i].trim()))) {
        blocks.push(new Paragraph({ numbering: { reference: "numbers", level: 0, instance: inst }, children: runs(m[1]) }));
        i++;
      }
      continue;
    }
    para.push(t);
    i++;
  }
  flush();
  return blocks;
}

// ------------------------------------------------------------------ phần đầu: bìa, phân công, cảm ơn, mục lục
function center(text, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { before: opts.before || 0, after: opts.after || 0, line: 300 },
    children: Array.isArray(text) ? text : [new TextRun({ text, font: FONT, bold: opts.bold, size: opts.size || SZ })],
  });
}
function infoTable(rows) {
  const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
  const b = { top: none, bottom: none, left: none, right: none };
  const W = [Math.round(TEXT_W * 0.42), TEXT_W - Math.round(TEXT_W * 0.42)];
  return new Table({
    width: { size: TEXT_W, type: WidthType.DXA }, columnWidths: W,
    rows: rows.map(([a, bRuns]) => new TableRow({
      children: [
        new TableCell({ width: { size: W[0], type: WidthType.DXA }, borders: b,
          children: [new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: a, font: FONT, size: SZ })] })] }),
        new TableCell({ width: { size: W[1], type: WidthType.DXA }, borders: b,
          children: [new Paragraph({ spacing: { after: 60 }, children: bRuns })] }),
      ],
    })),
  });
}
function coverPage() {
  return [
    center("ĐẠI HỌC PHENIKAA", { bold: true, size: 28 }),
    center("TRƯỜNG CÔNG NGHỆ THÔNG TIN", { bold: true, size: 28 }),
    center("───────────────", { after: 360 }),
    new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { before: 240, after: 600 },
      border: {
        top: { style: BorderStyle.DASHED, size: 6, color: "999999", space: 24 },
        bottom: { style: BorderStyle.DASHED, size: 6, color: "999999", space: 24 },
      },
      children: [ph("[Chèn logo Đại học Phenikaa]", { size: 24, color: "666666" })],
    }),
    center("BÁO CÁO ĐỒ ÁN CUỐI KỲ", { bold: true, size: 32, after: 120 }),
    center("HỌC PHẦN: TÍCH HỢP VÀ PHÂN TÍCH DỮ LIỆU LỚN", { bold: true, size: 26, after: 600 }),
    center("ĐỀ TÀI", { bold: true, size: 26, after: 120 }),
    center(COVER_TITLE, { bold: true, size: 30, after: 900 }),
    infoTable([
      ["Giảng viên hướng dẫn:", [ph("[TS. Nguyễn Văn A]")]],
      ["Mã học phần – Lớp:", [ph("[Mã học phần]"), new TextRun({ text: " – ", font: FONT }), ph("[Lớp]")]],
      ["Nhóm sinh viên thực hiện:", [ph("[Họ tên sinh viên 1] – [MSSV 1]")]],
      ["", [ph("[Họ tên sinh viên 2] – [MSSV 2]")]],
      ["", [ph("[Họ tên sinh viên 3] – [MSSV 3]")]],
    ]),
    center([new TextRun({ text: "Hà Nội, tháng ", font: FONT, size: SZ }), ph("[11]"),
      new TextRun({ text: " năm 2026", font: FONT, size: SZ })], { before: 1200 }),
  ];
}
function frontTitle(text) { // tiêu đề phần đầu: vào mục lục như chương nhưng không đánh số
  return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(text)] });
}
function plainTitle(text) { // tiêu đề không vào mục lục (Mục lục, Danh mục…)
  return new Paragraph({ style: "TitleNoToc", pageBreakBefore: true, children: [new TextRun(text)] });
}
function gridTable(header, rows, ratios) {
  return mdTable(["| " + header.join(" | ") + " |", "|" + header.map(() => "---").join("|") + "|",
    ...rows.map((r) => "| " + r.join(" | ") + " |")]);
}
function frontMatter() {
  const pc = [
    frontTitle("Bảng phân công nhiệm vụ"),
    new Paragraph({ children: runs("Bảng dưới đây ghi nhận nhiệm vụ và mức độ đóng góp của từng thành viên trong nhóm.") }),
    gridTable(["STT", "Họ và tên", "MSSV", "Nhiệm vụ chính", "Đóng góp"], [
      ["1", "**[Họ tên sinh viên 1]**", "**[MSSV 1]**", "**[Thu thập và tích hợp dữ liệu, xây dựng pipeline Spark]**", "**[34%]**"],
      ["2", "**[Họ tên sinh viên 2]**", "**[MSSV 2]**", "**[Phân tích bằng Spark MLlib, trực quan hóa kết quả]**", "**[33%]**"],
      ["3", "**[Họ tên sinh viên 3]**", "**[MSSV 3]**", "**[Viết báo cáo, chuẩn bị slide thuyết trình]**", "**[33%]**"],
    ]),
    new Paragraph({ children: [] }),
    frontTitle("Lời cảm ơn"),
    new Paragraph({ children: runs("Nhóm em xin chân thành cảm ơn **[TS. Nguyễn Văn A]**, giảng viên học phần Tích hợp và phân tích dữ liệu lớn, đã tận tình hướng dẫn và góp ý trong suốt quá trình thực hiện đồ án.") }),
    new Paragraph({ children: runs("Nhóm em cũng xin cảm ơn Trường Công nghệ Thông tin, Đại học Phenikaa đã tạo điều kiện học tập và nghiên cứu; cảm ơn Cục Thống kê đã công bố Niên giám thống kê 2025 và cộng đồng đã chia sẻ dữ liệu điểm thi, giúp đồ án có nguồn số liệu để thực hiện.") }),
    new Paragraph({ children: runs("Do thời gian và kiến thức còn hạn chế, báo cáo khó tránh khỏi thiếu sót. Nhóm em rất mong nhận được ý kiến góp ý của thầy cô để hoàn thiện hơn.") }),
    new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { before: 240 }, children: runs("*Hà Nội, tháng* **[11]** *năm 2026*") }),
    new Paragraph({ alignment: AlignmentType.RIGHT, children: runs("*Nhóm sinh viên thực hiện*") }),

    plainTitle("MỤC LỤC"),
    new TableOfContents("Mục lục", { hyperlink: true, headingStyleRange: "1-3" }),
    plainTitle("DANH MỤC HÌNH"),
    new TableOfContents("Danh mục hình", { hyperlink: true, stylesWithLevels: [new StyleLevel("HinhCaption", 1)] }),
    plainTitle("DANH MỤC BẢNG"),
    new TableOfContents("Danh mục bảng", { hyperlink: true, stylesWithLevels: [new StyleLevel("BangCaption", 1)] }),

    frontTitle("Danh mục chữ viết tắt"),
    gridTable(["Viết tắt", "Ý nghĩa"], [
      ["CSV", "Định dạng tệp dữ liệu dạng bảng, các giá trị cách nhau bằng dấu phẩy (Comma-Separated Values)"],
      ["GD KT&PL", "Giáo dục kinh tế và pháp luật"],
      ["GRDP", "Tổng sản phẩm trên địa bàn tỉnh (Gross Regional Domestic Product)"],
      ["HDI", "Chỉ số phát triển con người (Human Development Index)"],
      ["HS/GV", "Số học sinh trên một giáo viên"],
      ["KT-XH", "Kinh tế – xã hội"],
      ["MLlib", "Thư viện học máy của Apache Spark"],
      ["NN", "Ngoại ngữ"],
      ["PCA", "Phân tích thành phần chính (Principal Component Analysis)"],
      ["PDF", "Định dạng tài liệu di động (Portable Document Format)"],
      ["SBD", "Số báo danh"],
      ["TB", "Trung bình"],
      ["THPT", "Trung học phổ thông"],
      ["UDF", "Hàm do người dùng tự định nghĩa (User-Defined Function)"],
      ["VIF", "Hệ số phóng đại phương sai (Variance Inflation Factor)"],
    ]),
  ];
  return pc;
}

// ------------------------------------------------------------------ tài liệu
const footer = (fmt) => new Footer({
  children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 24 })] })],
});
const body = convert(MD);

const heading = (size, extra = {}) => ({
  run: { font: FONT, size, bold: true, color: "000000", ...extra.run },
  paragraph: { spacing: { before: extra.before ?? 240, after: extra.after ?? 120, line: 300 }, keepNext: true, keepLines: true, ...extra.paragraph },
});

const doc = new Document({
  creator: "Nhóm sinh viên",
  title: "Báo cáo đồ án: Điểm thi THPT 2026 và điều kiện kinh tế – xã hội 34 tỉnh",
  // Không bật features.updateFields: Word sẽ hiện hộp thoại khi mở. Mục lục được cập nhật
  // bằng cap_nhat_word.ps1 (Word COM) rồi lưu sẵn vào file.
  numbering: { config: numberingConfig },
  styles: {
    default: {
      document: { run: { font: FONT, size: SZ }, paragraph: { spacing: { after: 120, line: 360 }, alignment: AlignmentType.JUSTIFIED } },
      heading1: heading(28, { before: 0, after: 360, paragraph: { alignment: AlignmentType.CENTER, pageBreakBefore: true }, run: { allCaps: true } }),
      heading2: heading(SZ, { before: 240, after: 120 }),
      heading3: heading(SZ, { before: 180, after: 80, run: { italics: true } }),
      heading4: heading(SZ, { before: 120, after: 60, run: { bold: false, italics: true } }),
    },
    paragraphStyles: [
      // name phải trùng id: trường TOC \t của Word tìm theo TÊN kiểu chữ
      { id: "HinhCaption", name: "HinhCaption", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 24, italics: true }, paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 60, after: 240, line: 276 } } },
      { id: "BangCaption", name: "BangCaption", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 24, italics: true }, paragraph: { alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 180, after: 80, line: 276 } } },
      { id: "TitleNoToc", name: "Title No Toc", basedOn: "Normal", next: "Normal",
        run: { font: FONT, size: 28, bold: true }, paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 0, after: 360 } } },
    ],
  },
  sections: [
    { // bìa: không số trang, có khung viền
      properties: {
        page: {
          ...PAGE,
          borders: {
            pageBorderTop: { style: BorderStyle.DOUBLE, size: 12, color: "1C5CAB", space: 24 },
            pageBorderBottom: { style: BorderStyle.DOUBLE, size: 12, color: "1C5CAB", space: 24 },
            pageBorderLeft: { style: BorderStyle.DOUBLE, size: 12, color: "1C5CAB", space: 24 },
            pageBorderRight: { style: BorderStyle.DOUBLE, size: 12, color: "1C5CAB", space: 24 },
          },
        },
      },
      children: coverPage(),
    },
    { // phần đầu: số trang i, ii, iii
      properties: { page: { ...PAGE, pageNumbers: { start: 1, formatType: NumberFormat.LOWER_ROMAN } } },
      footers: { default: footer() },
      children: frontMatter(),
    },
    { // thân bài: số trang 1, 2, 3
      properties: { page: { ...PAGE, pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } } },
      footers: { default: footer() },
      children: body,
    },
  ],
});

// Kiểm tra: số hình trong văn bản phải khớp với số tự đánh
const expected = ["3.1", "4.1", "5.1", "5.2", "5.3", "5.4", "5.5", "5.6"];
const got = figList.map((f) => /^Hình (\S+)\./.exec(f)[1]);
if (JSON.stringify(got) !== JSON.stringify(expected)) {
  console.error("Số hình không khớp:", got); process.exit(1);
}

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log(`[docx] ${path.basename(OUT)}: ${figList.length} hình, ${MD.split("@bang").length - 1} bảng trong nội dung + 3 bảng phần đầu`);
});
