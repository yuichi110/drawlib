# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Playwright 1920x1080 DOM geometry and computed style extractor for PPTX export."""

from __future__ import annotations

import contextlib
import os
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final, Literal

from drawlib._builder._common.browser import (
    import_sync_playwright,
    launch_headless_chromium,
)

if TYPE_CHECKING:
    from playwright.sync_api import Page

LayerKey = tuple[int, int, int, int]
AlignType = Literal["left", "center", "right", "justify"]
ValignType = Literal["top", "middle", "bottom"]


@dataclass(frozen=True)
class PptxColor:
    """Resolved sRGB color with opacity."""

    rgb: tuple[int, int, int]
    alpha: float = 1.0


@dataclass(frozen=True)
class PptxRun:
    """Inline styled text run inside a slide paragraph or table cell."""

    text: str
    font_family: str
    ea_font_family: str
    font_size_px: float
    color: PptxColor
    bold: bool = False
    italic: bool = False
    underline: bool = False
    strike: bool = False
    code_bg: PptxColor | None = None
    href: str | None = None
    is_line_break: bool = False


@dataclass(frozen=True)
class PptxParagraph:
    """Single paragraph inside a text box or table cell."""

    runs: list[PptxRun]
    align: AlignType = "left"
    line_height_ratio: float = 1.35
    space_before_px: float = 0.0
    space_after_px: float = 0.0
    bullet_prefix: str | None = None
    hanging_indent_px: float = 0.0


@dataclass(frozen=True)
class PptxCard:
    """Positioned background/border container rectangle or rounded card."""

    layer: LayerKey
    x: float
    y: float
    width: float
    height: float
    bg: PptxColor | None
    border_color: PptxColor | None
    border_width_px: float
    radius_px: float
    left_accent_color: PptxColor | None = None
    left_accent_width_px: float = 0.0


@dataclass(frozen=True)
class PptxRule:
    """Horizontal divider rule (<hr>)."""

    layer: LayerKey
    x: float
    y: float
    width: float
    height: float
    color: PptxColor
    radius_px: float = 0.0


@dataclass(frozen=True)
class PptxImage:
    """Positioned raster image element with object-fit: contain geometry."""

    layer: LayerKey
    x: float
    y: float
    width: float
    height: float
    image_path: str


@dataclass(frozen=True)
class PptxTableCell:
    """Measured table cell style and inline paragraph content."""

    paragraphs: list[PptxParagraph]
    bg: PptxColor | None
    border_top: tuple[float, PptxColor] | None
    border_bottom: tuple[float, PptxColor] | None
    border_left: tuple[float, PptxColor] | None
    border_right: tuple[float, PptxColor] | None
    pad_top_px: float
    pad_right_px: float
    pad_bottom_px: float
    pad_left_px: float
    valign: ValignType = "middle"


@dataclass(frozen=True)
class PptxTable:
    """Measured HTML table geometry and cells."""

    layer: LayerKey
    x: float
    y: float
    width: float
    height: float
    col_widths_px: list[float]
    row_heights_px: list[float]
    rows: list[list[PptxTableCell]]


@dataclass(frozen=True)
class PptxTextBox:
    """Positioned native PowerPoint text box."""

    layer: LayerKey
    x: float
    y: float
    width: float
    height: float
    paragraphs: list[PptxParagraph]
    is_code: bool = False


SlideElement = PptxCard | PptxRule | PptxImage | PptxTable | PptxTextBox


@dataclass(frozen=True)
class PptxSlideSpec:
    """Complete measured specification for a single 1920x1080 slide."""

    index: int
    bg: PptxColor
    elements: list[SlideElement]
    notes_text: str


@dataclass(frozen=True)
class PptxDeckSpec:
    """Complete measured specification for an entire slide deck."""

    title: str
    default_ea_font: str
    slides: list[PptxSlideSpec]


_STAGE_OVERRIDE_CSS: Final[str] = """
html, body, .presentation-viewport {
  width: 1920px !important;
  height: 1080px !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow: visible !important;
}
.presentation-stage {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: 1920px !important;
  height: 1080px !important;
  transform: none !important;
  box-shadow: none !important;
}
.slide {
  top: 0 !important;
  left: 0 !important;
  width: 1920px !important;
  height: 1080px !important;
  transform: none !important;
}
.slide-controls, .overview-modal, .anim-play-badge {
  display: none !important;
}
.slide-block[style*="color"] p,
.slide-block[style*="color"] ul,
.slide-block[style*="color"] ol {
  color: inherit;
}
"""

