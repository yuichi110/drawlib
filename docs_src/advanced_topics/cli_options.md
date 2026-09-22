=================

# CLI and Options



# drawlib Command


Once drawlib is installed, you gain access to the `drawlib` command. 
This command is equivalent to invoking the drawlib module using `python -m drawlib`.

You can develop your illustration code using either `python <your_drawlib_code>` or `drawlib <your_drawlib_code_or_directory>`. 
If you are working with a single file that doesn't import any other files, there is minimal difference between using these commands.

However, significant differences arise when managing multiple illustration codes or referencing style code:

- The python command executes a single file.
- The `drawlib` command performs several tasks before executing your code:

  - It detects your package architecture and registers paths.
  - It executes all Python files found under the specified directory.
  - It can automatically apply `clear()` before executing each file.


For projects involving numerous illustrations, we strongly recommend using the `drawlib` command over `python` for its added convenience and automation features.



# Sample


We will cover how to build multiple illustrations in detail in the foundational chapter. 
Please refer to that section for comprehensive guidance. 
However, as demonstrated here, the `drawlib` command is capable of building multiple Python illustration codes after registering your package path.


```text
$ drawlib docs/                
Detect package root "/Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs".
   - Add parent directory of package root "/Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many" to Python Path.

Execute python files
   - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/__init__.py
   - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/chap01/__init__.py
   - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/chap01/image1.py
   - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/chap01/image2.py
   - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/chap02/__init__.py
   - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/chap02/image1.py
   - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/commons/__init__.py
   - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/commons/style.py
   - /Users/yuichi/GitHub/drawlib_docs/v0_1/samples/build_many/docs/commons/util.py
```




# Command Options


The `drawlib` command includes the `-h` and `--help` options, which display command help.


```text
$ drawlib -h
 usage: drawlib [-h] [-v] [--purge_font_cache] [--disable_auto_clear] [--enable_auto_initialize] [--quiet] [--verbose] [--developer] ...

 Ilustration as code by python

 positional arguments:
 file_or_directory     Target python file or directory which contains python codes

 optional arguments:
 -h, --help            show this help message and exit
 -v, --version         Show version.
 --purge_font_cache    Purge cached font files.
 --disable_auto_clear  Disable clearing canvas per executing drawing code files.
 --enable_auto_initialize
                         Enable initializing canvas per executing drawing code files.
 --quiet               Enable quiet logging. show only error messages
 --verbose             Enable verbose logging.
 --debug               Enable verbose logging. Equivalent to option "--verbose".
 --developer           Enable verbose logging. Disable error handling for library users.
```



## Controlling Auto Clear and Initialize Feature


By default, auto `clear()` is enabled, meaning your previous drawing actions are erased before executing the next illustration code. 
This behavior is generally suitable for normal use cases.

However, if you intend to create a single illustration using multiple Python files, this auto clear feature may not be desirable. 
In such cases, you can disable it using `--disable_auto_clear`.

The `clear()` function erases canvas elements while maintaining consistent theme configurations. 
If you need to completely initialize drawlib per illustration code execution, you can use `--enable_auto_initialize`. 
This option ensures that drawlib calls `dutil_canvas.initialize()` every time your code files are executed.

Typically, you won't need to specify both options.



## Purging Font Cache


The `--purge_font_cache` option removes drawlib's cached font files from your local machine. 

Font files are downloaded and cached the first time you use a particular font, and this option deletes those cached files to reclaim disk space. 
The combined size of font files is usually under 100MB. 
Note that using Chinese or Japanese fonts may consume more space due to the large number of characters they include. 

Uninstalling drawlib also removes cached fonts, as drawlib stores font caches in its library directory.


## Setting Log Level


Options like `--quiet`, `--verbose`, `--debug`, and `--developer` adjust the log level:

- `--quiet`: Suppresses all output except errors.
- `--verbose` / `--debug`: Provides verbose logging and includes stack traces for errors.
- `--developer`: Provides verbose logging and offering detailed error dumps without error handling, suitable for advanced Python users troubleshooting issues.

Choose the appropriate log level based on your need for error visibility and troubleshooting depth.


## Generating Coordinate Grid Images with Batch (`--grid` / `-g`)

When building illustrations via `drawlib batch` (or direct `drawlib <files>` execution), you can specify the `-g` or `--grid` option:

```bash
drawlib batch my_drawing.py --grid
# Shorthand:
drawlib batch my_drawing.py -g

# Batch build an entire directory with grids:
drawlib batch docs/ --grid
```

