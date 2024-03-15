from drawlib import *


def test_circle():
    config(width=10, height=10, axis=False)
    Circle(5, 5, 3)
    save("test_circle.png")