_JS_EXTRACT_SLIDE: Final[str] = r"""
(slideIndex) => {
  const slides = Array.from(document.querySelectorAll('section.slide'));
  slides.forEach((s, idx) => {
    if (idx === slideIndex) s.classList.add('active');
    else s.classList.remove('active');
  });
  const slide = slides[slideIndex];
  if (!slide) return null;

  const slideRect = slide.getBoundingClientRect();
  const sx = slideRect.left;
  const sy = slideRect.top;

  const colorCanvas = document.createElement('canvas');
  colorCanvas.width = 1;
  colorCanvas.height = 1;
  const colorCtx = colorCanvas.getContext('2d', { willReadFrequently: true });

  function parseColor(cssVal) {
    if (!cssVal || cssVal === 'transparent' || cssVal === 'none') return null;
    const m = cssVal.match(/^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,/\s]+([\d.]+))?\s*\)$/i);
    if (m) {
      const a = m[4] !== undefined ? parseFloat(m[4]) : 1.0;
      if (a <= 0.01) return null;
      return { r: Math.round(parseFloat(m[1])), g: Math.round(parseFloat(m[2])), b: Math.round(parseFloat(m[3])), a };
    }
    if (!colorCtx) return null;
    colorCtx.clearRect(0, 0, 1, 1);
    colorCtx.fillStyle = 'rgba(0,0,0,0)';
    colorCtx.fillStyle = cssVal;
    colorCtx.fillRect(0, 0, 1, 1);
    const d = colorCtx.getImageData(0, 0, 1, 1).data;
    const a = +(d[3] / 255).toFixed(4);
    if (a <= 0.01) return null;
    return { r: d[0], g: d[1], b: d[2], a };
  }

  const GENERIC_FONTS = new Set([
    'sans-serif', 'serif', 'monospace', 'system-ui', 'ui-sans-serif',
    'ui-serif', 'ui-monospace', '-apple-system', 'blinkmacsystemfont', 'phosphor'
  ]);
  const CJK_RE = new RegExp(
    'noto\\s+(sans|serif).*jp|noto\\s+sans\\s+cjk|hiragino|yu\\s*gothic|yugothic|' +
    'meiryo|ms\\s+pgothic|source\\s+han|pingfang|microsoft\\s+yahei|malgun',
    'i'
  );

  function parseFonts(fontFamilyStr, fallbackEa) {
    const parts = (fontFamilyStr || '').split(',').map(s => s.trim().replace(/^['"]|['"]$/g, '')).filter(Boolean);
    let latin = '';
    let ea = '';
    for (const p of parts) {
      const low = p.toLowerCase();
      if (GENERIC_FONTS.has(low)) continue;
      if (CJK_RE.test(p)) {
        if (!ea) ea = p;
      } else if (!latin) {
        latin = p;
      }
    }
    const isMono = /monospace|mono|consolas|menlo|fira\s+code/i.test(fontFamilyStr || '');
    if (!latin) latin = isMono ? 'Consolas' : 'Calibri';
    if (!ea) ea = fallbackEa || 'Noto Sans JP';
    return { latin, ea };
  }

  const bodyFonts = parseFonts(getComputedStyle(document.body).fontFamily, 'Noto Sans JP');
  const defaultEa = bodyFonts.ea;
  const slideBg = parseColor(getComputedStyle(slide).backgroundColor) || { r: 255, g: 255, b: 255, a: 1.0 };

  function px(val) {
    const n = parseFloat(val);
    return Number.isFinite(n) ? n : 0;
  }

  function normAlign(val) {
    if (val === 'center') return 'center';
    if (val === 'right' || val === 'end') return 'right';
    if (val === 'justify') return 'justify';
    return 'left';
  }

  function computeLineHeightRatio(cs, fontSizePx) {
    if (!cs.lineHeight || cs.lineHeight === 'normal') return 1.35;
    const lh = parseFloat(cs.lineHeight);
    if (!Number.isFinite(lh) || fontSizePx <= 0) return 1.35;
    return Math.max(0.95, Math.min(2.5, +(lh / fontSizePx).toFixed(3)));
  }

  function findHref(el) {
    let cur = el;
    while (cur && cur !== slide) {
      if (cur.tagName === 'A') {
        const raw = cur.getAttribute('href') || '';
        if (/^(https?:|mailto:)/i.test(raw)) return raw;
      }
      cur = cur.parentElement;
    }
    return null;
  }

  function findInlineCodeBg(el, stopRoot) {
    let cur = el;
    while (cur && cur !== stopRoot && cur !== slide) {
      if (cur.tagName === 'CODE' && (!cur.parentElement || cur.parentElement.tagName !== 'PRE')) {
        const bg = parseColor(getComputedStyle(cur).backgroundColor);
        if (bg && bg.a > 0.05) return bg;
      }
      cur = cur.parentElement;
    }
    return null;
  }

  function isHidden(el) {
    const cs = getComputedStyle(el);
    return cs.display === 'none' || cs.visibility === 'hidden' || px(cs.opacity) <= 0.01;
  }

  const BLOCK_TAGS = new Set([
    'DIV', 'P', 'UL', 'OL', 'LI', 'PRE', 'TABLE', 'BLOCKQUOTE',
    'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'HR', 'FIGURE', 'SECTION', 'ARTICLE', 'ASIDE'
  ]);

  function collectInlineRuns(nodes, stopRoot, preserveWhitespace) {
    const rawRuns = [];
    function walk(node) {
      if (node.nodeType === Node.TEXT_NODE) {
        const txt = node.nodeValue || '';
        if (!txt) return;
        const parentEl = node.parentElement || stopRoot;
        if (!parentEl || isHidden(parentEl)) return;
        const cs = getComputedStyle(parentEl);
        const fs = px(cs.fontSize) || 20;
        const fonts = parseFonts(cs.fontFamily, defaultEa);
        const fw = cs.fontWeight;
        const bold = fw === 'bold' || fw === 'bolder' || parseInt(fw, 10) >= 600;
        const italic = cs.fontStyle === 'italic' || cs.fontStyle === 'oblique';
        const deco = cs.textDecorationLine || cs.textDecoration || '';
        const href = findHref(parentEl);
        const underline = deco.includes('underline') || Boolean(href);
        const strike = deco.includes('line-through');
        const color = parseColor(cs.color) || { r: 32, g: 33, b: 36, a: 1.0 };
        const codeBg = preserveWhitespace ? null : findInlineCodeBg(parentEl, stopRoot);
        rawRuns.push({
          text: txt,
          latin: fonts.latin,
          ea: fonts.ea,
          fontSize: fs,
          color,
          bold,
          italic,
          underline,
          strike,
          codeBg,
          href,
          br: false
        });
        return;
      }
      if (node.nodeType !== Node.ELEMENT_NODE) return;
      const el = node;
      const tag = el.tagName;
      if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'SVG') return;
      if (isHidden(el)) return;
      if (tag === 'BR') {
        rawRuns.push({
          br: true, text: '', latin: bodyFonts.latin, ea: defaultEa,
          fontSize: 16, color: { r: 0, g: 0, b: 0, a: 1 }
        });
        return;
      }
      if (!preserveWhitespace && BLOCK_TAGS.has(tag)) return;
      for (const child of el.childNodes) walk(child);
    }
    for (const n of nodes) walk(n);

    if (preserveWhitespace) return rawRuns;

    // Collapse HTML flow whitespace while preserving inter-span single spaces
    const cleaned = [];
    let atLineStart = true;
    for (const r of rawRuns) {
      if (r.br) {
        if (cleaned.length > 0 && !cleaned[cleaned.length - 1].br) {
          cleaned[cleaned.length - 1].text = cleaned[cleaned.length - 1].text.replace(/ +$/g, '');
        }
        cleaned.push(r);
        atLineStart = true;
        continue;
      }
      let t = r.text.replace(/[\t\r\n ]+/g, ' ');
      if (atLineStart) t = t.replace(/^ +/g, '');
      if (!t) continue;
      atLineStart = t.endsWith(' ');
      // Merge identical consecutive run styles
      const prev = cleaned.length > 0 ? cleaned[cleaned.length - 1] : null;
      if (prev && !prev.br && atLineStart && t === ' ' && cleaned.length === 0) continue;
      if (
        prev && !prev.br &&
        prev.latin === r.latin && prev.ea === r.ea && prev.fontSize === r.fontSize &&
        prev.bold === r.bold && prev.italic === r.italic &&
        prev.underline === r.underline && prev.strike === r.strike &&
        prev.href === r.href &&
        prev.color.r === r.color.r && prev.color.g === r.color.g && prev.color.b === r.color.b &&
        JSON.stringify(prev.codeBg) === JSON.stringify(r.codeBg)
      ) {
        prev.text = (prev.text + t).replace(/ {2,}/g, ' ');
      } else {
        if (prev && !prev.br && prev.text.endsWith(' ') && t.startsWith(' ')) {
          t = t.slice(1);
        }
        if (t) cleaned.push({ ...r, text: t });
      }
      const last = cleaned[cleaned.length - 1];
      atLineStart = !last || last.br;
    }
    while (cleaned.length > 0 && !cleaned[cleaned.length - 1].br) {
      cleaned[cleaned.length - 1].text = cleaned[cleaned.length - 1].text.replace(/ +$/g, '');
      if (!cleaned[cleaned.length - 1].text) cleaned.pop();
      else break;
    }
    return cleaned;
  }

  let itemCounter = 0;
  let svgCaptureCounter = 0;
  const cards = [];
  const rules = [];
  const images = [];
  const tables = [];
  const textBoxes = [];

  function extractCardIfStyled(el, blockZ, blockIdx, subLayer) {
    if (isHidden(el)) return;
    const rect = el.getBoundingClientRect();
    if (rect.width <= 1 || rect.height <= 1) return;
    const cs = getComputedStyle(el);
    const bg = parseColor(cs.backgroundColor);

    const btW = cs.borderTopStyle !== 'none' ? px(cs.borderTopWidth) : 0;
    const brW = cs.borderRightStyle !== 'none' ? px(cs.borderRightWidth) : 0;
    const bbW = cs.borderBottomStyle !== 'none' ? px(cs.borderBottomWidth) : 0;
    const blW = cs.borderLeftStyle !== 'none' ? px(cs.borderLeftWidth) : 0;

    const btC = btW > 0 ? parseColor(cs.borderTopColor) : null;
    const blC = blW > 0 ? parseColor(cs.borderLeftColor) : null;
    const bbC = bbW > 0 ? parseColor(cs.borderBottomColor) : null;

    let borderW = 0;
    let borderColor = null;
    let leftAccentW = 0;
    let leftAccentColor = null;

    if (blW >= 3 && blC && blW > btW + 1.5) {
      leftAccentW = blW;
      leftAccentColor = blC;
      if (btW > 0 && btC) {
        borderW = btW;
        borderColor = btC;
      }
    } else {
      const candidates = [
        [btW, btC], [bbW, bbC], [blW, blC],
        [brW, brW > 0 ? parseColor(cs.borderRightColor) : null]
      ].filter(c => c[0] > 0 && c[1]);
      if (candidates.length > 0) {
        borderW = candidates[0][0];
        borderColor = candidates[0][1];
      }
    }

    if (!bg && !borderColor && !leftAccentColor) return;
    const radius = Math.max(
      px(cs.borderTopLeftRadius),
      px(cs.borderTopRightRadius),
      px(cs.borderBottomLeftRadius),
      px(cs.borderBottomRightRadius)
    );
    cards.push({
      layer: [blockZ, blockIdx, subLayer, ++itemCounter],
      x: rect.left - sx,
      y: rect.top - sy,
      width: rect.width,
      height: rect.height,
      bg,
      borderColor,
      borderWidthPx: borderW,
      radiusPx: radius,
      leftAccentColor,
      leftAccentWidthPx: leftAccentW,
    });
  }

  function contentBoxOf(el) {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    const pl = px(cs.paddingLeft) + px(cs.borderLeftWidth);
    const pr = px(cs.paddingRight) + px(cs.borderRightWidth);
    const pt = px(cs.paddingTop) + px(cs.borderTopWidth);
    const pb = px(cs.paddingBottom) + px(cs.borderBottomWidth);
    return {
      x: r.left - sx + pl,
      y: r.top - sy + pt,
      width: Math.max(4, r.width - pl - pr),
      height: Math.max(4, r.height - pt - pb),
      cs
    };
  }

  function listMarkerFor(li) {
    const parent = li.parentElement;
    if (!parent || (parent.tagName !== 'UL' && parent.tagName !== 'OL')) return null;
    const pcs = getComputedStyle(li);
    if (pcs.listStyleType === 'none') return null;

    let depth = 0;
    let cur = parent.parentElement;
    while (cur && cur !== slide) {
      if (cur.tagName === 'UL' || cur.tagName === 'OL') depth++;
      cur = cur.parentElement;
    }

    if (parent.tagName === 'UL') {
      const bullets = ['•', '◦', '▪'];
      return bullets[Math.min(depth, bullets.length - 1)];
    }
    let idx = parseInt(parent.getAttribute('start') || '1', 10);
    if (!Number.isFinite(idx)) idx = 1;
    for (const sib of parent.children) {
      if (sib === li) break;
      if (sib.tagName === 'LI') idx++;
    }
    const valAttr = li.getAttribute('value');
    if (valAttr && Number.isFinite(parseInt(valAttr, 10))) idx = parseInt(valAttr, 10);
    return `${idx}.`;
  }

  function listGutterPx(li, textLeftX) {
    const parent = li.parentElement;
    if (!parent) return 28;
    const pRect = parent.getBoundingClientRect();
    const parentLeft = pRect.left - sx;
    const diff = textLeftX - parentLeft;
    if (diff >= 14 && diff <= 56) return Math.min(34, Math.max(20, diff - 6));
    return 28;
  }

  function emitFlowParagraphBox(box, runs, cs, blockZ, blockIdx, marker, gutterPx) {
    if (!runs || runs.length === 0) return;
    const fs = px(cs.fontSize) || 20;
    let bx = box.x;
    let bw = box.width;
    let hanging = 0;
    if (marker) {
      const g = gutterPx || 28;
      bx = Math.max(0, bx - g);
      bw = bw + g;
      hanging = g;
    }
    textBoxes.push({
      layer: [blockZ, blockIdx, 3, ++itemCounter],
      x: bx,
      y: box.y,
      width: bw,
      height: box.height,
      isCode: false,
      paragraphs: [{
        runs,
        align: normAlign(cs.textAlign),
        lineHeightRatio: computeLineHeightRatio(cs, fs),
        spaceBeforePx: 0,
        spaceAfterPx: 0,
        bulletPrefix: marker || null,
        hangingIndentPx: hanging,
      }]
    });
  }

  function emitPreCodeBlock(preEl, blockZ, blockIdx) {
    extractCardIfStyled(preEl, blockZ, blockIdx, 1);
    const codeEl = Array.from(preEl.children).find(c => c.tagName === 'CODE') || null;
    if (codeEl && getComputedStyle(codeEl).display === 'block') {
      extractCardIfStyled(codeEl, blockZ, blockIdx, 1);
    }
    const targetEl = codeEl || preEl;
    const cbox = contentBoxOf(targetEl);
    const runs = collectInlineRuns(Array.from(targetEl.childNodes), targetEl, true);
    if (runs.length === 0) return;

    const fs = px(cbox.cs.fontSize) || 20;
    const lh = computeLineHeightRatio(cbox.cs, fs);
    // Split runs on '\n' into individual code paragraphs
    const lines = [[]];
    for (const r of runs) {
      if (r.br) {
        lines.push([]);
        continue;
      }
      const parts = r.text.split('\n');
      for (let i = 0; i < parts.length; i++) {
        if (i > 0) lines.push([]);
        if (parts[i].length > 0) {
          lines[lines.length - 1].push({ ...r, text: parts[i] });
        }
      }
    }
    // Remove single trailing empty line added by markdown-it before </code>
    if (lines.length > 1 && lines[lines.length - 1].length === 0) {
      lines.pop();
    }
    const paragraphs = lines.map(lineRuns => ({
      runs: lineRuns.length > 0 ? lineRuns : [{
        text: ' ',
        latin: bodyFonts.latin,
        ea: defaultEa,
        fontSize: fs,
        color: { r: 32, g: 33, b: 36, a: 1 },
        bold: false, italic: false, underline: false, strike: false, codeBg: null, href: null, br: false
      }],
      align: 'left',
      lineHeightRatio: lh,
      spaceBeforePx: 0,
      spaceAfterPx: 0,
      bulletPrefix: null,
      hangingIndentPx: 0,
    }));
    textBoxes.push({
      layer: [blockZ, blockIdx, 3, ++itemCounter],
      x: cbox.x,
      y: cbox.y,
      width: cbox.width,
      height: cbox.height,
      isCode: true,
      paragraphs,
    });
  }

  function extractBorderSide(cs, side) {
    const style = cs[`border${side}Style`];
    const w = style && style !== 'none' ? px(cs[`border${side}Width`]) : 0;
    if (w <= 0) return null;
    const c = parseColor(cs[`border${side}Color`]);
    return c ? { widthPx: w, color: c } : null;
  }

  function emitTable(tableEl, blockZ, blockIdx) {
    if (isHidden(tableEl)) return;
    const tRect = tableEl.getBoundingClientRect();
    if (tRect.width <= 2 || tRect.height <= 2) return;

    const trList = Array.from(tableEl.querySelectorAll('tr')).filter(
      tr => tr.closest('table') === tableEl && !isHidden(tr)
    );
    if (trList.length === 0) return;

    const rowHeights = [];
    const parsedRows = [];
    let maxCols = 0;
    const colWidths = [];

    for (let rIdx = 0; rIdx < trList.length; rIdx++) {
      const tr = trList[rIdx];
      const trRect = tr.getBoundingClientRect();
      rowHeights.push(Math.max(8, trRect.height));
      const trBg = parseColor(getComputedStyle(tr).backgroundColor);

      const cells = Array.from(tr.children).filter(c => c.tagName === 'TH' || c.tagName === 'TD');
      if (cells.length > maxCols) maxCols = cells.length;

      const rowData = [];
      for (let cIdx = 0; cIdx < cells.length; cIdx++) {
        const cell = cells[cIdx];
        const cellRect = cell.getBoundingClientRect();
        if (colWidths[cIdx] === undefined) colWidths[cIdx] = Math.max(12, cellRect.width);

        const ccs = getComputedStyle(cell);
        const bg = parseColor(ccs.backgroundColor) || trBg;
        const fs = px(ccs.fontSize) || 18;
        const runs = collectInlineRuns(Array.from(cell.childNodes), cell, false);
        const va = ccs.verticalAlign;
        const valign = va === 'top' ? 'top' : (va === 'bottom' ? 'bottom' : 'middle');

        rowData.push({
          paragraphs: [{
            runs,
            align: normAlign(ccs.textAlign),
            lineHeightRatio: computeLineHeightRatio(ccs, fs),
            spaceBeforePx: 0,
            spaceAfterPx: 0,
            bulletPrefix: null,
            hangingIndentPx: 0,
          }],
          bg,
          borderTop: extractBorderSide(ccs, 'Top'),
          borderBottom: extractBorderSide(ccs, 'Bottom'),
          borderLeft: extractBorderSide(ccs, 'Left'),
          borderRight: extractBorderSide(ccs, 'Right'),
          padTopPx: px(ccs.paddingTop),
          padRightPx: px(ccs.paddingRight),
          padBottomPx: px(ccs.paddingBottom),
          padLeftPx: px(ccs.paddingLeft),
          valign,
        });
      }
      parsedRows.push(rowData);
    }
    if (maxCols === 0) return;
    while (colWidths.length < maxCols) colWidths.push(Math.max(20, tRect.width / maxCols));

    tables.push({
      layer: [blockZ, blockIdx, 3, ++itemCounter],
      x: tRect.left - sx,
      y: tRect.top - sy,
      width: tRect.width,
      height: tRect.height,
      colWidthsPx: colWidths.slice(0, maxCols),
      rowHeightsPx: rowHeights,
      rows: parsedRows,
    });
  }

  function emitImage(imgEl, blockZ, blockIdx) {
    if (isHidden(imgEl)) return;
    const r = imgEl.getBoundingClientRect();
    if (r.width <= 1 || r.height <= 1) return;
    const srcAttr = imgEl.getAttribute('src') || '';
    if (!srcAttr) return;

    const cs = getComputedStyle(imgEl);
    const fit = cs.objectFit || 'fill';
    const natW = imgEl.naturalWidth || r.width;
    const natH = imgEl.naturalHeight || r.height;

    let drawX = r.left - sx;
    let drawY = r.top - sy;
    let drawW = r.width;
    let drawH = r.height;

    if ((fit === 'contain' || fit === 'scale-down') && natW > 0 && natH > 0) {
      const scale = fit === 'scale-down'
        ? Math.min(1.0, r.width / natW, r.height / natH)
        : Math.min(r.width / natW, r.height / natH);
      drawW = natW * scale;
      drawH = natH * scale;
      drawX = (r.left - sx) + (r.width - drawW) / 2;
      drawY = (r.top - sy) + (r.height - drawH) / 2;
    }

    let captureId = null;
    if (/\.svg(\?|#|$)/i.test(srcAttr)) {
      captureId = `svg_img_${slideIndex}_${++svgCaptureCounter}`;
      imgEl.setAttribute('data-pptx-svg-capture', captureId);
    }

    images.push({
      layer: [blockZ, blockIdx, 2, ++itemCounter],
      x: drawX,
      y: drawY,
      width: drawW,
      height: drawH,
      src: srcAttr,
      captureId,
    });
  }

  function emitInlineSvg(svgEl, blockZ, blockIdx) {
    if (isHidden(svgEl)) return;
    if (svgEl.closest('.anim-play-badge')) return;
    const r = svgEl.getBoundingClientRect();
    if (r.width <= 2 || r.height <= 2) return;
    const captureId = `svg_inline_${slideIndex}_${++svgCaptureCounter}`;
    svgEl.setAttribute('data-pptx-svg-capture', captureId);
    images.push({
      layer: [blockZ, blockIdx, 2, ++itemCounter],
      x: r.left - sx,
      y: r.top - sy,
      width: r.width,
      height: r.height,
      src: '',
      captureId,
    });
  }

  function flushInlineSlice(nodes, containerEl, blockZ, blockIdx, markerOverride) {
    if (!nodes || nodes.length === 0) return false;
    const imgs = [];
    for (const n of nodes) {
      if (n.nodeType === Node.ELEMENT_NODE) {
        if (n.tagName === 'IMG') imgs.push(n);
        else imgs.push(...n.querySelectorAll('img'));
      }
    }
    for (const im of imgs) emitImage(im, blockZ, blockIdx);

    const runs = collectInlineRuns(nodes, containerEl, false);
    if (runs.length === 0) return false;

    const range = document.createRange();
    range.setStartBefore(nodes[0]);
    range.setEndAfter(nodes[nodes.length - 1]);
    const rRect = range.getBoundingClientRect();
    const cbox = contentBoxOf(containerEl);
    const rx = rRect.width > 0 ? (rRect.left - sx) : cbox.x;
    const ry = rRect.height > 0 ? (rRect.top - sy) : cbox.y;
    const rw = Math.max(rRect.width, (cbox.x + cbox.width) - rx);
    const rh = Math.max(rRect.height, px(cbox.cs.fontSize) * 1.25);
    const gutter = markerOverride ? listGutterPx(containerEl, rx) : 0;
    emitFlowParagraphBox(
      { x: rx, y: ry, width: rw, height: rh },
      runs,
      cbox.cs,
      blockZ,
      blockIdx,
      markerOverride,
      gutter
    );
    return true;
  }

  function walkContainer(el, blockZ, blockIdx, isRootBlock, pendingLiMarker) {
    if (isHidden(el)) return;
    const tag = el.tagName;
    if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'ASIDE') return;

    if (tag === 'HR') {
      const r = el.getBoundingClientRect();
      if (r.width > 0) {
        const cs = getComputedStyle(el);
        const btW = cs.borderTopStyle !== 'none' ? px(cs.borderTopWidth) : 0;
        const h = Math.max(r.height, btW, 2);
        const col = parseColor(cs.backgroundColor) || parseColor(cs.borderTopColor) || { r: 180, g: 186, b: 196, a: 1 };
        const rad = px(cs.borderTopLeftRadius);
        rules.push({
          layer: [blockZ, blockIdx, 2, ++itemCounter],
          x: r.left - sx,
          y: r.top - sy,
          width: r.width,
          height: h,
          color: col,
          radiusPx: rad,
        });
      }
      return;
    }

    if (tag === 'IMG') {
      emitImage(el, blockZ, blockIdx);
      return;
    }

    if (tag === 'SVG') {
      emitInlineSvg(el, blockZ, blockIdx);
      return;
    }

    if (tag === 'FIGURE') {
      for (const ch of el.children) {
        if (ch.tagName === 'IMG') emitImage(ch, blockZ, blockIdx);
        else if (ch.tagName === 'SVG') emitInlineSvg(ch, blockZ, blockIdx);
      }
      return;
    }

    if (tag === 'PRE') {
      emitPreCodeBlock(el, blockZ, blockIdx);
      return;
    }

    if (tag === 'TABLE') {
      emitTable(el, blockZ, blockIdx);
      return;
    }

    if (/^H[1-6]$/.test(tag) || tag === 'P') {
      // Emit any embedded images inside <p>
      for (const im of el.querySelectorAll('img')) emitImage(im, blockZ, blockIdx);
      const cbox = contentBoxOf(el);
      const runs = collectInlineRuns(Array.from(el.childNodes), el, false);
      const gutter = pendingLiMarker ? listGutterPx(el.parentElement || el, cbox.x) : 0;
      emitFlowParagraphBox(cbox, runs, cbox.cs, blockZ, blockIdx, pendingLiMarker, gutter);
      return;
    }

    if (tag === 'DIV' || tag === 'BLOCKQUOTE' || tag === 'SECTION' || tag === 'ARTICLE') {
      extractCardIfStyled(el, blockZ, blockIdx, isRootBlock ? 0 : 1);
    }

    let markerToAssign = tag === 'LI' ? listMarkerFor(el) : null;
    let inlineBuf = [];
    for (const child of el.childNodes) {
      const isBlockChild = child.nodeType === Node.ELEMENT_NODE && BLOCK_TAGS.has(child.tagName);
      if (isBlockChild) {
        if (flushInlineSlice(inlineBuf, el, blockZ, blockIdx, markerToAssign)) {
          markerToAssign = null;
        }
        inlineBuf = [];
        const passMarker = (markerToAssign && child.tagName === 'P') ? markerToAssign : null;
        if (passMarker) markerToAssign = null;
        walkContainer(child, blockZ, blockIdx, false, passMarker);
      } else {
        inlineBuf.push(child);
      }
    }
    flushInlineSlice(inlineBuf, el, blockZ, blockIdx, markerToAssign);
  }

  const bodyEl = slide.querySelector('.slide-body') || slide;
  const topChildren = Array.from(bodyEl.children);
  topChildren.forEach((topEl, bIdx) => {
    const zRaw = parseInt(getComputedStyle(topEl).zIndex, 10);
    const blockZ = Number.isFinite(zRaw) ? zRaw : 10;
    walkContainer(topEl, blockZ, bIdx, true, null);
  });

  function extractNotesText(notesEl) {
    if (!notesEl) return '';
    function serializeChildren(parent, listDepth) {
      const chunks = [];
      for (const ch of parent.children) {
        const t = ch.tagName;
        if (t === 'UL' || t === 'OL') {
          let num = parseInt(ch.getAttribute('start') || '1', 10) || 1;
          const lines = [];
          for (const li of ch.children) {
            if (li.tagName !== 'LI') continue;
            const prefix = '  '.repeat(listDepth) + (t === 'UL' ? '• ' : `${num++}. `);
            const inlineNodes = Array.from(li.childNodes).filter(
              n => !(n.nodeType === Node.ELEMENT_NODE && (n.tagName === 'UL' || n.tagName === 'OL'))
            );
            let head = inlineNodes.map(n => (n.textContent || '')).join('').replace(/\s+/g, ' ').trim();
            if (head) lines.push(prefix + head);
            for (const sub of li.children) {
              if (sub.tagName === 'UL' || sub.tagName === 'OL') {
                const nested = serializeChildren(li, listDepth + 1);
                if (nested) lines.push(nested);
                break;
              }
            }
          }
          if (lines.length > 0) chunks.push(lines.join('\n'));
        } else if (t === 'PRE') {
          const codeTxt = (ch.textContent || '').replace(/\n+$/, '');
          if (codeTxt) chunks.push(codeTxt);
        } else {
          const txt = (ch.textContent || '').replace(/\s+/g, ' ').trim();
          if (txt) chunks.push(txt);
        }
      }
      if (chunks.length > 0) return chunks.join('\n\n');
      return (parent.textContent || '').trim();
    }
    return serializeChildren(notesEl, 0).trim();
  }

  const notesEl = slide.querySelector('aside.slide-notes');
  return {
    index: slideIndex + 1,
    defaultEa,
    bg: slideBg,
    cards,
    rules,
    images,
    tables,
    textBoxes,
    notesText: extractNotesText(notesEl),
  };
}
"""


