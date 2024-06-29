# About Drawlib

Drawlib is a pure Python drawing library crafted to facilitate Illustration as Code rather than focusing solely on creating polished illustrations. Witness Python code in action generating a circular image:

As you can see, we define circle location, size and styles at left side code. Executing it generate right side circle image. You will get illustration as you code.

## Official Documentation

Complete documentation is provided at our official documentation.


## Concept: Apply Style to Content

The parameters of a circle include coordinates, size, color, etc. Many drawing tools treat these parameters uniformly. However, we divide them into two parts:

Content: The type of drawing items, such as coordinates, size, angle, etc.
Style: Elements like color, line width, and font.
If you are familiar with HTML/CSS, content is analogous to HTML, and style is analogous to CSS. Just as it’s recommended to define styles in CSS and reference them in HTML, Drawlib encourages defining styles separately and referencing them in the illustration code.

From an artistic perspective, the mix of content and style is essential. However, for illustrations that do not require an artistic look, the content is more critical than the styles. The color or width of a line is less important than where the line is drawn.

Separating content and style allows you to focus on the essential content first. Once the content is created, you can modify its appearance by changing styles outside of the content. Additionally, you can apply one style to many content items if they are separated. Using the same style for many items is crucial for achieving consistency in illustrations.

## Good for Documentations and Books

In contemporary software development, version control extends beyond code to encompass documentation, all managed seamlessly through Git. While I compose technical documents and literature using VSCode and Markdown, I previously relied on PowerPoint for illustrations. However, this approach lacks compatibility with versioning documentation images.

Enter Drawlib, a solution meticulously developed to address this issue. With Drawlib, not only can textual documentation be version-controlled, but illustration code can also be managed through Git. This facilitates the automation of build tasks via scripting or CI/CD pipelines.

Integrating Drawlib into your workflow is straightforward and doesn’t significantly differ from managing markdown documents. If you create your documentation using markdown or a similar format, you can easily adopt drawlib.


# Installation

You can install drawlib with the following command. If your system uses python3 and pip3, use them instead.

```bash
$ pip install drawlib
```

After installation, you can check whether Drawlib was installed successfully with these commands:

```bash
$ python -m drawlib --version
software=0.1.24
api=0.1.24

$ drawlib --version
software=0.1.24
api=0.1.24
```

The Drawlib package also installs the drawlib command, which is useful for building many images. This command calls the Drawlib libraries’ script, equivalent to python -m drawlib. For more details, refer to the relevant section in the foundation chapter.


# Quick Start

## Standard Procedure for Drawing with Drawlib

Below is the standard procedure for drawing using Drawlib:

