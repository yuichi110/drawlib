# Styles & Theming Guide

The **Styles & Theming** section provides a comprehensive guide to Drawlib's design system, including the color palette, typography and font registration, built-in preset theme catalogs, and custom style authoring.

---

## 1. Fundamentals: Colors & Fonts

- [Color System & Utilities](./color.md): Built-in color palettes (`Colors`, `Colors140`, `ColorsEssentials`, `ColorsMonochrome`), HEX/RGB color creation, transparency, and background color settings.
- [Fonts System](./font.md): Default CJK/Latin typography (`Font`), specialized font families (`FontSansSerif`, `FontSerif`, `FontMonoSpace`, `FontRoboto`, local language fonts), and custom TrueType font loading via `FontFile`.

---

## 2. Official Preset Style Catalogs

Preset styles unify colors, line weights, fills, and typography into intuitive string identifiers (e.g., `"blue_flat"`, `"red_outline"`, `"green_soft"`).

- [Official Default Preset Styles](./official_default.md): Core 5-color palette (Red, Green, Blue, Black, White) with shape and line variations.
- [Official Essentials Preset Styles](./official_essentials.md): Rich 25-color balanced palette covering corporate and modern presentation aesthetics.
- [Official Monochrome Preset Styles](./official_monochrome.md): Clean grayscale palette from Charcoal to Snow for print-friendly or minimal technical documentation.

---

## 3. Custom Presets & Advanced Theming

- [Custom Preset Creation](./create.md): Defining and registering your own domain-specific styling themes by subclassing `BasePresetStyles`.
- [Advanced Style Topics](./advanced_topics.md): Advanced style retrieval, cloning, dynamic overrides, and preset merging strategies.

---

## Navigation

- [Back to Main Index](../index.md)

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