def _parse_color(raw: dict[str, Any] | None) -> PptxColor | None:
    """Convert a JS color dictionary into a PptxColor instance."""
    if not raw:
        return None
    r = max(0, min(255, int(raw.get("r", 0))))
    g = max(0, min(255, int(raw.get("g", 0))))
    b = max(0, min(255, int(raw.get("b", 0))))
    a = max(0.0, min(1.0, float(raw.get("a", 1.0))))
    return PptxColor(rgb=(r, g, b), alpha=a)


def _parse_layer(raw_layer: list[Any]) -> LayerKey:
    """Convert a 4-element JS layer array into a typed LayerKey tuple."""
    return (
        int(raw_layer[0]),
        int(raw_layer[1]),
        int(raw_layer[2]),
        int(raw_layer[3]),
    )


def _parse_align(raw: str) -> AlignType:
    """Normalize horizontal alignment literal."""
    if raw == "center":
        return "center"
    if raw == "right":
        return "right"
    if raw == "justify":
        return "justify"
    return "left"


def _parse_valign(raw: str) -> ValignType:
    """Normalize vertical alignment literal."""
    if raw == "top":
        return "top"
    if raw == "bottom":
        return "bottom"
    return "middle"


def _parse_run(raw: dict[str, Any]) -> PptxRun:
    """Parse a single inline run dictionary from Playwright evaluation."""
    color = _parse_color(raw.get("color")) or PptxColor((32, 33, 36), 1.0)
    return PptxRun(
        text=str(raw.get("text", "")),
        font_family=str(raw.get("latin", "Calibri")),
        ea_font_family=str(raw.get("ea", "Noto Sans JP")),
        font_size_px=float(raw.get("fontSize", 20.0)),
        color=color,
        bold=bool(raw.get("bold", False)),
        italic=bool(raw.get("italic", False)),
        underline=bool(raw.get("underline", False)),
        strike=bool(raw.get("strike", False)),
        code_bg=_parse_color(raw.get("codeBg")),
        href=str(raw["href"]) if raw.get("href") else None,
        is_line_break=bool(raw.get("br", False)),
    )


