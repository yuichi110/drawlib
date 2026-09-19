import glob
import re

files = glob.glob("tests/**/*.py", recursive=True)

for path in files:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    orig = content

    # 1. Fix img1.text_size, img1.line_width in tests/utils.py
    if "utils.py" in path:
        content = content.replace("img1.text_size", "img1.size")
        content = content.replace("img2.text_size", "img2.size")
        content = content.replace("img1.line_width", "img1.width")
        content = content.replace("img2.line_width", "img2.width")

    # 2. Fix ColorUtil.get_mplot_rgba fill_alpha -> alpha
    content = content.replace("ColorUtil.get_mplot_rgba((255, 127, 0), fill_alpha=0.75)", "ColorUtil.get_mplot_rgba((255, 127, 0), alpha=0.75)")
    content = content.replace("ColorUtil.get_mplot_rgba((0, 255, 127, 0.5), fill_alpha=0.8)", "ColorUtil.get_mplot_rgba((0, 255, 127, 0.5), alpha=0.8)")

    # 3. Fix sourcecode text_font= -> font=
    content = re.sub(r'(\bsourcecode\([^)]*?\b)text_font=', r'\1font=', content, flags=re.DOTALL)
    # Also direct replacements where sourcecode or code blocks are called:
    content = content.replace("text_font=FontSourceCode.", "font=FontSourceCode.")

    # 4. Fix chevron line_width= -> width=
    # In chevron(xy=..., line_width=10, height=15, corner_angle=60)
    content = re.sub(r'(\bchevron\([^)]*?\b)line_width=', r'\1width=', content)

    # 5. Fix text(..., text_size=...) -> size=..., text(..., text_angle=...) -> angle=...
    # text(...) takes size= and angle=, NOT text_size= or text_angle= (unless inside style=Style(...))
    # Let's target direct keyword args to drawing functions
    content = re.sub(r'(\btext\([^)]*?\b)text_size=(\d+)', r'\1size=\2', content)
    content = re.sub(r'(\btext\([^)]*?\b)text_angle=(\d+)', r'\1angle=\2', content)

    # 6. Fix shape text_angle= -> angle= for donuts, fan, triangle, polygon, trapezoid, rhombus, chevron, star, icon
    for func in ["donuts", "fan", "triangle", "polygon", "trapezoid", "rhombus", "chevron", "star", "icon", "image", "rectangle", "ellipse", "regular_polygon"]:
        content = re.sub(rf'(\b{func}\([^)]*?\b)text_angle=', r'\1angle=', content)

    if content != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {path}")
