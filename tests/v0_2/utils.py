# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import io
from pathlib import Path

from PIL import Image, ImageChops


def check_image_match(
    generated_binary: bytes,
    correct_binary: bytes | None = None,
    correct_file: str | Path | None = None,
    threshold: float = 0.99,
) -> bool:
    """Compare two image binaries.

    Compares two image binaries and returns True if their pixel match percentage
    meets or exceeds the specified threshold (0.0 - 100.0).
    """
    # 1. Validate the threshold (raise an error if outside 0.0 - 100.0)
    if not (0.0 <= threshold <= 100.0):
        raise ValueError(f"Error: Threshold must be between 0.0 and 100.0. (Input value: {threshold})")

    # 2. Validate exclusive inputs (must provide exactly one of the two)
    if (correct_binary is None) == (correct_file is None):
        raise ValueError("Error: You must provide exactly one of 'correct_binary' or 'correct_file'.")

    # 3. If a file path is provided, read it into bytes
    if correct_file is not None:
        try:
            with open(correct_file, "rb") as f:
                correct_binary = f.read()
        except Exception as e:
            print(f"Failed to read the file '{correct_file}': {e}")
            return False

    try:
        # 4. Load the binary data as PIL images in memory and convert to RGB
        img1 = Image.open(io.BytesIO(generated_binary)).convert("RGB")
        img2 = Image.open(io.BytesIO(correct_binary)).convert("RGB")
    except Exception as e:
        print(f"Failed to load images: {e}")
        return False

    # 5. If image sizes differ, they cannot match
    if img1.size != img2.size:
        print(f"Image sizes differ: {img1.size} vs {img2.size}")
        return False

    # 6. Get the difference between the two images and calculate the histogram
    diff = ImageChops.difference(img1, img2)
    diff_gray = diff.convert("L")
    hist = diff_gray.histogram()

    # 7. Get the number of exactly matching pixels and calculate the percentage
    exact_match_pixels = hist[0]
    total_pixels = img1.width * img1.height
    match_percentage = (exact_match_pixels / total_pixels) * 100

    print(f"Exact pixel match rate: {match_percentage:.2f}% (Target threshold: {threshold:.2f}%)")

    # 8. Return whether the match percentage meets the threshold
    return match_percentage >= threshold
