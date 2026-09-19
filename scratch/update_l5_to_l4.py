import glob
import os

files = glob.glob("src/**/*.py", recursive=True) + glob.glob("tests/**/*.py", recursive=True) + glob.glob("tasks/**/*.py", recursive=True) + glob.glob("tasks/**/*.yml", recursive=True) + glob.glob("tasks/**/*.yaml", recursive=True)

for path in files:
    if not os.path.isfile(path):
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    orig = content
    content = content.replace("drawlib._core.l5_canvas_utils", "drawlib._core.l4_canvas_utils")
    content = content.replace("drawlib._core.l5_canvas", "drawlib._core.l4_canvas")
    content = content.replace("tests/l5_canvas_utils", "tests/l4_canvas_utils")
    content = content.replace("tests/l5_canvas", "tests/l4_canvas")
    content = content.replace("output_tests/l5_canvas", "output_tests/l4_canvas")
    content = content.replace("l5_canvas_utils", "l4_canvas_utils")
    content = content.replace("l5_canvas", "l4_canvas")

    if content != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {path}")
