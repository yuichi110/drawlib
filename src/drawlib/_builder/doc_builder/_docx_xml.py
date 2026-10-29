# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""OpenXML and CSS theme helpers for python-docx Word (.docx) export."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from docx.document import Document as DocxDocument
    from docx.table import Table, _Cell, _Row
    from docx.text.paragraph import Paragraph
    from docx.text.run import Run

_GENERIC_FONT_NAMES: frozenset[str] = frozenset(
    {
        "-apple-system",
        "blinkmacsystemfont",
        "system-ui",
        "sans-serif",
        "serif",
        "monospace",
        "ui-monospace",
        "ui-sans-serif",
        "sfmono-regular",
    }
)

_CJK_FONT_KEYWORDS: tuple[str, ...] = (
    "noto sans jp",
    "noto sans cjk",
    "noto sans sc",
    "noto sans tc",
    "noto sans kr",
    "noto sans thai",
    "yu gothic",
    "hiragino",
    "meiryo",
    "ms pgothic",
)


@dataclass(frozen=True)
class DocxTheme:
    """Resolved typography and color palette for a Word (.docx) document."""

    brand_color: tuple[int, int, int] = (26, 115, 232)
    heading_color: tuple[int, int, int] = (32, 33, 36)
    text_color: tuple[int, int, int] = (60, 64, 67)
    muted_color: tuple[int, int, int] = (95, 99, 104)
    border_hex: str = "DADCE0"
    surface_bg_hex: str = "F8F9FA"
    code_bg_hex: str = "F8F9FA"
    inline_code_bg_hex: str = "F1F3F4"
    inline_code_color: tuple[int, int, int] = (24, 90, 188)
    note_bg_hex: str = "F8F9FA"
    note_border_hex: str = "1A73E8"
    code_keyword: tuple[int, int, int] = (26, 115, 232)
    code_string: tuple[int, int, int] = (30, 142, 62)
    code_comment: tuple[int, int, int] = (128, 134, 139)
    code_number: tuple[int, int, int] = (217, 119, 6)
    code_function: tuple[int, int, int] = (217, 48, 37)
    code_type: tuple[int, int, int] = (147, 52, 230)
    code_operator: tuple[int, int, int] = (95, 99, 104)
    code_builtin: tuple[int, int, int] = (26, 115, 232)
    latin_font: str = "Segoe UI"
    heading_font: str = "Segoe UI"
    east_asia_font: str = "Noto Sans JP"
    mono_font: str = "Consolas"


def import_docx() -> Any:  # noqa: ANN401
    """Lazy-import python-docx with an actionable error message if missing."""
    try:
        import docx

        return docx
    except ImportError as err:
        msg = (
            "MS Word (.docx) export requires the 'python-docx' package.\n"
            "Please install it via:\n"
            "  uv add python-docx\n"
            "or:\n"
            "  pip install python-docx"
        )
        raise RuntimeError(msg) from err


