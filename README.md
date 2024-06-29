## About

Drawlib is a Python drawing library designed to achieve *Illustration as Code*.

![Example](https://www.drawlib.com/readme_images/image1.png)

In this example, we import drawlib APIs and call the `circle()` function. We provide XY coordinates, radius, and optional style. If a style is not provided, the default style (which you can manage) is applied.

Drawlib offers a range of basic drawing features, including:

- Icon
- Image
- Line and Arrow-line
- Shape
- Text
- Others

All with a consistent syntax.

Here is a brief overview of the library's API design.

![Example](https://www.drawlib.com/readme_images/image2.png)

As you can see, the core drawing components rely on the same canvas and coordinate systems. 
Styling for each component is slightly different but mostly similar. 
If you require advanced use cases, many helper classes and functions can resolve the situation.

It's important to note that drawlib is a pure Python library. This means you can leverage the entire Python ecosystem, including:

- Accessing library help and code completion via IDEs.
- Using programming constructs such as creating functions for grouping drawing tasks and using loops.

## Why Illustration as Code

In today's world, many technical documents are managed using version control systems such as Git. 
However, managing illustrations poses a challenge as they are typically binary files rather than text-based. 
Drawlib offers a solution by generating illustrations from pure Python code. 
This means that if you create your illustrations using Python and drawlib, you can manage them using version control systems too.

Drawlib is optimized for drawing a large number of illustrations with a consistent style. 
You can easily achieve this by creating a theme file (which is simply Python code) and importing it into your illustration codes (also Python code). 
Here is a typical use case of drawlib.

![Use Case](https://www.drawlib.com/readme_images/image3.png)

We have provided examples of building Sphinx-based documentation with numerous drawlib images. If you're interested, please check out our documentation.

## Links

- [Documentation](https://www.drawlib.com/docs/)
- [PyPI](https://pypi.org/project/drawlib/)
- [Code repository](https://github.com/yuichi110/drawlib)
- [Docs repository](https://github.com/yuichi110/drawlib_docs)
- [Assets repository](https://github.com/yuichi110/drawlib_assets)
