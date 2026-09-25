# About drawlib


Drawlib is a pure Python drawing library designed to facilitate Illustration as Code. 
Instead of focusing solely on creating polished illustrations, Drawlib emphasizes generating illustrations directly from code.

For instance, consider the following Python code:


```python
from drawlib.canvas import save
from drawlib.colors import Colors140
from drawlib.shapes import circle

circle(
    xy=(50, 50),
    radius=30,
    style=styles.primary.patch(
        line_style="dashed",
        shape_line_color=Colors140.BlueViolet,
        shape_line_width=5,
        shape_fill_color=Colors140.Turquoise,
    ),
)
save()
```

Execute it with the following command:


```text
$ python image1.py
```


This will generate an image file:


```drawlib 450px center
from drawlib.canvas import save
from drawlib.colors import Colors140
from drawlib.shapes import circle

circle(
    xy=(50, 50),
    radius=30,
    style=styles.primary.patch(
        line_style="dashed",
        shape_line_color=Colors140.BlueViolet,
        shape_line_width=5,
        shape_fill_color=Colors140.Turquoise,
    ),
)
```

As illustrated, Drawlib generates an image corresponding to your code.

Drawlib applies style (the equivalent of CSS) to drawing content (the equivalent of HTML). 
You can apply the style directly when you draw, as shown above. 
However, specifying detailed styles is usually unnecessary. 
Instead, it is recommended to use predefined style names for styling.



# Benefit of "Illustration as Code"


In today's world, many technical documents are managed using version control systems such as Git. 
However, managing illustrations poses a challenge since they are typically binary files rather than text-based. 
Drawlib offers a solution by generating illustrations from pure Python code, allowing you to manage them with version control systems just like any other code.

Drawlib is optimized for drawing a large number of illustrations with a consistent style. 
This can be easily achieved by defining reusable styles or configuration scripts (which are simply Python code) and importing them into your illustration codes. 
Here is a typical use case of Drawlib:


```drawlib 650px center
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import arrow, rectangle
from drawlib.text import text
from drawlib.types import Style

config(width=100, height=60)

rect_width = 20
rect_height = 38
style_dashed = styles.primary.patch(line_style="dashed", shape_fill_color=Colors.White)
style_text_head = styles.primary.patch(text_size=15, text_halign="center")
style_text_left = styles.primary.patch(text_size=11, text_halign="left")
style_text_red = styles.primary.patch(text_size=11, text_halign="left", text_color=Colors.Red)
style_tree_line = styles.primary.patch(line_width=1, line_color=Colors.Gray)

def left():
    text((15, 54), "Drawlib's\nDocument Source", style=style_text_head)
    rectangle((15, 30), width=rect_width, height=rect_height, r=2, style=style_dashed)

    x = 8
    phosphor.folder((x, 45), width=3, style=styles.primary)
    text((x + 2.5, 45), "docs", style=style_text_left)
    line((x, 43), (x, 13), style=style_tree_line)

    line((x, 42), (x + 1, 42), style=style_tree_line)
    phosphor.folder((x + 3, 42), width=3, style=styles.primary)
    text((x + 5.5, 42), "commons", style=style_text_left)
    line((x + 3, 40), (x + 3, 35), style=style_tree_line)
    phosphor.file_py((x + 6, 39), width=3, style=styles.primary.patch(icon_color=Colors.Red))
    text((x + 8.5, 39), "style.py", style=style_text_red)
    line((x + 3, 39), (x + 4, 39), style=style_tree_line)
    phosphor.file_py((x + 6, 36), width=3, style=styles.primary.patch(icon_color=Colors.Red))
    text((x + 8.5, 36), "util.py", style=style_text_red)
    line((x + 3, 36), (x + 4, 36), style=style_tree_line)

    line((x, 30), (x + 1, 30), style=style_tree_line)
    phosphor.folder((x + 3, 30), width=3, style=styles.primary)
    text((x + 5.5, 30), "chapter1", style=style_text_left)
    line((x + 3, 28), (x + 3, 19), style=style_tree_line)
    phosphor.file_md((x + 6, 27), width=3, style=styles.primary)
    text((x + 8.5, 27), "doc.md", style=style_text_left)
    line((x + 3, 27), (x + 4, 27), style=style_tree_line)
    phosphor.file_py((x + 6, 24), width=3, style=styles.primary.patch(icon_color=Colors.Red))
    text((x + 8.5, 24), "img1.py", style=style_text_red)
    line((x + 3, 24), (x + 4, 24), style=style_tree_line)
    phosphor.file_py((x + 6, 21), width=3, style=styles.primary.patch(icon_color=Colors.Red))
    text((x + 8.5, 21), "img2.py", style=style_text_red)
    line((x + 3, 21), (x + 4, 21), style=style_tree_line)

    line((x, 15), (x + 1, 15), style=style_tree_line)
    phosphor.folder((x + 3, 15), width=3, style=styles.primary)
    text((x + 5.5, 15), "chapter2", style=style_text_left)

def center():
    text((50, 54), "Traditional\nDocument Source", style=style_text_head)
    rectangle((50, 30), width=rect_width, height=rect_height, r=2, style=style_dashed)

    x = 43
    phosphor.folder((x, 45), width=3, style=styles.primary)
    text((x + 2.5, 45), "docs", style=style_text_left)
    line((x, 43), (x, 13), style=style_tree_line)

    line((x, 30), (x + 1, 30), style=style_tree_line)
    phosphor.folder((x + 3, 30), width=3, style=styles.primary)
    text((x + 5.5, 30), "chapter1", style=style_text_left)
    line((x + 3, 28), (x + 3, 19), style=style_tree_line)
    phosphor.file_md((x + 6, 27), width=3, style=styles.primary)
    text((x + 8.5, 27), "doc.md", style=style_text_left)
    line((x + 3, 27), (x + 4, 27), style=style_tree_line)
    phosphor.file_image((x + 6, 24), width=3, style=styles.primary.patch(icon_color=Colors.Red))
    text((x + 8.5, 24), "img1.png", style=style_text_red)
    line((x + 3, 24), (x + 4, 24), style=style_tree_line)
    phosphor.file_image((x + 6, 21), width=3, style=styles.primary.patch(icon_color=Colors.Red))
    text((x + 8.5, 21), "img2.png", style=style_text_red)
    line((x + 3, 21), (x + 4, 21), style=style_tree_line)

    line((x, 15), (x + 1, 15), style=style_tree_line)
    phosphor.folder((x + 3, 15), width=3, style=styles.primary)
    text((x + 5.5, 15), "chapter2", style=style_text_left)

def right():
    text((85, 54), "Output Documents", style=style_text_head)
    rectangle((85, 30), width=rect_width, height=rect_height, r=2, style=style_dashed)

    phosphor.file_pdf((85, 43), width=6, style=styles.primary)
    phosphor.file_html((85, 35), width=6, style=styles.primary)
    phosphor.file_ppt((85, 27), width=6, style=styles.primary)
    phosphor.book_bookmark((85, 19), width=6, style=styles.primary)
    text((85, 14.5), text="eBook", style=styles.primary.patch(text_size=13, text_halign="center"))

def bottom():
    rectangle((50, 5), width=90, height=6, r=2, style=styles.primary.patch(shape_fill_color=Colors.White, shape_line_color=Colors.Black))
    phosphor.github_logo((17, 5), width=5, style=styles.primary)
    text((53, 5), "Illustration and doc text versioning with CI/CD automation", style=styles.primary.patch(text_size=14, text_halign="center"))

left()
arrow(
    (28, 35),
    (37, 35),
    tail_width=3,
    head_width=6,
    head_length=3,
    style=styles.red_flat,
    text="Drawlib",
    textstyle=styles.primary.patch(text_size=13, text_color=Colors.White),
)
text((32, 25), "Build\nImages", style=styles.primary.patch(text_size=14, text_halign="center", text_color=Colors.Red))
center()
arrow(
    (63, 35),
    (72, 35),
    tail_width=3,
    head_width=6,
    head_length=3,
    style=styles.primary.patch(shape_fill_color=Colors.White, shape_line_color=Colors.Black),
)
text((67, 25), "Build\nDocs", style=styles.primary.patch(text_size=14, text_halign="center"))
right()
bottom()
```

As a real-world example, almost all of the documentation images are created using Drawlib. 
The build flow is similar to the image above. 
We compile documents via Drawlib Document Builder and publish them to the Internet or repository. 
These images are built by scripts locally for quick verification of the drawing results. 
To reduce human error and operation costs, we run CI/CD processes when code is committed to the GitHub repository.

Drawlib adopts the preset styles feature, similar to slide templates. 
When you change the preset styles, the default styles are automatically applied to all images. 
If you want to slightly change the style, modifying the style definitions will affect all images that reference it. 
This ensures consistent image styling with minimal effort.



# Because it is Python


Many readers of this document might already be familiar with Python. 
With Drawlib, you can leverage Python and its extensive ecosystem to enhance your illustration workflow. 
Some benefits include:

- Creating custom functions to group drawing actions
- Using loops for repeated drawing tasks
- Utilizing conditional branches (if statements) within your drawing code
- Receiving assistance from your IDE (I recommend VSCode with Python extensions)
- Getting familiar Python error messages when encountering issues in your code

You don't need to learn another programming language or domain-specific language (DSL) to achieve illustration as code. 
Here is an example of VSCode's help screenshot for the `circle()` function:


![image_vscode.png](image_vscode.png)


As you can see, VSCode provides detailed information about the function and offers auto-completion and other helpful features.

If you are familiar with Python, you should be able to understand how to use Drawlib with just a few hours of practice. 
The design of Drawlib is consistent and Pythonic, making it intuitive for Python developers.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
