# drawlib.tools

`drawlib.tools` exposes the lazy-loaded programmatic Python developer API powering the [`drawlib` CLI](28_cli.md). Use its 28 functions to embed multi-locale HTML, Markdown, PDF, MS Word (`.docx`), HTML Slide, and MS PowerPoint (`.pptx`) compilation, single-block diagram export, project/agent scaffolding, broken-link scanning, CSS preset synthesis, and asset cache management directly into Python automation scripts, CI/CD pipelines, and `pytest` suites.

```drawlib align=center code=fold file=27_tools_hero.png caption="Programmatic Build, Export, Scaffolding, and Link Verification Pipeline in drawlib.tools"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import BoxList, ChevronProcess
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=134, height=62)

rectangle(
    (67, 31),
    width=124,
    height=52,
    style=Styles.Neutral.patch(shape_fill_color=Colors.Transparent, line_style="dashed", shape_r=2.5),
)
text(
    (67, 53.0),
    "drawlib.tools · Programmatic Automation & Build Pipeline (28 Functions)",
    style=Styles.DarkBold.patch(text_size=11.5),
)

stage_icons = [
    (22.5, phosphor.folder_open, Styles.PrimaryBold),
    (51.5, phosphor.gear_six, Styles.PrimaryBold),
    (80.5, phosphor.magnifying_glass, Styles.PrimaryBold),
    (109.5, phosphor.check_circle, Styles.SecondaryBold),
]
for ix, icon_fn, ist in stage_icons:
    icon_fn((ix, 46.2), width=4.4, style=ist)

pipeline = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Dark.patch(text_size=10.0),
    corner_angle=60.0,
    spacing=1.8,
    flat_left_end=True,
)
pipeline.add("1. Scaffold", description="init_project()")
pipeline.add(
    "2. Compile",
    description="build_html / pdf()",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
    description_style=Styles.White.patch(text_size=10.0),
)
pipeline.add("3. Inspect", description="export_code_block()", style=Styles.PrimaryNeutral)
pipeline.add("4. Verify", description="scan_broken_links()", style=Styles.SecondaryNeutral)
pipeline.draw(xy=(10.0, 26.0), width=114.0, height=16.5)

domains = BoxList(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
domains.add("HTML / API\nbuild_html()")
domains.add("PDF & Word\nbuild_pdf / docx()")
domains.add("Slide & PPTX\nbuild_slide / pptx()")
domains.add("Agent Rules\ninit_agent_*()")
domains.add("Cache & CSS\ndownload / get_css()", style=Styles.SecondaryNeutral)
domains.draw(xy=(10.0, 8.5), box_width=22.8, box_height=13.0, direction="left")

save()
```

## `def` build_document(input_dir, output_path=None, output_format=None, *, ...)

Unified dispatcher that compiles a documentation directory into HTML, PDF, MS Word (`.docx`), or GitHub-Flavored Markdown based on `output_format` or the file extension of `output_path`.

```python
from drawlib.tools import build_document

build_document(
    input_dir: str,
    output_path: str | None = None,
    output_format: str | None = None,
    *,
    image_format: str = "png",
    css_mode: str = "external",
    styles_path: str | None = None,
    utils_path: str | None = None,
    no_cache: bool = False,
    timestamp: bool = False,
) -> str
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `input_dir` | `str` | *(required)* | Source documentation project directory. |
| `output_path` | `str \| None` | `None` | Destination directory or output file path (`.pdf`, `.docx`, `.md` auto-infer `output_format`). |
| `output_format` | `str \| None` | `None` | Target format (`"html"`, `"pdf"`, `"docx"`, or `"markdown"`; defaults to `"html"`). |
| `image_format` | `str` | `"png"` | Embedded diagram image format (`"png"` or `"webp"`). |
| `css_mode` | `str` | `"external"` | HTML stylesheet linking mode (`"external"` or `"embed"`). |
| `styles_path` | `str \| None` | `None` | Optional path to a custom `styles.py` file. |
| `utils_path` | `str \| None` | `None` | Optional path to a custom `utils.py` file. |
| `no_cache` | `bool` | `False` | Bypass the SQLite image build cache when `True`. |
| `timestamp` | `bool` | `False` | Include current build timestamp in PDF or Word metadata when `True`. |

- **Returns (`str`)**: Absolute path of the generated output directory or file.

## `def` build_docx(input_path=None, output_file=None, *, ...)

Compile a linear `doc` project directory (emitting `<base>_<lang>.docx` per configured locale) or a standalone Markdown file (`.md`) into a native editable Microsoft Word (`.docx`) document via `python-docx`.

```python
from drawlib.tools import build_docx

