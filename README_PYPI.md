## About

Drawlib is a pure Python drawing library crafted to facilitate Illustration as Code rather than focusing solely on creating polished illustrations. 
Witness Python code in action generating a circular image:

![Example](https://www.drawlib.com/pypi_images/image1.png)

In this example, we import drawlib APIs and call the `circle()` function. 
We provide XY coordinates, radius, and optional style with `ShapeStyle` class.

Defining styles directly within the drawing object is straightforward, similar to writing styles within HTML tags. 
However, just as HTML recommends using a separate CSS file, Drawlib recommends creating a separate styling code file and referencing it in multiple illustration codes. 
Following this guide simplifies the above code.

## Documentation

We have official documentation. 
Please check it out if you're interested in Drawlib.

[Drawlib Official Documentation](https://www.drawlib.com/docs/)

## API Design

Drawlib offers a range of basic drawing features, including:

- Icon
- Image
- Line
- Shape
- Text
- Others

All with a consistent syntax.

Here is a brief overview of the library's API design.

![Example](https://www.drawlib.com/pypi_images/image2.png)

As you can see, the core drawing components rely on the same canvas and coordinate systems. 
Styling for each component is slightly different but mostly similar. 
If you require advanced use cases, many helper classes and functions can resolve the situation.

## Good IDE Help and Python Ecosystem

It's important to note that drawlib is a pure Python library. This means you can leverage the entire Python ecosystem, including:

- Accessing library help and code completion via IDEs.
- Using programming constructs such as creating functions for grouping drawing tasks and using loops.

Here is a screenshot of my VS Code providing help for the `ShapeStyle` class when I point to it. 
All other functions and classes are also well-documented, offering comprehensive help and intelligent code completion.

![Example](https://www.drawlib.com/pypi_images/image3.png)

## Good for Documentations and Books

In today's world, many technical documents are managed using version control systems such as Git. 
However, managing illustrations poses a challenge as they are typically binary files rather than text-based. 
Drawlib offers a solution by generating illustrations from pure Python code. 
This means that if you create your illustrations using Python and drawlib, you can manage them using version control systems too.

Drawlib is optimized for drawing a large number of illustrations with a consistent style. 
You can easily achieve this by creating a style code and importing it into your illustration codes. 
Here is a typical use case of drawlib.

![Use Case](https://www.drawlib.com/pypi_images/image4.png)

Integrating Drawlib into your workflow is straightforward and doesn’t significantly differ from managing markdown documents. 
If you create your documentation using markdown or a similar format, you can easily adopt drawlib.

## Links

- [Documentation](https://www.drawlib.com/docs/)
- [PyPI](https://pypi.org/project/drawlib/)
- [Code repository](https://github.com/yuichi110/drawlib)
- [Docs repository](https://github.com/yuichi110/drawlib_docs)
- [Assets repository](https://github.com/yuichi110/drawlib_assets)
