# 1. test_names.py
with open("tests/l3_fonts/test_names.py", "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace("text_font=Font.SANSSERIF_LIGHT", "font=Font.SANSSERIF_LIGHT")
c = c.replace("loaded.text_font", "loaded.font")
with open("tests/l3_fonts/test_names.py", "w", encoding="utf-8") as f:
    f.write(c)

# 2. test_system_default.py
with open("tests/l3_styles/test_system_default.py", "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace("SYSTEM_DEFAULT_ICON_STYLE.style ==", "SYSTEM_DEFAULT_ICON_STYLE.icon_style ==")
c = c.replace("SYSTEM_DEFAULT_LINE_STYLE.style ==", "SYSTEM_DEFAULT_LINE_STYLE.line_style ==")
with open("tests/l3_styles/test_system_default.py", "w", encoding="utf-8") as f:
    f.write(c)

# 3. test_arrow.py
with open("tests/l5_canvas/test_arrow.py", "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace('ellipse(xy=(25, 25), width=30, height=30, line_style="dashed")', 'ellipse(xy=(25, 25), width=30, height=30, style="dashed")')
c = c.replace('ellipse(xy=(25, 75), width=30, height=30, line_style="dashed")', 'ellipse(xy=(25, 75), width=30, height=30, style="dashed")')
c = c.replace('ellipse(xy=(75, 25), width=40, height=20, line_style="dashed")', 'ellipse(xy=(75, 25), width=40, height=20, style="dashed")')
c = c.replace('ellipse(xy=(75, 75), width=40, height=20, line_style="dashed", text_angle=45)', 'ellipse(xy=(75, 75), width=40, height=20, style="dashed", angle=45)')
c = c.replace('text_angle=45,', 'angle=45,')
c = c.replace('text_angle=90', 'angle=90')
with open("tests/l5_canvas/test_arrow.py", "w", encoding="utf-8") as f:
    f.write(c)

# 4. test_base.py
with open("tests/l5_canvas/test_base.py", "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace("text_angle=45", "angle=45")
c = c.replace("text_angle=90", "angle=90")
c = c.replace("text_angle=135", "angle=135")
with open("tests/l5_canvas/test_base.py", "w", encoding="utf-8") as f:
    f.write(c)

# 5. test_image.py
with open("tests/l5_canvas/test_image.py", "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace("text_angle=45", "angle=45")
c = c.replace("text_angle=90", "angle=90")
c = c.replace("text_angle=135", "angle=135")
with open("tests/l5_canvas/test_image.py", "w", encoding="utf-8") as f:
    f.write(c)

# 6. test_line.py
with open("tests/l5_canvas/test_line.py", "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace('LineStyle(line_width=3, text_color=Colors.Red, style="dashdot", fill_alpha=0.5)', 'LineStyle(line_width=3, text_color=Colors.Red, line_style="dashdot", fill_alpha=0.5)')
c = c.replace('text_angle=45', 'angle=45')
c = c.replace('ellipse((50, 50), 30, 30, line_style="dashed")', 'ellipse((50, 50), 30, 30, style="dashed")')
with open("tests/l5_canvas/test_line.py", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated remaining files.")