def _parse_hex_rgb(val: str) -> tuple[int, int, int] | None:
    """Parse #RGB or #RRGGBB CSS color value into an (R, G, B) tuple."""
    clean = val.strip()
    if clean.startswith("#"):
        hex_part = clean[1:].strip()
        if len(hex_part) == 3 and all(c in "0123456789abcdefABCDEF" for c in hex_part):
            return (
                int(hex_part[0] * 2, 16),
                int(hex_part[1] * 2, 16),
                int(hex_part[2] * 2, 16),
            )
        if len(hex_part) >= 6 and all(c in "0123456789abcdefABCDEF" for c in hex_part[:6]):
            return (
                int(hex_part[0:2], 16),
                int(hex_part[2:4], 16),
                int(hex_part[4:6], 16),
            )
    rgb_match = re.match(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", clean, re.IGNORECASE)
    if rgb_match:
        return (
            min(255, int(rgb_match.group(1))),
            min(255, int(rgb_match.group(2))),
            min(255, int(rgb_match.group(3))),
        )
    return None


def _rgb_to_hex6(rgb: tuple[int, int, int]) -> str:
    """Format an (R, G, B) tuple as an uppercase 6-char hex string."""
    return f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


def _luminance(rgb: tuple[int, int, int]) -> float:
    """Compute perceived luminance in [0.0, 1.0]."""
    return (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255.0


def _split_css_font_list(raw: str) -> list[str]:
    """Split a CSS font-family declaration into cleaned font names."""
    result: list[str] = []
    for part in raw.split(","):
        cleaned = part.strip().strip("\"'").strip()
        if cleaned:
            result.append(cleaned)
    return result


def _pick_east_asia_font(fonts: list[str], default: str = "Noto Sans JP") -> str:
    """Pick the most portable CJK font from a CSS font stack."""
    for f in fonts:
        low = f.lower()
        if "noto sans" in low and any(k in low for k in ("jp", "sc", "tc", "kr", "thai", "cjk")):
            return f
    for f in fonts:
        low = f.lower()
        if any(k in low for k in _CJK_FONT_KEYWORDS) and "hiragino" not in low:
            return f
    for f in fonts:
        if any(k in f.lower() for k in _CJK_FONT_KEYWORDS):
            return f
    return default


def _pick_latin_font(fonts: list[str], default: str = "Segoe UI") -> str:
    """Pick primary non-generic Latin sans-serif font from a CSS font stack."""
    for f in fonts:
        low = f.lower()
        if low in _GENERIC_FONT_NAMES:
            continue
        if any(k in low for k in _CJK_FONT_KEYWORDS):
            continue
        return f
    return default


def parse_docx_theme(css_path: str | None) -> DocxTheme:
    """Extract DocxTheme colors and fonts from a project's style.css file."""
    default = DocxTheme()
    if not css_path or not os.path.isfile(css_path):
        return default

    try:
        with open(css_path, "r", encoding="utf-8") as f:
            css_text = f.read()
    except OSError:
        return default

    vars_map: dict[str, str] = {}
    for match in re.finditer(r"--([a-zA-Z0-9_-]+)\s*:\s*([^;\}]+)", css_text):
        vars_map[match.group(1).strip()] = match.group(2).strip()

    body_fonts = _split_css_font_list(vars_map.get("rtd-body-font", vars_map.get("rtd-font", "")))
    head_fonts = _split_css_font_list(vars_map.get("rtd-font", ""))
    east_asia = _pick_east_asia_font(body_fonts or head_fonts, default.east_asia_font)
    latin_font = _pick_latin_font(body_fonts, default.latin_font)
    heading_font = _pick_latin_font(head_fonts, latin_font)

    bg_rgb = _parse_hex_rgb(vars_map.get("rtd-bg-color", "#ffffff"))
    is_dark_theme = bg_rgb is not None and _luminance(bg_rgb) < 0.5
    if is_dark_theme:
        # Word A4 pages use white paper; preserve font choices while keeping crisp light-page contrast.
        brand = _parse_hex_rgb(vars_map.get("rtd-brand-color", "")) or default.brand_color
        return DocxTheme(
            brand_color=brand,
            note_border_hex=_rgb_to_hex6(brand),
            latin_font=latin_font,
            heading_font=heading_font,
            east_asia_font=east_asia,
        )

    def _color(key: str, fallback: tuple[int, int, int]) -> tuple[int, int, int]:
        parsed = _parse_hex_rgb(vars_map.get(key, ""))
        return parsed if parsed is not None else fallback

    def _hex6(key: str, fallback: str) -> str:
        parsed = _parse_hex_rgb(vars_map.get(key, ""))
        return _rgb_to_hex6(parsed) if parsed is not None else fallback

    return DocxTheme(
        brand_color=_color("rtd-brand-color", default.brand_color),
        heading_color=_color("rtd-heading-color", default.heading_color),
        text_color=_color("rtd-text-color", default.text_color),
        muted_color=_color("rtd-muted-color", default.muted_color),
        border_hex=_hex6("rtd-border-color", default.border_hex),
        surface_bg_hex=_hex6("rtd-surface-bg", default.surface_bg_hex),
        code_bg_hex=_hex6("rtd-code-bg", default.code_bg_hex),
        inline_code_bg_hex=_hex6("rtd-inline-code-bg", default.inline_code_bg_hex),
        inline_code_color=_color("rtd-inline-code-color", default.inline_code_color),
        note_bg_hex=_hex6("rtd-note-bg", default.note_bg_hex),
        note_border_hex=_hex6("rtd-note-border", default.note_border_hex),
        code_keyword=_color("rtd-code-keyword", default.code_keyword),
        code_string=_color("rtd-code-string", default.code_string),
        code_comment=_color("rtd-code-comment", default.code_comment),
        code_number=_color("rtd-code-number", default.code_number),
        code_function=_color("rtd-code-function", default.code_function),
        code_type=_color("rtd-code-type", default.code_type),
        code_operator=_color("rtd-code-operator", default.code_operator),
        code_builtin=_color("rtd-code-builtin", default.code_builtin),
        latin_font=latin_font,
        heading_font=heading_font,
        east_asia_font=east_asia,
    )


def set_rpr_fonts(rpr: Any, latin_font: str, east_asia_font: str) -> None:  # noqa: ANN401
    """Configure w:rFonts on a CT_RPr element with explicit East Asian typeface."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    rfonts.set(qn("w:ascii"), latin_font)
    rfonts.set(qn("w:hAnsi"), latin_font)
    rfonts.set(qn("w:cs"), latin_font)
    rfonts.set(qn("w:eastAsia"), east_asia_font)


def set_style_fonts(style_obj: Any, latin_font: str, east_asia_font: str) -> None:  # noqa: ANN401
    """Set both Latin and East Asian (w:eastAsia) fonts on a python-docx Style."""
    style_obj.font.name = latin_font
    rpr = style_obj.element.get_or_add_rPr()
    set_rpr_fonts(rpr, latin_font, east_asia_font)


def set_run_fonts(run: Run, latin_font: str, east_asia_font: str) -> None:
    """Set both Latin and East Asian (w:eastAsia) fonts on a python-docx Run."""
    run.font.name = latin_font
    rpr = run._r.get_or_add_rPr()
    set_rpr_fonts(rpr, latin_font, east_asia_font)


def set_run_shading(run: Run, fill_hex: str) -> None:
    """Apply background shading (w:shd) to an inline code run."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    rpr = run._r.get_or_add_rPr()
    existing = rpr.find(qn("w:shd"))
    if existing is not None:
        rpr.remove(existing)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    rpr.append(shd)


def configure_docx_document(doc: DocxDocument, theme: DocxTheme) -> None:
    """Configure A4 page margins and built-in paragraph styles on a Document."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Mm, Pt, RGBColor

    for section in doc.sections:
        section.page_width = Mm(210)
        section.page_height = Mm(297)
        section.top_margin = Mm(18)
        section.bottom_margin = Mm(18)
        section.left_margin = Mm(16)
        section.right_margin = Mm(16)

    styles = doc.styles

    normal = styles["Normal"]
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = RGBColor(*theme.text_color)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.35
    set_style_fonts(normal, theme.latin_font, theme.east_asia_font)

    heading_specs: list[tuple[int, float, float, float, tuple[int, int, int], bool]] = [
        (1, 20.0, 14.0, 8.0, theme.heading_color, False),
        (2, 15.0, 14.0, 6.0, theme.heading_color, True),
        (3, 12.5, 10.0, 4.0, theme.heading_color, False),
        (4, 11.0, 8.0, 3.0, theme.heading_color, False),
        (5, 10.5, 6.0, 2.0, theme.heading_color, False),
        (6, 10.0, 6.0, 2.0, theme.muted_color, False),
    ]
    for level, size_pt, before_pt, after_pt, rgb, bottom_rule in heading_specs:
        h_style = styles[f"Heading {level}"]
        h_style.font.size = Pt(size_pt)
        h_style.font.bold = True
        h_style.font.italic = False
        h_style.font.color.rgb = RGBColor(*rgb)
        h_style.paragraph_format.space_before = Pt(before_pt)
        h_style.paragraph_format.space_after = Pt(after_pt)
        h_style.paragraph_format.line_spacing = 1.25
        h_style.paragraph_format.keep_with_next = True
        set_style_fonts(h_style, theme.heading_font, theme.east_asia_font)
        if bottom_rule:
            ppr = h_style.element.get_or_add_pPr()
            pbdr = ppr.find(qn("w:pBdr"))
            if pbdr is None:
                pbdr = OxmlElement("w:pBdr")
                ppr.append(pbdr)
            btm = OxmlElement("w:bottom")
            btm.set(qn("w:val"), "single")
            btm.set(qn("w:sz"), "6")
            btm.set(qn("w:space"), "4")
            btm.set(qn("w:color"), theme.border_hex)
            pbdr.append(btm)

    if "Caption" in styles:
        cap = styles["Caption"]
        cap.font.size = Pt(9.5)
        cap.font.bold = False
        cap.font.italic = False
        cap.font.color.rgb = RGBColor(*theme.muted_color)
        cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.space_before = Pt(2)
        cap.paragraph_format.space_after = Pt(10)
        set_style_fonts(cap, theme.latin_font, theme.east_asia_font)

    for list_style_name in (
        "List Bullet",
        "List Bullet 2",
        "List Bullet 3",
        "List Number",
        "List Number 2",
        "List Number 3",
    ):
        if list_style_name in styles:
            ls = styles[list_style_name]
            ls.font.size = Pt(10.5)
            ls.font.color.rgb = RGBColor(*theme.text_color)
            ls.paragraph_format.space_before = Pt(0)
            ls.paragraph_format.space_after = Pt(3)
            ls.paragraph_format.line_spacing = 1.3
            set_style_fonts(ls, theme.latin_font, theme.east_asia_font)


def add_bookmark(paragraph: Paragraph, bookmark_name: str, bookmark_id: int) -> None:
    """Attach an OpenXML bookmark anchor to the start of a paragraph."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    bm_start = OxmlElement("w:bookmarkStart")
    bm_start.set(qn("w:id"), str(bookmark_id))
    bm_start.set(qn("w:name"), bookmark_name)

    bm_end = OxmlElement("w:bookmarkEnd")
    bm_end.set(qn("w:id"), str(bookmark_id))

    paragraph._p.insert(0, bm_start)
    paragraph._p.append(bm_end)


def add_hyperlink_run(
    paragraph: Paragraph,
    text: str,
    *,
    theme: DocxTheme,
    url: str | None = None,
    anchor: str | None = None,
    bold: bool = False,
    italic: bool = False,
    strikethrough: bool = False,
    is_code: bool = False,
) -> None:
    """Append a clickable external or internal bookmark hyperlink run to a paragraph."""
    from docx.opc.constants import RELATIONSHIP_TYPE
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    hyperlink = OxmlElement("w:hyperlink")
    if url:
        rel_id = paragraph.part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
        hyperlink.set(qn("r:id"), rel_id)
    elif anchor:
        hyperlink.set(qn("w:anchor"), anchor)
    else:
        return

    new_run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    set_rpr_fonts(rpr, theme.mono_font if is_code else theme.latin_font, theme.east_asia_font)

    color_el = OxmlElement("w:color")
    color_el.set(qn("w:val"), _rgb_to_hex6(theme.brand_color))
    rpr.append(color_el)

    u_el = OxmlElement("w:u")
    u_el.set(qn("w:val"), "single")
    rpr.append(u_el)

    if bold:
        rpr.append(OxmlElement("w:b"))
    if italic:
        rpr.append(OxmlElement("w:i"))
    if strikethrough:
        rpr.append(OxmlElement("w:strike"))
    if is_code:
        sz_el = OxmlElement("w:sz")
        sz_el.set(qn("w:val"), "19")  # 9.5pt in half-points
        rpr.append(sz_el)
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), theme.inline_code_bg_hex)
        rpr.append(shd)

    new_run.append(rpr)
    t_el = OxmlElement("w:t")
    if text.startswith(" ") or text.endswith(" "):
        t_el.set(qn("xml:space"), "preserve")
    t_el.text = text
    new_run.append(t_el)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def style_blockquote_paragraph(paragraph: Paragraph, theme: DocxTheme, *, depth: int = 1) -> None:
    """Format a paragraph as a callout / blockquote with a left accent border and shading."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Mm, Pt

    paragraph.paragraph_format.left_indent = Mm(6 * max(1, depth))
    paragraph.paragraph_format.right_indent = Mm(4)
    paragraph.paragraph_format.space_before = Pt(3)
    paragraph.paragraph_format.space_after = Pt(4)

    ppr = paragraph._p.get_or_add_pPr()
    pbdr = ppr.find(qn("w:pBdr"))
    if pbdr is None:
        pbdr = OxmlElement("w:pBdr")
        ppr.append(pbdr)
    left_bdr = OxmlElement("w:left")
    left_bdr.set(qn("w:val"), "single")
    left_bdr.set(qn("w:sz"), "24")
    left_bdr.set(qn("w:space"), "8")
    left_bdr.set(qn("w:color"), theme.note_border_hex)
    pbdr.append(left_bdr)

    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), theme.note_bg_hex)
    ppr.append(shd)


def style_hr_paragraph(paragraph: Paragraph, border_hex: str) -> None:
    """Format a paragraph as a horizontal divider rule."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt

    paragraph.paragraph_format.space_before = Pt(6)
    paragraph.paragraph_format.space_after = Pt(8)
    ppr = paragraph._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    btm = OxmlElement("w:bottom")
    btm.set(qn("w:val"), "single")
    btm.set(qn("w:sz"), "6")
    btm.set(qn("w:space"), "1")
    btm.set(qn("w:color"), border_hex)
    pbdr.append(btm)
    ppr.append(pbdr)


