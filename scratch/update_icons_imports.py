import glob
import os

files = glob.glob("src/**/*.py", recursive=True) + glob.glob("tests/**/*.py", recursive=True) + glob.glob("tasks/**/*.py", recursive=True)

for path in files:
    if not os.path.isfile(path):
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    orig = content
    content = content.replace("drawlib._core.l6_icons", "drawlib._icons")

    if content != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {path}")