def _parse_paragraph(raw: dict[str, Any]) -> PptxParagraph:
    """Parse a PptxParagraph dictionary."""
    runs = [_parse_run(r) for r in raw.get("runs", [])]
    return PptxParagraph(
        runs=runs,
        align=_parse_align(str(raw.get("align", "left"))),
        line_height_ratio=float(raw.get("lineHeightRatio", 1.35)),
        space_before_px=float(raw.get("spaceBeforePx", 0.0)),
        space_after_px=float(raw.get("spaceAfterPx", 0.0)),
        bullet_prefix=str(raw["bulletPrefix"]) if raw.get("bulletPrefix") else None,
        hanging_indent_px=float(raw.get("hangingIndentPx", 0.0)),
    )


def _parse_border_side(raw: dict[str, Any] | None) -> tuple[float, PptxColor] | None:
    """Parse a table cell border side specification."""
    if not raw:
        return None
    col = _parse_color(raw.get("color"))
    width = float(raw.get("widthPx", 0.0))
    if col is None or width <= 0:
        return None
    return width, col


def _parse_table(raw: dict[str, Any]) -> PptxTable:
    """Parse a PptxTable dictionary."""
    rows: list[list[PptxTableCell]] = []
    for raw_row in raw.get("rows", []):
        row_cells: list[PptxTableCell] = []
        for cell in raw_row:
            row_cells.append(
                PptxTableCell(
                    paragraphs=[_parse_paragraph(p) for p in cell.get("paragraphs", [])],
                    bg=_parse_color(cell.get("bg")),
                    border_top=_parse_border_side(cell.get("borderTop")),
                    border_bottom=_parse_border_side(cell.get("borderBottom")),
                    border_left=_parse_border_side(cell.get("borderLeft")),
                    border_right=_parse_border_side(cell.get("borderRight")),
                    pad_top_px=float(cell.get("padTopPx", 8.0)),
                    pad_right_px=float(cell.get("padRightPx", 12.0)),
                    pad_bottom_px=float(cell.get("padBottomPx", 8.0)),
                    pad_left_px=float(cell.get("padLeftPx", 12.0)),
                    valign=_parse_valign(str(cell.get("valign", "middle"))),
                )
            )
        rows.append(row_cells)
    return PptxTable(
        layer=_parse_layer(raw["layer"]),
        x=float(raw["x"]),
        y=float(raw["y"]),
        width=float(raw["width"]),
        height=float(raw["height"]),
        col_widths_px=[float(w) for w in raw.get("colWidthsPx", [])],
        row_heights_px=[float(h) for h in raw.get("rowHeightsPx", [])],
        rows=rows,
    )


