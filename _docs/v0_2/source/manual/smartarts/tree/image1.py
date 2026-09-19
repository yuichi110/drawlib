from drawlib.apis import *

config(width=100, height=50, grid=True)

tree1 = dsart.TreeNode(
    "Root",
    default_textstyle="",
    default_linestyle="light",
    default_line_horizontal_margin=2,
    default_line_horizontal_length=2,
    default_line_vertical_margin=5,
    children=[
        dsart.TreeNode(
            "Child1",
            children=[
                dsart.TreeNode(
                    "Child1-1",
                    children=[
                        dsart.TreeNode("Child1-1-1"),
                    ],
                ),
                dsart.TreeNode("Child1-2", textstyle="red"),
            ],
        ),
        dsart.TreeNode(
            text="Child2",
            default_textstyle="blue",
            children=[
                dsart.TreeNode("Child2-1"),
                dsart.TreeNode("Child2-2"),
            ],
        ),
    ],
)
tree1.draw((10, 42.5))


dsart.TreeNode.register_drawing_item(
    name="py_file",
    location="before",
    padding_width=5,
    function=icon_phosphor.file_py,
    style=dtheme.iconstyles.get(),
    args={"width": 4},
)
dsart.TreeNode.register_drawing_item(
    name="png_file",
    location="before",
    padding_width=5,
    function=icon_phosphor.file_png,
    style=dtheme.iconstyles.get("red"),
    args={"width": 4},
)

tree2 = dsart.TreeNode(
    "Root",
    default_textstyle="",
    default_linestyle="light",
    default_line_horizontal_margin=2,
    default_line_horizontal_length=2,
    default_line_vertical_margin=5,
    children=[
        dsart.TreeNode(
            "Child1",
            children=[
                dsart.TreeNode(
                    "Child1-1",
                ).set_drawing_item("py_file"),
                dsart.TreeNode("Child1-2").set_drawing_item("png_file"),
            ],
        ),
        dsart.TreeNode(
            "Child2",
            children=[
                dsart.TreeNode("Child2-1").set_drawing_item("py_file"),
                dsart.TreeNode("Child2-2").set_drawing_item("png_file"),
            ],
        ),
    ],
)

tree2.draw((60, 42.5))
save()
