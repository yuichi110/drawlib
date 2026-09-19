# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""PDF exporter using Playwright or Headless browser."""

import os


def export_html_to_pdf(html_content: str, output_path: str) -> None:
    """Export HTML content to PDF file using Playwright.

    Args:
        html_content (str): HTML content string.
        output_path (str): Output PDF file path.

    Raises:
        ImportError: If Playwright is not installed.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as err:
        msg = (
            "Playwright is required for PDF export. "
            "Please install it using 'pip install playwright' and run 'playwright install chromium'."
        )
        raise ImportError(msg) from err

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html_content)
        page.pdf(path=output_path, format="A4", print_background=True)
        browser.close()