def allocate_ordered_list_num_id(doc: DocxDocument, start: int = 1) -> int:
    """Create a fresh numbering instance in numbering_part so each ordered list restarts cleanly."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    numbering = doc.part.numbering_part.numbering_definitions._numbering
    existing_ids: list[int] = []
    abs_num_id = "7"
    for el in numbering.findall(qn("w:num")):
        raw_id = el.get(qn("w:numId"))
        if raw_id and raw_id.isdigit():
            existing_ids.append(int(raw_id))
        if raw_id == "5":
            abs_el = el.find(qn("w:abstractNumId"))
            if abs_el is not None and abs_el.get(qn("w:val")):
                abs_num_id = str(abs_el.get(qn("w:val")))

    new_id = max(existing_ids, default=9) + 1
    num_el = OxmlElement("w:num")
    num_el.set(qn("w:numId"), str(new_id))
    abs_ref = OxmlElement("w:abstractNumId")
    abs_ref.set(qn("w:val"), abs_num_id)
    num_el.append(abs_ref)

    for lvl in range(9):
        lvl_override = OxmlElement("w:lvlOverride")
        lvl_override.set(qn("w:ilvl"), str(lvl))
        start_override = OxmlElement("w:startOverride")
        start_override.set(qn("w:val"), str(start if lvl == 0 else 1))
        lvl_override.append(start_override)
        num_el.append(lvl_override)

    numbering.append(num_el)
    return new_id


def apply_ordered_numbering(paragraph: Paragraph, num_id: int, level: int) -> None:
    """Bind a paragraph to a specific numbering definition and nesting level."""
    ppr = paragraph._p.get_or_add_pPr()
    num_pr = ppr.get_or_add_numPr()
    ilvl = num_pr.get_or_add_ilvl()
    ilvl.val = max(0, min(level, 8))
    nid = num_pr.get_or_add_numId()
    nid.val = num_id


def set_table_full_width(table: Table, width_mm: float = 178.0) -> None:
    """Set preferred width on a Word table in dxa (1/20 pt)."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    dxa = int(round(width_mm * 72.0 / 25.4 * 20.0))
    tbl_pr = table._tbl.tblPr
    existing = tbl_pr.find(qn("w:tblW"))
    if existing is not None:
        tbl_pr.remove(existing)
    tbl_w = OxmlElement("w:tblW")
    tbl_w.set(qn("w:w"), str(dxa))
    tbl_w.set(qn("w:type"), "dxa")
    tbl_pr.append(tbl_w)


