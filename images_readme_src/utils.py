# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Drawlib user utility functions and constants."""

from __future__ import annotations

# Define reusable drawing helper functions, macro components,
# or project-specific constants in this file.
#
# All top-level functions and variables defined here are automatically
# accessible in drawing code via `drawlib.utils`.
#
# Example:
#
# from drawlib.shapes import rectangle
# from drawlib.styles import styles
# from drawlib.text import text
#
# PROJECT_NAME = "My Documentation Project"
# BRAND_PRIMARY = "#1a73e8"
#
# def service_card(xy: tuple[float, float], title: str, subtitle: str = "") -> None:
#     """Draw a reusable service card component."""
#     x, y = xy
#     rectangle(xy, width=32, height=18, r=2, style="blue_flat")
#     text((x, y + 3), title, style="white_bold")
#     if subtitle:
#         text((x, y - 3), subtitle, style="white_light")
#
# In your drawing scripts or embedded markdown code blocks:
#     from drawlib.utils import PROJECT_NAME, service_card
#     service_card((50, 50), "Auth Service")
