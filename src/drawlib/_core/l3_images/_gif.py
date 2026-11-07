# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Palette quantization helpers for crisp, dither-free diagram GIF export."""

from __future__ import annotations

from PIL import Image


def quantize_pil_for_gif(image: Image.Image) -> tuple[Image.Image, int | None]:
    """Quantize a PIL image into an indexed ``P``-mode frame optimized for diagrams and text.

    Uses Median Cut palette selection with dithering disabled (``Image.Dither.NONE``)
    so flat design-token surfaces (such as ``Styles.Neutral``) and anti-aliased labels
    remain crisp without Floyd-Steinberg grain noise. When transparent pixels are present,
    palette index ``255`` is reserved as the dedicated 1-bit GIF transparency index.

    Args:
        image: Source PIL image frame.

    Returns:
        tuple[Image.Image, int | None]: ``(quantized_p_frame, transparency_index)``.
    """
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    extrema = alpha.getextrema()
    min_alpha = extrema[0] if isinstance(extrema[0], int) else 255

    if min_alpha >= 255:
        rgb = rgba.convert("RGB")
        quantized = rgb.quantize(
            colors=256,
            method=Image.Quantize.MEDIANCUT,
            dither=Image.Dither.NONE,
        )
        return quantized, None

    # Composite onto white before quantizing RGB so anti-aliased text/shape edges
    # with alpha >= 128 blend cleanly instead of picking up dark matte fringes.
    white_bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
    composited_rgb = Image.alpha_composite(white_bg, rgba).convert("RGB")
    quantized_255 = composited_rgb.quantize(
        colors=255,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    )

    raw_palette = quantized_255.getpalette() or []
    padded_palette = (raw_palette + [0] * 768)[:768]
    transparent_mask = alpha.point(lambda a: 255 if a < 128 else 0, mode="L")
    transparent_layer = Image.new("P", rgba.size, 255)
    combined = Image.composite(transparent_layer, quantized_255, transparent_mask)
    combined.putpalette(padded_palette)
    return combined, 255