build_docx(
    input_path: str | None = None,
    output_file: str | None = None,
    *,
    input_dir: str | None = None,
    title: str | None = None,
    page_break: bool = True,
    generate_index: bool = False,
    dpi: int = 200,
    styles_path: str | None = None,
    utils_path: str | None = None,
    no_cache: bool = False,
    timestamp: bool = False,
) -> str
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `input_path` | `str \| None` | `None` | `doc` project directory (`drawlib.toml`) or standalone `.md` file path. |
| `output_file` | `str \| None` | `None` | Destination `.docx` file path (or base path/directory for multi-locale `doc` projects). |
| `input_dir` | `str \| None` | `None` | Keyword alias for `input_path`. |
| `title` | `str \| None` | `None` | Document title override. |
| `page_break` | `bool` | `True` | Insert Word page breaks between merged chapters. |
| `generate_index` | `bool` | `False` | Generate a localized Table of Contents between the 1st and 2nd chapters. |
| `dpi` | `int` | `200` | Rasterization DPI for embedded `drawlib` static PNG diagrams. |
| `styles_path` | `str \| None` | `None` | Optional path to a custom `styles.py` script. |
| `utils_path` | `str \| None` | `None` | Optional path to a custom `utils.py` script. |
| `no_cache` | `bool` | `False` | Disable reading and writing the `.drawlib/cache.db` SQLite image cache. |
| `timestamp` | `bool` | `False` | Include current build timestamp in `.docx` metadata instead of deterministic normalization. |

- **Returns (`str`)**: Absolute path to the generated `.docx` file (or `default_lang` `.docx` for `doc` projects).

## `def` build_html(input_dir, output_dir=None, *, ...)

Compile an `i18n`-native `site`, `doc`, or `catalog` project directory (`drawlib.toml` + `<lang>/` sources) into static HTML with shared diagram deduplication, per-locale stylesheets, language switcher navigation (when 2+ locales are configured), and a root `index.html`.

```python
from drawlib.tools import build_html

build_html(
    input_dir: str,
    output_dir: str | None = None,
    *,
    image_format: str = "png",
    styles_path: str | None = None,
    utils_path: str | None = None,
    no_cache: bool = False,
    css_mode: str = "external",
) -> str
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `input_dir` | `str` | *(required)* | Project root directory containing `drawlib.toml` (`type = "site"`, `"doc"`, or `"catalog"`) and `<lang>/` folders. |
| `output_dir` | `str \| None` | `None` | Target HTML output directory (defaults to `<base>_html`). |
| `image_format` | `str` | `"png"` | Image output format for embedded `drawlib` blocks (`"png"` or `"webp"`). |
| `styles_path` | `str \| None` | `None` | Optional path to a custom `styles.py` script. |
| `utils_path` | `str \| None` | `None` | Optional path to a custom `utils.py` script. |
| `no_cache` | `bool` | `False` | Disable reading and writing the SQLite build image cache. |
| `css_mode` | `str` | `"external"` | CSS linking mode (`"external"` or `"embed"`). |

- **Returns (`str`)**: Absolute path of the generated HTML output directory.

## `def` build_image(input_path, output_path=None, *, ...)

Execute one or more standalone Python drawing scripts (`.py`), script directories, or project Markdown directories in batch mode to render image assets, performing static AST collision checks prior to execution.

```python
from drawlib.tools import build_image