When `--grid` is enabled, drawlib automatically generates a companion `{name}_grid.png` image with the coordinate grid overlaid alongside the normal `{name}.png` image for every executed script. This is especially helpful during drafting and layout alignment when managing multiple illustrations in a project.


# Interactive Preview with `drawlib show`

The `drawlib show` command provides an instant visual preview of your illustrations without manually opening saved image files. It supports both standalone Python scripts (`.py`) and embedded code blocks within Markdown files (`.md`).


## Previewing a Python Script

To preview an illustration defined in a Python script:

```bash
drawlib show my_drawing.py
```

### Displaying with Coordinate Grid (`--grid` / `-g`)

When designing illustrations, aligning elements precisely to coordinates is essential. You can overlay the coordinate grid onto the preview image using the `-g` or `--grid` option:

```bash
drawlib show my_drawing.py --grid
# Shorthand:
drawlib show my_drawing.py -g
```

This renders the drawing along with the canvas grid lines and center axes, making it straightforward to fine-tune shape coordinates and sizes.


## Previewing Markdown Code Blocks

You can also preview `drawlib` code blocks embedded in your Markdown documents.

### Listing Available Code Blocks

If you specify a Markdown file without a block index, `drawlib show` lists all code blocks found in the document:

```bash
drawlib show doc.md
```

Example output:
```text
Available drawlib code blocks in 'doc.md':
Index   Line    File Target                  Header Options
-----------------------------------------------------------------
1       L45     doc_images/1.png             -
2       L92     doc_images/diagram.png       caption:"Architecture"
```

### Previewing a Specific Block

Provide the block index (1-based) or target filename:

```bash
drawlib show doc.md 1
# Or by target name:
drawlib show doc.md diagram.png
```

### Previewing Markdown Blocks with Grid (`--grid` / `-g`)

Just like with Python scripts, add `-g` or `--grid` to overlay the coordinate grid:

```bash
drawlib show doc.md 1 --grid
# Shorthand:
drawlib show doc.md 1 -g
```

### Saving Directly to File (`-o` / `--output`)

If you want to save the previewed image directly to a designated file path instead of opening a GUI preview window, specify the `-o` or `--output` option:

```bash
drawlib show my_drawing.py -o output.png
drawlib show doc.md 1 -o preview.png
```

When `-o` / `--output` is specified, the GUI window is suppressed and the image is written directly to the target location.


# Exporting Single Illustrations with `drawlib export`

The `drawlib export` command extracts and renders a single illustration from either a standalone Python script or a Markdown document into an image file. It is specifically designed for:

- Automated workflows and CI/CD pipelines without GUI displays.
- Headless environments or AI agent interactions where inspecting a specific visual artifact is required.
- Quick extraction of a single diagram from a large Markdown document without running a full document build.

## Basic Syntax

```bash
drawlib export <file> [target] [-o <output_path>] [-c <config_path>] [-g]
```

- `<file>`: Path to a Python script (`.py`) or Markdown file (`.md`).
- `[target]`: Block index (1-based, e.g., `1`) or target image filename (e.g., `diagram.png`) when targeting a Markdown document. If omitted for a Markdown file, available blocks are listed.
- `-o`, `--output <path>`: Destination path for the exported image (defaults to `<input_stem>_export.png` if omitted).
- `-c`, `--config <path>`: Path to custom configuration script (such as `config.py`) that sets themes, styles, or canvas defaults.
- `-g`, `--grid`: Overlay coordinate grid lines and axes on the exported image.

## Listing Markdown Code Blocks

Running `drawlib export` with only a Markdown file lists all `drawlib` blocks without rendering:

```bash
drawlib export doc.md
```

## Exporting from Markdown Code Blocks

Export by block index (1-based):

```bash
drawlib export doc.md 1 -o doc_images/intro.png
```

Export by target image name:

```bash
drawlib export doc.md diagram.png -o doc_images/diagram.png
```

## Exporting from Standalone Python Scripts

```bash
drawlib export my_drawing.py -o output.png
```

## Applying Custom Configuration (`--config` / `-c`)

When your documentation relies on a global `config.py` (e.g., for custom color themes, fonts, or drawing options), supply it using `-c` or `--config`:

```bash
drawlib export doc.md 1 -c config.py -o rendered_1.png
```

This runs the code block within the exact shared execution context and configuration established by `config.py`, guaranteeing identical visual output to a full document build (`drawlib doc-builder`).

## Exporting with Coordinate Grid (`--grid` / `-g`)

Overlay coordinate axes and grid lines on the output image during drafting or layout adjustments:

```bash
drawlib export doc.md 1 --grid -o debug_grid.png
# Shorthand:
drawlib export doc.md 1 -g -o debug_grid.png
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>

