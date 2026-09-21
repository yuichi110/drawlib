# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""PDF exporter using native headless Chromium-based browser (Chrome, Chromium, Edge)."""

from __future__ import annotations

import os
import shutil
import subprocess  # noqa: S404
import sys
import tempfile


def find_system_browser() -> str | None:
    """Locate a Chromium-based browser (Google Chrome, Chromium, or Microsoft Edge) on the system.

    Checks:
        1. Environment variable DRAWLIB_CHROME_PATH
        2. System PATH via shutil.which
        3. Standard installation paths for macOS and Windows

    Returns:
        str | None: Absolute path to the browser executable, or None if not found.
    """
    custom_path = os.environ.get("DRAWLIB_CHROME_PATH")
    if custom_path:
        expanded = os.path.expanduser(os.path.expandvars(custom_path))
        if os.path.isfile(expanded) and os.access(expanded, os.X_OK):
            return expanded

    candidates = [
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
        "msedge",
        "microsoft-edge",
    ]
    for name in candidates:
        found = shutil.which(name)
        if found:
            return found

    if sys.platform == "darwin":
        darwin_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        ]
        for p in darwin_paths:
            if os.path.isfile(p) and os.access(p, os.X_OK):
                return p
    elif sys.platform == "win32":
        win_roots = [
            os.environ.get("PROGRAMFILES", r"C:\Program Files"),
            os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"),
            os.environ.get("LOCALAPPDATA", r"C:\Users\Default\AppData\Local"),
        ]
        rel_paths = [
            r"Google\Chrome\Application\chrome.exe",
            r"Microsoft\Edge\Application\msedge.exe",
            r"Chromium\Application\chrome.exe",
        ]
        for root in win_roots:
            if not root:
                continue
            for rel in rel_paths:
                p = os.path.join(root, rel)
                if os.path.isfile(p):
                    return p

    return None


def export_html_to_pdf(html_content: str, output_path: str) -> None:
    """Export HTML content to PDF file using a headless Chromium browser.

    Args:
        html_content (str): HTML content string.
        output_path (str): Output PDF file path.

    Raises:
        RuntimeError: If no supported browser is found or PDF generation fails.
    """
    browser_path = find_system_browser()
    if not browser_path:
        msg = (
            "No compatible browser (Google Chrome, Chromium, or Microsoft Edge) was found on your system.\n"
            "PDF export requires a Chromium-based browser with headless printing capability.\n\n"
            "To resolve this:\n"
            "1. Install Google Chrome (https://www.google.com/chrome/), Chromium, or Microsoft Edge.\n"
            "2. If your browser is installed in a non-standard location,\n"
            "   set the DRAWLIB_CHROME_PATH environment variable:\n"
            '   export DRAWLIB_CHROME_PATH="/path/to/google-chrome"\n'
        )
        raise RuntimeError(msg)

    abs_output = os.path.abspath(output_path)
    output_dir = os.path.dirname(abs_output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    temp_html = tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False)
    temp_html_path = temp_html.name
    try:
        temp_html.write(html_content)
        temp_html.flush()
        temp_html.close()

        cmd = [
            browser_path,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={abs_output}",
            temp_html_path,
        ]

        result = subprocess.run(  # noqa: S603
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=60,
        )

        if result.returncode != 0:
            stderr_text = result.stderr.decode("utf-8", errors="replace").strip()
            msg = f"Browser PDF generation failed with code {result.returncode}:\n{stderr_text}"
            raise RuntimeError(msg)

        if not os.path.isfile(abs_output) or os.path.getsize(abs_output) == 0:
            msg = f"Browser command succeeded but output PDF file '{abs_output}' was not created or is empty."
            raise RuntimeError(msg)

    except subprocess.TimeoutExpired as err:
        msg = "Browser timed out while generating PDF (limit: 60s)."
        raise RuntimeError(msg) from err
    finally:
        if os.path.exists(temp_html_path):
            try:
                os.remove(temp_html_path)
            except OSError:
                pass