build_image(
    input_path: str | Sequence[str],
    output_path: str | None = None,
    *,
    format: Literal["png", "webp", "gif", "jpg", "pdf"] | None = None,
    styles_path: str | None = None,
    utils_path: str | None = None,
    grid: bool = False,
    disable_auto_clear: bool = False,
    enable_auto_initialize: bool = False,
    no_cache: bool = False,
) -> list[str]
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `input_path` | `str \| Sequence[str]` | *(required)* | Target Python script(s), Markdown file(s), or directory path(s). |
| `output_path` | `str \| None` | `None` | Output image file path (for a single script) or destination directory path. |
| `format` | `Literal["png", "webp", "gif", "jpg", "pdf"] \| None` | `None` | Global output image format override (`None` preserves script `save()` setting). |
| `styles_path` | `str \| None` | `None` | Optional path to a custom `styles.py` script. |
| `utils_path` | `str \| None` | `None` | Optional path to a custom `utils.py` script. |
| `grid` | `bool` | `False` | Also save companion `*_grid.<ext>` images with the coordinate grid overlaid. |
| `disable_auto_clear` | `bool` | `False` | Skip automatic canvas artist clearing between consecutive files. |
| `enable_auto_initialize` | `bool` | `False` | Perform full canvas re-initialization before each executed file. |
| `no_cache` | `bool` | `False` | Bypass the SQLite build image cache. |

- **Returns (`list[str]`)**: List of executed target file paths.

## `def` build_markdown(input_dir, output_dir=None, *, ...)

Compile an `i18n`-native `site`, `doc`, or `catalog` project directory into GitHub-Flavored Markdown (`<output_dir>/<lang>/` + shared `<output_dir>/images/`), refusing in-place source overwrites.

```python
from drawlib.tools import build_markdown

build_markdown(
    input_dir: str,
    output_dir: str | None = None,
    *,
    image_format: str = "png",
    styles_path: str | None = None,
    utils_path: str | None = None,
    no_cache: bool = False,
) -> str
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `input_dir` | `str` | *(required)* | Project root directory containing `drawlib.toml` and `<lang>/` Markdown sources. |
| `output_dir` | `str \| None` | `None` | Target Markdown output directory (defaults to `<base>_markdown`). |
| `image_format` | `str` | `"png"` | Image output format (`"png"` or `"webp"`). |
| `styles_path` | `str \| None` | `None` | Optional path to a custom `styles.py` script. |
| `utils_path` | `str \| None` | `None` | Optional path to a custom `utils.py` script. |
| `no_cache` | `bool` | `False` | Bypass the SQLite build image cache. |

- **Returns (`str`)**: Absolute path of the generated Markdown output directory.

## `def` build_pdf(input_path=None, output_file=None, *, ...)

Compile a `doc` project directory, `slide` project directory, or standalone Markdown/HTML file into print-ready vector PDF(s) via headless Chromium (`playwright`). Project directory builds emit `<base>_<lang>.pdf` for every configured locale.

```python
from drawlib.tools import build_pdf

build_pdf(
    input_path: str | None = None,
    output_file: str | None = None,
    *,
    input_dir: str | None = None,
    title: str | None = None,
    page_break: bool = True,
    generate_index: bool = False,
    styles_path: str | None = None,
    utils_path: str | None = None,
    no_cache: bool = False,
    timestamp: bool = False,
) -> str
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `input_path` | `str \| None` | `None` | `doc` or `slide` project directory, or standalone `.md`/`.html` file path. |
| `output_file` | `str \| None` | `None` | Destination PDF file path (or base path/directory for multi-locale project builds). |
| `input_dir` | `str \| None` | `None` | Keyword alias for `input_path`. |
| `title` | `str \| None` | `None` | Document or presentation title override. |
| `page_break` | `bool` | `True` | Insert CSS page breaks between merged `doc` chapters. |
| `generate_index` | `bool` | `False` | Insert a localized Table of Contents between the 1st and 2nd `doc` chapters. |
| `styles_path` | `str \| None` | `None` | Optional path to a custom `styles.py` script. |
| `utils_path` | `str \| None` | `None` | Optional path to a custom `utils.py` script. |
| `no_cache` | `bool` | `False` | Bypass the SQLite build image cache. |
| `timestamp` | `bool` | `False` | Include current build timestamp in PDF metadata instead of deterministic normalization. |