def style_table_cell(
    cell: _Cell,
    *,
    fill_hex: str | None = None,
    border_hex: str | None = None,
    all_borders: bool = False,
    is_header: bool = False,
    pad_v_dxa: int = 110,
    pad_h_dxa: int = 140,
) -> None:
    """Apply background shading, borders, and margins to a Word table cell."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    tc_pr = cell._tc.get_or_add_tcPr()

    if fill_hex:
        existing_shd = tc_pr.find(qn("w:shd"))
        if existing_shd is not None:
            tc_pr.remove(existing_shd)
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), fill_hex)
        tc_pr.append(shd)

    if border_hex:
        existing_bdr = tc_pr.find(qn("w:tcBorders"))
        if existing_bdr is not None:
            tc_pr.remove(existing_bdr)
        tc_borders = OxmlElement("w:tcBorders")
        sides = ("top", "bottom", "left", "right") if all_borders else ("top", "bottom")
        for side in ("top", "bottom", "left", "right"):
            b_el = OxmlElement(f"w:{side}")
            if side in sides:
                b_el.set(qn("w:val"), "single")
                b_el.set(qn("w:sz"), "8" if (is_header and side == "bottom") else "4")
                b_el.set(qn("w:space"), "0")
                b_el.set(qn("w:color"), border_hex)
            else:
                b_el.set(qn("w:val"), "none")
            tc_borders.append(b_el)
        tc_pr.append(tc_borders)

    existing_mar = tc_pr.find(qn("w:tcMar"))
    if existing_mar is not None:
        tc_pr.remove(existing_mar)
    tc_mar = OxmlElement("w:tcMar")
    for side, val in (
        ("top", pad_v_dxa),
        ("bottom", pad_v_dxa),
        ("left", pad_h_dxa),
        ("right", pad_h_dxa),
    ):
        m_el = OxmlElement(f"w:{side}")
        m_el.set(qn("w:w"), str(val))
        m_el.set(qn("w:type"), "dxa")
        tc_mar.append(m_el)
    tc_pr.append(tc_mar)


def set_table_row_flags(row: _Row, *, is_header: bool = False, cant_split: bool = True) -> None:
    """Configure w:tblHeader and w:cantSplit flags on a Word table row."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    tr_pr = row._tr.get_or_add_trPr()
    if is_header and tr_pr.find(qn("w:tblHeader")) is None:
        tr_pr.append(OxmlElement("w:tblHeader"))
    if cant_split and tr_pr.find(qn("w:cantSplit")) is None:
        tr_pr.append(OxmlElement("w:cantSplit"))