def _resolve_slide_image(
    page: Page,
    raw_img: dict[str, Any],
    html_dir: str,
    svg_capture_dir: str,
) -> PptxImage | None:
    """Resolve local raster image path or capture fallback SVG screenshot."""
    capture_id = raw_img.get("captureId")
    if capture_id:
        os.makedirs(svg_capture_dir, exist_ok=True)
        out_png = os.path.join(svg_capture_dir, f"{capture_id}.png")
        with contextlib.suppress(Exception):
            page.locator(f'[data-pptx-svg-capture="{capture_id}"]').first.screenshot(
                path=out_png,
                omit_background=True,
            )
        if not os.path.isfile(out_png):
            return None
        img_path = out_png
    else:
        src = str(raw_img.get("src", ""))
        if src.startswith("file://"):
            parsed = urllib.parse.urlparse(src)
            img_path = urllib.request.url2pathname(parsed.path) if hasattr(urllib, "request") else parsed.path
        else:
            clean_rel = urllib.parse.unquote(src.split("?", 1)[0].split("#", 1)[0])
            img_path = os.path.normpath(os.path.join(html_dir, clean_rel))
        if not os.path.isfile(img_path):
            return None

    return PptxImage(
        layer=_parse_layer(raw_img["layer"]),
        x=float(raw_img["x"]),
        y=float(raw_img["y"]),
        width=float(raw_img["width"]),
        height=float(raw_img["height"]),
        image_path=img_path,
    )