- **Returns (`str`)**: Absolute path of the generated PDF file (or `default_lang` PDF for project directories).

## `def` build_pptx(input_dir, output_file=None, *, ...)

Compile an `i18n`-native Markdown `slide` project directory into native editable 16:9 (`960×540 pt`) Microsoft PowerPoint (`<stem>_<lang>.pptx`) decks (re-exported from [`drawlib.slide`](26_anim_and_slide.md)).

```python
from drawlib.tools import build_pptx

build_pptx(
    input_dir: str,
    output_file: str | None = None,
    *,
    title: str | None = None,
    theme: str | None = None,
    dpi: int = 240,
    anim_frame: Literal["first", "last"] = "last",
    styles_path: str | None = None,
    utils_path: str | None = None,
    no_cache: bool = False,
    timestamp: bool = False,
) -> str
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `input_dir` | `str` | *(required)* | Slide project root directory containing `drawlib.toml` and `<lang>/` slide files. |
| `output_file` | `str \| None` | `None` | Optional destination `.pptx` base path or directory (`<stem>_<lang>.pptx`). |
| `title` | `str \| None` | `None` | Presentation title override in `.pptx` metadata. |
| `theme` | `str \| None` | `None` | CSS theme preset override (`"google"`, `"default"`, `"google-dark"`, `"default-dark"`). |
| `dpi` | `int` | `240` | Rasterization DPI for embedded static PNG diagrams (`> 0`). |
| `anim_frame` | `Literal["first", "last"]` | `"last"` | Frame extracted from animated blocks (`"first"` or `"last"`). |
| `styles_path` | `str \| None` | `None` | Optional path to a custom `styles.py` script. |
| `utils_path` | `str \| None` | `None` | Optional path to a custom `utils.py` script. |
| `no_cache` | `bool` | `False` | Disable reading and writing the SQLite build image cache. |
| `timestamp` | `bool` | `False` | Write current build timestamp into OpenXML metadata. |

- **Returns (`str`)**: Absolute path to the generated `<stem>_<default_lang>.pptx` file.

## `def` build_slide(input_dir, output_dir=None, *, ...)

Compile an `i18n`-native presentation project directory into a standalone multi-locale 16:9 HTML slide deck (re-exported from [`drawlib.slide`](26_anim_and_slide.md)).

```python
from drawlib.tools import build_slide

build_slide(
    input_dir: str,
    output_dir: str | None = None,
    *,
    title: str | None = None,
    theme: str | None = None,
    image_format: str = "svg",
    dpi: int | None = None,
    force_image_format: bool = False,
    static_anim_frame: Literal["first", "last"] | None = None,
    styles_path: str | None = None,
    utils_path: str | None = None,
    no_cache: bool = False,
) -> str
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `input_dir` | `str` | *(required)* | Slide project root directory containing `drawlib.toml` and `<lang>/` slides. |
| `output_dir` | `str \| None` | `None` | Target output directory (defaults to `<base>_html`). |
| `title` | `str \| None` | `None` | Optional HTML presentation `<title>` override. |
| `theme` | `str \| None` | `None` | CSS theme preset override. |
| `image_format` | `str` | `"svg"` | Default embedded diagram format (`"svg"`, `"webp"`, or `"png"`). |
| `dpi` | `int \| None` | `None` | Optional rasterization DPI override for raster diagrams. |
| `force_image_format` | `bool` | `False` | Rewrite explicit diagram extensions to `image_format` when `True`. |
| `static_anim_frame` | `Literal["first", "last"] \| None` | `None` | Flatten multi-frame animations into static PNGs using `"first"` or `"last"` frame. |
| `styles_path` | `str \| None` | `None` | Optional path to a custom `styles.py` script. |
| `utils_path` | `str \| None` | `None` | Optional path to a custom `utils.py` script. |
| `no_cache` | `bool` | `False` | Bypass the SQLite build cache. |

- **Returns (`str`)**: Absolute path to `<output_dir>/<default_lang>/index.html`.

## `def` clear_cache()

Delete all locally cached font, icon, and GeoJSON map asset archives downloaded from GitHub Releases.

