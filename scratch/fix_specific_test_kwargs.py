# Fix test_patches.py
with open("tests/l5_canvas/test_patches.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('text_angle=45', 'angle=45')
content = content.replace('text_angle=120', 'angle=120')
content = content.replace('line_width=40,', 'width=40,')
content = content.replace('line_width=10,', 'width=10,')
content = content.replace('line_width=10 style=', 'width=10, style=')

with open("tests/l5_canvas/test_patches.py", "w", encoding="utf-8") as f:
    f.write(content)

# Fix test_polygon.py
with open("tests/l5_canvas/test_polygon.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('text_angle=45', 'angle=45')
content = content.replace('line_width=10,', 'width=10,')

with open("tests/l5_canvas/test_polygon.py", "w", encoding="utf-8") as f:
    f.write(content)

# Fix test_text.py
with open("tests/l5_canvas/test_text.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('text_size=36', 'size=36')
content = content.replace('text_angle=90', 'angle=90')

with open("tests/l5_canvas/test_text.py", "w", encoding="utf-8") as f:
    f.write(content)

# Fix test_phosphor.py
with open("tests/l6_icons/test_phosphor.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('text_angle=45', 'angle=45')

with open("tests/l6_icons/test_phosphor.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated test files.")