def _build_slide_elements(
    page: Page,
    raw_slide: dict[str, Any],
    html_dir: str,
    svg_capture_dir: str,
) -> list[SlideElement]:
    """Convert raw JS dictionaries into layer-sorted SlideElement instances."""
    elements: list[SlideElement] = []

    for rc in raw_slide.get("cards", []):
        elements.append(
            PptxCard(
                layer=_parse_layer(rc["layer"]),
                x=float(rc["x"]),
                y=float(rc["y"]),
                width=float(rc["width"]),
                height=float(rc["height"]),
                bg=_parse_color(rc.get("bg")),
                border_color=_parse_color(rc.get("borderColor")),
                border_width_px=float(rc.get("borderWidthPx", 0.0)),
                radius_px=float(rc.get("radiusPx", 0.0)),
                left_accent_color=_parse_color(rc.get("leftAccentColor")),
                left_accent_width_px=float(rc.get("leftAccentWidthPx", 0.0)),
            )
        )

    for rr in raw_slide.get("rules", []):
        col = _parse_color(rr.get("color")) or PptxColor((180, 186, 196), 1.0)
        elements.append(
            PptxRule(
                layer=_parse_layer(rr["layer"]),
                x=float(rr["x"]),
                y=float(rr["y"]),
                width=float(rr["width"]),
                height=float(rr["height"]),
                color=col,
                radius_px=float(rr.get("radiusPx", 0.0)),
            )
        )

    for ri in raw_slide.get("images", []):
        resolved = _resolve_slide_image(page, ri, html_dir, svg_capture_dir)
        if resolved is not None:
            elements.append(resolved)

    for rt in raw_slide.get("tables", []):
        elements.append(_parse_table(rt))

    for rtb in raw_slide.get("textBoxes", []):
        elements.append(
            PptxTextBox(
                layer=_parse_layer(rtb["layer"]),
                x=float(rtb["x"]),
                y=float(rtb["y"]),
                width=float(rtb["width"]),
                height=float(rtb["height"]),
                paragraphs=[_parse_paragraph(p) for p in rtb.get("paragraphs", [])],
                is_code=bool(rtb.get("isCode", False)),
            )
        )

    elements.sort(key=lambda item: item.layer)
    return elements