```python
from drawlib.tools import clear_cache

clear_cache() -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| *(none)* | — | — | Takes no parameters and returns `None`. |

## `def` detect_agent_targets(destination=".")

Inspect a workspace root directory for existing AI coding agent configuration directories or instruction files (`.agents/`, `.agent/`, `.claude/`, `.cursor/`, `.github/instructions/`, `.windsurf/`, `.clinerules/`, `.roo/`, `AGENTS.md`, `GEMINI.md`) and return their canonical agent names.

```python
from drawlib.tools import detect_agent_targets

detect_agent_targets(
    destination: str | Path = ".",
) -> list[str]
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `destination` | `str \| Path` | `"."` | Workspace root directory path to inspect. |

- **Returns (`list[str]`)**: Canonical names of detected AI coding agents in deterministic order (e.g., `["antigravity", "claude"]`).

## `def` detect_document_type(file_path, content=None)

Classify a Markdown (`.md`, `.markdown`) or HTML (`.html`, `.htm`) file into one of four canonical document types (`"markdown_drawlib"`, `"markdown"`, `"html_drawlib"`, or `"html"`).

```python
from drawlib.tools import detect_document_type

detect_document_type(
    file_path: str,
    content: str | None = None,
) -> DocumentInputInfo
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `file_path` | `str` | *(required)* | Path to the input `.md`, `.markdown`, `.html`, or `.htm` file. |
| `content` | `str \| None` | `None` | Optional pre-loaded file text (`None` reads `file_path` from disk). |

- **Returns (`DocumentInputInfo`)**: Frozen Pydantic model with fields `path`, `doc_type`, `has_drawlib`, `is_markdown`, `is_html`, `is_full_html`, and `block_count`.

## `def` download_cache(all_assets=True, fonts=False, icons=False, maps=False, browser=False)

Pre-download font, icon, GeoJSON map packages, and/or headless Chromium (`chromium-headless-shell`) into the local cache for offline, Docker, or CI/CD environments.

```python
from drawlib.tools import download_cache

