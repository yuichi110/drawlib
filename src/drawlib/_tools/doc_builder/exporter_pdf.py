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

import os


def export_html_to_pdf(html_content: str, output_path: str) -> None:
    """Export HTML content to PDF file using Playwright and headless Chromium.

    Args:
        html_content (str): HTML content string.
        output_path (str): Output PDF file path.

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