def _prepare_stage_page(page: Page, index_html_path: str) -> int:
    """Load compiled slide HTML at 1920x1080 and return slide count."""
    file_uri = Path(os.path.abspath(index_html_path)).as_uri()
    page.goto(file_uri, wait_until="domcontentloaded", timeout=15000)
    page.add_style_tag(content=_STAGE_OVERRIDE_CSS)
    with contextlib.suppress(Exception):
        page.evaluate(
            "() => Promise.race([document.fonts.ready, new Promise(r => setTimeout(r, 2000))])"
        )
    with contextlib.suppress(Exception):
        page.evaluate(
            "() => Promise.all(Array.from(document.images).map(img => img.decode().catch(() => {})))"
        )
    return int(page.evaluate("() => document.querySelectorAll('section.slide').length"))


def extract_deck_dom(
    index_html_path: str,
    svg_capture_dir: str,
) -> PptxDeckSpec:
    """Measure all slides in a compiled index.html deck via Headless Chromium at 1920x1080.

    Args:
        index_html_path: Path to compiled slide deck index.html.
        svg_capture_dir: Temporary directory for rasterizing any static SVG assets.

    Returns:
        PptxDeckSpec: Complete layout, typography, image, table, and speaker note specification.

    Raises:
        FileNotFoundError: If index_html_path does not exist.
        RuntimeError: If Playwright or Headless Chromium fails.
    """
    abs_html = os.path.abspath(index_html_path)
    if not os.path.isfile(abs_html):
        raise FileNotFoundError(f"Slide HTML file not found: '{abs_html}'")

    html_dir = os.path.dirname(abs_html)
    sync_playwright = import_sync_playwright(context_label="PPTX Export")

    slides: list[PptxSlideSpec] = []
    deck_title = "Drawlib Presentation"
    default_ea = "Noto Sans JP"

    try:
        with sync_playwright() as p:
            browser = launch_headless_chromium(p, context_label="PPTX Export")
            try:
                page = browser.new_page(
                    viewport={"width": 1920, "height": 1080},
                    device_scale_factor=2,
                )
                slide_count = _prepare_stage_page(page, abs_html)
                deck_title = str(page.title() or deck_title)

                for slide_idx in range(slide_count):
                    raw_slide = page.evaluate(_JS_EXTRACT_SLIDE, slide_idx)
                    if not isinstance(raw_slide, dict):
                        continue
                    if slide_idx == 0 and raw_slide.get("defaultEa"):
                        default_ea = str(raw_slide["defaultEa"])
                    bg_color = _parse_color(raw_slide.get("bg")) or PptxColor((255, 255, 255), 1.0)
                    elements = _build_slide_elements(page, raw_slide, html_dir, svg_capture_dir)
                    slides.append(
                        PptxSlideSpec(
                            index=int(raw_slide.get("index", slide_idx + 1)),
                            bg=bg_color,
                            elements=elements,
                            notes_text=str(raw_slide.get("notesText", "")),
                        )
                    )
            finally:
                browser.close()
    except Exception as err:
        if isinstance(err, RuntimeError):
            raise
        raise RuntimeError(f"Playwright slide DOM measurement failed: {err}") from err

    return PptxDeckSpec(
        title=deck_title,
        default_ea_font=default_ea,
        slides=slides,
    )