download_cache(
    all_assets: bool = True,
    fonts: bool = False,
    icons: bool = False,
    maps: bool = False,
    browser: bool = False,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `all_assets` | `bool` | `True` | Download all font, icon, map, and browser assets when no narrower flag is selected. |
| `fonts` | `bool` | `False` | Download font packages only. |
| `icons` | `bool` | `False` | Download icon packages only. |
| `maps` | `bool` | `False` | Download GeoJSON map packages only. |
| `browser` | `bool` | `False` | Download headless Chromium (`chromium-headless-shell`) via Playwright only. |

## `def` export_code_block(file_path=None, target=None, output_path=None, ...)

Headlessly execute a single `drawlib` block from a Markdown/HTML file (matched by filename `file=...` or 1-based block index) or execute a standalone `.py` script and save the rendered image to disk without opening a GUI window.

```python
from drawlib.tools import export_code_block

export_code_block(
    file_path: str | None = None,
    target: str | None = None,
    output_path: str | None = None,
    styles_path: str | None = None,
    utils_path: str | None = None,
    grid: bool = False,
    no_cache: bool = False,
) -> str
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `file_path` | `str \| None` | `None` | Path to the Markdown (`.md`), HTML (`.html`), or Python (`.py`) file. |
| `target` | `str \| None` | `None` | Block image filename (e.g., `"arch.png"`) or 1-based index (`"1"`). If omitted on `.md`/`.html`, prints all detected blocks and returns `""`. |
| `output_path` | `str \| None` | `None` | Destination image file or directory path. |
| `styles_path` | `str \| None` | `None` | Optional path to a custom `styles.py` script. |
| `utils_path` | `str \| None` | `None` | Optional path to a custom `utils.py` script. |
| `grid` | `bool` | `False` | Overlay the 10/5-unit coordinate inspection grid on the exported image. |
| `no_cache` | `bool` | `False` | Bypass reading and writing the SQLite build image cache. |

- **Returns (`str`)**: Absolute path of the exported image file (or `""` when listing blocks).

## `def` export_css(name, output_path=None, target="html", force=False, lang="en")

Synthesize and write a built-in CSS theme preset to a file on disk.

```python
from drawlib.tools import export_css

export_css(
    name: str,
    output_path: str | None = None,
    target: CssTarget = "html",
    force: bool = False,
    lang: str = "en",
) -> str
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | *(required)* | Built-in CSS preset name (`"default"`, `"google"`, `"default-dark"`, `"monochrome"`, etc.). |
| `output_path` | `str \| None` | `None` | Destination CSS path (defaults to `docs_src/style.css` if present, else `style.css`). |
| `target` | `CssTarget` | `"html"` | Target layout format (`"html"`, `"pdf"`, `"slide"`, `"site"`, `"doc"`, or `"catalog"`). |
| `force` | `bool` | `False` | Overwrite `output_path` if it already exists (`FileExistsError` when `False`). |
| `lang` | `str` | `"en"` | Language code for localized web font stacks (`"en"`, `"ja"`, `"zh-cn"`, etc.). |

- **Returns (`str`)**: Absolute path of the written CSS file.

## `def` get_agent_instruction(agent, mode="auto", global_scope=False)

Render the complete Drawlib instruction Markdown/MDC text (including any tool-specific YAML frontmatter) in memory for a target AI coding agent.

```python
from drawlib.tools import get_agent_instruction

get_agent_instruction(
    agent: str,
    mode: AgentTriggerMode = "auto",
    global_scope: bool = False,
) -> str
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `agent` | `str` | *(required)* | Target agent name or alias (`"antigravity"`, `"claude"`, `"cursor"`, `"copilot"`, `"windsurf"`, `"cline"`, `"roo"`, `"codex"`, `"gemini"`). |
| `mode` | `AgentTriggerMode` | `"auto"` | Frontmatter activation mode (`"auto"` on-demand or `"always"` always-on). |
| `global_scope` | `bool` | `False` | Format frontmatter/content for user-home global configuration when `True`. |

- **Returns (`str`)**: Complete formatted instruction string.

## `def` get_css(name=None, target="html", lang="en")

Synthesize and return a complete standalone CSS stylesheet string combining theme tokens, UI components, and target layout rules.

```python
from drawlib.tools import get_css

get_css(
    name: str | None = None,
    target: CssTarget = "html",
    lang: str = "en",
) -> str
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str \| None` | `None` | Built-in preset name or custom CSS path (defaults to `"default"`). |
| `target` | `CssTarget` | `"html"` | Target layout format (`"html"`, `"site"`, `"doc"`, `"pdf"`, `"slide"`, or `"catalog"`). |
| `lang` | `str` | `"en"` | Language code or alias for typography font stack substitution. |

- **Returns (`str`)**: Synthesized CSS stylesheet text.

## `def` init_agent_instruction(agent, destination=".", mode="auto", ...)

Write per-agent Drawlib instruction files into modular rule directories (`.agents/rules/`, `.claude/rules/`, `.cursor/rules/`, `.github/instructions/`, `.windsurf/rules/`, `.clinerules/`, `.roo/rules/`) or non-destructively merge marker-delimited sections into shared `AGENTS.md` / `GEMINI.md` files.

```python
from drawlib.tools import init_agent_instruction

init_agent_instruction(
    agent: str | Sequence[str],
    destination: str | Path = ".",
    mode: AgentTriggerMode = "auto",
    global_scope: bool = False,
    output_path: str | Path | None = None,
    force: bool = False,
) -> list[Path]
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `agent` | `str \| Sequence[str]` | *(required)* | Single agent name, comma-separated names, sequence of names, or `"all"`. |
| `destination` | `str \| Path` | `"."` | Workspace root directory for project-scoped rule files. |
| `mode` | `AgentTriggerMode` | `"auto"` | Trigger mode for frontmatter-capable agents (`"auto"` or `"always"`). |
| `global_scope` | `bool` | `False` | Write to the user's home global agent configuration path when `True`. |
| `output_path` | `str \| Path \| None` | `None` | Explicit destination file override (supported only when targeting a single agent). |
| `force` | `bool` | `False` | Overwrite existing dedicated files or update existing marker blocks when `True`. |

- **Returns (`list[Path]`)**: Resolved `Path` objects of created or updated instruction files.

## `def` init_project(project_type, destination=".", target=None, ...)

Scaffold a starter Drawlib project (`<target>_src/`) pre-configured with `drawlib.toml`, `styles.py`, `utils.py`, `_assets/`, stylesheets/templates, and executable `build*.sh` scripts.

```python
from drawlib.tools import init_project

init_project(
    project_type: str,
    destination: str | Path = ".",
    target: str | None = None,
    output: str | None = None,
    force: bool = False,
    lang: str = "en",
    style: str | None = None,
    here: bool = False,
) -> list[Path]
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `project_type` | `str` | *(required)* | Archetype name: `"doc"`, `"site"`, `"catalog"`, `"slide"`, `"images"`, or `"image"`. |
| `destination` | `str \| Path` | `"."` | Parent directory in which `<target>_src/` is created. |
| `target` | `str \| None` | `None` | Custom base name (defaults to `"doc"`, `"docs"`, `"catalog"`, `"slide"`, or `"images"`). |
| `output` | `str \| None` | `None` | Legacy alias for `target`. |
| `force` | `bool` | `False` | Overwrite conflicting files in the destination directory when `True`. |
| `lang` | `str` | `"en"` | Locale code (`"en"`, `"ja"`) or comma-separated codes (`"en,ja"`) for multi-locale `doc`/`site`/`catalog`/`slide`. |
| `style` | `str \| None` | `None` | Theme preset (`"default"`, `"google"`, `"monochrome"`, etc.) or custom CSS file path. |
| `here` | `bool` | `False` | Deprecated legacy flag (ignored; `<target>_src/` is always created). |

- **Returns (`list[Path]`)**: List of scaffolded `Path` objects.

## `def` list_agent_targets()

Return metadata dictionaries describing all supported AI coding agent instruction targets.

```python
from drawlib.tools import list_agent_targets

list_agent_targets() -> list[dict[str, str]]
```

| Return Dict Key | Type | Description |
| :--- | :--- | :--- |
| `name` | `str` | Canonical target identifier (e.g., `"antigravity"`, `"claude"`, `"cursor"`). |
| `label` | `str` | Human-readable tool name. |
| `project_path` | `str` | Default workspace-relative rule file path. |
| `global_path` | `str` | Default user-home global configuration file path. |
| `format` | `str` | Output file format / frontmatter convention. |
| `description` | `str` | Summary of how the agent loads the instruction file. |

## `def` list_cache()

Inspect all downloadable font, icon, and GeoJSON map asset packages alongside their local cache status and disk usage.

```python
from drawlib.tools import list_cache

list_cache() -> list[dict[str, Any]]
```

| Return Dict Key | Type | Description |
| :--- | :--- | :--- |
| `name` | `str` | Asset package identifier (e.g., `"icon_phosphor"`, `"font_japanese"`). |
| `category` | `str` | Asset category (`"font"`, `"icon"`, or `"map"`). |
| `cached` | `bool` | `True` when extracted and present in the local Drawlib cache directory. |
| `file_count` | `int` | Number of cached files in the package (`0` if not cached). |
| `size_bytes` | `int` | Total disk size in bytes occupied by the cached package. |

## `def` list_css(target="html")

Return metadata dictionaries for all built-in CSS theme presets available for `target`.

```python
from drawlib.tools import list_css

list_css(
    target: CssTarget = "html",
) -> list[dict[str, str]]
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `target` | `CssTarget` | `"html"` | Target layout format (`"html"`, `"pdf"`, `"slide"`, `"site"`, `"doc"`, or `"catalog"`). |

- **Returns (`list[dict[str, str]]`)**: Preset dictionaries containing `"name"`, `"file"`, and `"description"`.

## `def` list_html_css()

Convenience wrapper returning metadata dictionaries (`"name"`, `"file"`, `"description"`) for all built-in HTML CSS presets (`list_css(target="html")`).

```python
from drawlib.tools import list_html_css

list_html_css() -> list[dict[str, str]]
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| *(none)* | — | — | Returns built-in HTML CSS preset metadata list. |

## `def` list_pdf_css()

Convenience wrapper returning metadata dictionaries (`"name"`, `"file"`, `"description"`) for all built-in PDF CSS presets (`list_css(target="pdf")`).

```python
from drawlib.tools import list_pdf_css

list_pdf_css() -> list[dict[str, str]]
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| *(none)* | — | — | Returns built-in PDF CSS preset metadata list. |

## `def` list_project_types()

Return a mapping of all supported starter project archetype names (`"site"`, `"catalog"`, `"doc"`, `"slide"`, `"images"`) to their human-readable descriptions.

```python
from drawlib.tools import list_project_types

list_project_types() -> dict[str, str]
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| *(none)* | — | — | Returns `dict[str, str]` mapping archetype name to summary description. |

## `def` list_slide_css()

Convenience wrapper returning metadata dictionaries (`"name"`, `"file"`, `"description"`) for all built-in presentation slide CSS presets (`list_css(target="slide")`).

```python
from drawlib.tools import list_slide_css

list_slide_css() -> list[dict[str, str]]
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| *(none)* | — | — | Returns built-in slide CSS preset metadata list. |

## `def` scan_broken_links(root_dir)

Recursively scan all built `.html` files inside `root_dir` to verify internal relative links, `#slug` fragment anchors, and referenced static/diagram assets.

```python
from drawlib.tools import scan_broken_links

scan_broken_links(
    root_dir: str,
) -> tuple[int, int, list[tuple[str, str, str]]]
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `root_dir` | `str` | *(required)* | Built HTML root directory to scan (e.g., `"docs_html"` or `"catalog_html"`). |

- **Returns (`tuple[int, int, list[tuple[str, str, str]]]`)**: `(total_html_files, total_links_checked, broken_links)`, where each entry in `broken_links` is `(html_rel_path, tag_name, target_url)`.

## `def` serve_docs(directory, port=8000, open_browser=True, skip_check=False, check_only=False)

Run the local HTTP preview server serving static HTML files from `directory`, or perform a headless pre-flight broken-link scan and exit when `check_only=True`.

```python
from drawlib.tools import serve_docs

serve_docs(
    directory: str,
    port: int = 8000,
    open_browser: bool = True,
    skip_check: bool = False,
    check_only: bool = False,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `directory` | `str` | *(required)* | Built HTML directory to serve (raises `ValueError` if missing or not a directory). |
| `port` | `int` | `8000` | Local TCP port number for the HTTP preview server. |
| `open_browser` | `bool` | `True` | Automatically launch the default desktop web browser when starting the server. |
| `skip_check` | `bool` | `False` | Skip running `scan_broken_links()` prior to starting the HTTP server. |
| `check_only` | `bool` | `False` | Run `scan_broken_links()` and exit immediately without starting the HTTP server. |

## `def` show_code_block(file_path=None, target=None, styles_path=None, ...)

Execute a `drawlib` block from a Markdown/HTML file or a standalone `.py` script and open the rendered image in a desktop GUI viewer (or delegate to headless `export_code_block()` when `output_path` is provided).

```python
from drawlib.tools import show_code_block

show_code_block(
    file_path: str | None = None,
    target: str | None = None,
    styles_path: str | None = None,
    utils_path: str | None = None,
    grid: bool = False,
    output_path: str | None = None,
    no_cache: bool = False,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `file_path` | `str \| None` | `None` | Path to the Markdown (`.md`), HTML (`.html`), or Python (`.py`) file. |
| `target` | `str \| None` | `None` | Block image filename (e.g., `"hero.png"`) or 1-based index (`"1"`). Prints block table if omitted. |
| `styles_path` | `str \| None` | `None` | Optional path to a custom `styles.py` script. |
| `utils_path` | `str \| None` | `None` | Optional path to a custom `utils.py` script. |
| `grid` | `bool` | `False` | Overlay the coordinate grid on the displayed or exported image. |
| `output_path` | `str \| None` | `None` | Optional output file path; suppresses GUI viewer and writes directly to disk when specified. |
| `no_cache` | `bool` | `False` | Bypass reading and writing the SQLite build image cache. |