def add_post_table_spacer(doc: DocxDocument) -> None:
    """Append a compact spacer paragraph after a table so adjacent Word tables do not merge."""
    from docx.shared import Pt

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(4)
    spacer.paragraph_format.line_spacing = 1.0
    run = spacer.add_run()
    run.font.size = Pt(2)


def resolve_pygments_style(
    token_type: Any,  # noqa: ANN401
    theme: DocxTheme,
) -> tuple[tuple[int, int, int], bool, bool]:
    """Map a Pygments Token type to (rgb_color, is_bold, is_italic)."""
    from pygments.token import Comment, Error, Keyword, Name, Number, Operator, String

    result: tuple[tuple[int, int, int], bool, bool] = (theme.text_color, False, False)
    if token_type in Keyword:
        result = (theme.code_keyword, True, False)
    elif token_type in String:
        result = (theme.code_string, False, False)
    elif token_type in Comment:
        result = (theme.code_comment, False, True)
    elif token_type in Number:
        result = (theme.code_number, False, False)
    elif token_type in Name.Function:
        result = (theme.code_function, False, False)
    elif (
        token_type in Name.Class
        or token_type in Name.Namespace
        or token_type in Name.Decorator
        or token_type in Name.Exception
        or token_type in Name.Tag
        or token_type in Name.Attribute
    ):
        result = (theme.code_type, True, False)
    elif token_type in Name.Builtin:
        result = (theme.code_builtin, False, False)
    elif token_type in Operator:
        result = (theme.code_operator, False, False)
    elif token_type in Error:
        result = ((239, 68, 68), False, False)
    return result
