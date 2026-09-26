# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""PDF exporter using Playwright and headless Chromium browser."""

from __future__ import annotations

import datetime
import os
import re


def _get_fixed_pdf_date_bytes(target_len: int) -> bytes:
    """Generate fixed PDF date bytes with exactly target_len bytes."""
    source_date_epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if source_date_epoch:
        try:
            epoch_val = int(source_date_epoch)
            dt = datetime.datetime.fromtimestamp(epoch_val, tz=datetime.timezone.utc)
            date_str = dt.strftime("D:%Y%m%d%H%M%S+00'00'")
        except (ValueError, OverflowError):
            date_str = "D:20260101000000+00'00'"
    else:
        date_str = "D:20260101000000+00'00'"

    raw_bytes = date_str.encode("ascii")
    if len(raw_bytes) == target_len:
        return raw_bytes
    if len(raw_bytes) > target_len:
        return raw_bytes[:target_len]
    return raw_bytes.ljust(target_len, b"0")


def normalize_pdf_timestamps(pdf_path: str) -> None:
    """Normalize CreationDate and ModDate in a PDF file to ensure deterministic builds.

    Args:
        pdf_path (str): Path to the generated PDF file.
    """
    if not os.path.isfile(pdf_path):
        return

    with open(pdf_path, "rb") as f:
        content = f.read()

    def _replace_date(match: re.Match[bytes]) -> bytes:
        key_prefix = match.group(1)
        orig_val = match.group(2)
        fixed_val = _get_fixed_pdf_date_bytes(len(orig_val))
        return key_prefix + fixed_val + b")"

    # Chromium / Skia formats dates as /CreationDate (D:YYYYMMDDHHmmSS+00'00')
    pattern = re.compile(rb"(/CreationDate\s*\(|/ModDate\s*\()(D:[0-9]{14}[^)]*)\)")
    new_content = pattern.sub(_replace_date, content)

    # Cross-reference safety: ensure file size is identical to avoid invalidating the xref table
    if len(new_content) != len(content):
        return

    if new_content != content:
        with open(pdf_path, "wb") as f:
            f.write(new_content)


def export_html_to_pdf(html_content: str, output_path: str, timestamp: bool = False) -> None:
    """Export HTML content to PDF file using Playwright and headless Chromium.

    Args:
        html_content (str): HTML content string.
        output_path (str): Output PDF file path.
        timestamp (bool): If True, preserve current build timestamp in PDF metadata.
            If False (default), normalize timestamps for deterministic builds.

    Raises:
        RuntimeError: If Playwright or Chromium is not installed, or if PDF generation fails.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as err:
        msg = (
            "\n[PDF Export Error]\n"
            "PDF export requires the 'playwright' package and a headless Chromium browser.\n\n"
            "1. Install Playwright:\n"
            "   - For uv users:\n"
            '       uv add "drawlib[pdf]"\n'
            "     (or: uv add playwright)\n\n"
            "   - For pip users:\n"
            '       pip install "drawlib[pdf]"\n'
            "     (or: pip install playwright)\n\n"
            "2. Download the headless Chromium browser:\n"
            "   - For uv users:\n"
            "       uv run playwright install chromium\n\n"
            "   - For pip users:\n"
            "       playwright install chromium\n"
        )
        raise RuntimeError(msg) from err

    abs_output = os.path.abspath(output_path)
    output_dir = os.path.dirname(abs_output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
            except Exception as err:
                err_str = str(err)
                if "Executable doesn't exist" in err_str or "playwright install" in err_str:
                    msg = (
                        "\n[PDF Export Error]\n"
                        "Playwright is installed, but the headless Chromium browser is missing.\n\n"
                        "To download Chromium, run:\n"
                        "  - For uv users:\n"
                        "      uv run playwright install chromium\n\n"
                        "  - For pip users:\n"
                        "      playwright install chromium\n"
                    )
                    raise RuntimeError(msg) from err
                raise RuntimeError(f"Failed to launch Chromium browser: {err}") from err

            try:
                page = browser.new_page()
                page.set_content(html_content, wait_until="networkidle")
                page.pdf(
                    path=abs_output,
                    format="A4",
                    print_background=True,
                    margin={
                        "top": "15mm",
                        "bottom": "15mm",
                        "left": "15mm",
                        "right": "15mm",
                    },
                )
            finally:
                browser.close()

    except Exception as err:
        if isinstance(err, RuntimeError):
            raise
        raise RuntimeError(f"Playwright PDF generation failed: {err}") from err

    if not os.path.isfile(abs_output) or os.path.getsize(abs_output) == 0:
        msg = f"Playwright command completed but output PDF file '{abs_output}' was not created or is empty."
        raise RuntimeError(msg)

    if not timestamp:
        normalize_pdf_timestamps(abs_output)
