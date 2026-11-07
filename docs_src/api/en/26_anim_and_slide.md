# drawlib.anim & drawlib.slide

`drawlib.anim` generates multi-frame **APNG** (`.png`), **Animated WebP** (`.webp`), and dither-free **Animated GIF** (`.gif`) illustrations via the `Animation` frame manager, while `drawlib.slide` provides `1920×1080` presentation stage helpers (`current_slide`, `draw_page_number`, `draw_section_header`) and compilers (`build_slide`, `build_pptx`) for interactive HTML and native editable PowerPoint decks.

```drawlib align=center code=fold file=26_anim_and_slide_hero.png caption="Static Overview of drawlib.anim Keyframe Timeline and drawlib.slide 16:9 Stage Architecture"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import BoxList
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=134, height=62)

# Left Panel: drawlib.anim Keyframe Timeline
rectangle((35, 31), width=60, height=52, style=Styles.Neutral.patch(shape_r=2.5))
phosphor.play_circle((11.5, 51.5), width=4.6, style=Styles.PrimaryBold)
text((37.5, 51.5), "drawlib.anim · Keyframe Loop", style=Styles.DarkBold.patch(text_size=11.5))

frames = [
    (16.5, "Frame 1", "0.0s", Styles.PrimaryNeutral, Styles.DarkBold, Styles.Dark),
    (35.0, "Frame 2", "0.5s", Styles.PrimaryNeutral, Styles.DarkBold, Styles.Dark),
    (53.5, "Frame 3", "1.0s", Styles.PrimaryFlat, Styles.WhiteBold, Styles.White),
]
for fx, title, ts, fst, tst, sst in frames:
    rectangle((fx, 35.5), width=16.5, height=16.5, style=fst.patch(shape_r=1.8))
    text((fx, 38.5), title, style=tst.patch(text_size=10.5))
    text((fx, 32.0), ts, style=sst.patch(text_size=10.0))

line((14, 21.5), (56, 21.5), arrow_head="->", style=Styles.PrimaryBold)
for fx in (16.5, 35.0, 53.5):
    circle((fx, 21.5), radius=1.2, style=Styles.PrimaryFlat)

anim_out = BoxList(style=Styles.SecondaryNeutral, text_style=Styles.DarkBold.patch(text_size=10.0))
anim_out.add("save('flow.png') APNG")
anim_out.add("save('flow.webp') WebP")
anim_out.draw(xy=(8.5, 8.5), box_width=26.5, box_height=7.5, direction="left")

# Right Panel: drawlib.slide 16:9 Presentation Stage
rectangle((99, 31), width=60, height=52, style=Styles.SecondaryNeutral.patch(shape_r=2.5))
phosphor.presentation_chart((75.0, 51.5), width=4.6, style=Styles.SecondaryBold)
text((101.5, 51.5), "drawlib.slide · 16:9 Stage", style=Styles.DarkBold.patch(text_size=11.5))

# Miniature 16:9 Stage (50 x 28)
rectangle(
    (99, 32.5),
    width=50,
    height=28,
    style=Styles.Neutral.patch(shape_fill_color=Colors.White, shape_r=1.5),
)
rectangle((81.5, 32.5), width=15, height=28, style=Styles.PrimaryFlat.patch(shape_r=1.2))
text((81.5, 36.0), "SEC 02", style=Styles.WhiteBold.patch(text_size=10.0))
text((81.5, 30.0), "split", style=Styles.White.patch(text_size=10.0))

rectangle((107.5, 35.5), width=29, height=15, style=Styles.Neutral.patch(line_style="dashed", shape_r=1.2))
text((107.5, 38.2), "BoundingBox", style=Styles.DarkBold.patch(text_size=10.2))
text((107.5, 32.5), "1920 x 1080 px", style=Styles.Dark.patch(text_size=10.0))
text((117.5, 22.2), "4 / 9", style=Styles.PrimaryBold.patch(text_size=10.0))

slide_out = BoxList(style=Styles.Neutral, text_style=Styles.DarkBold.patch(text_size=10.0))
slide_out.add("build_slide() -> HTML")
slide_out.add("build_pptx() -> .pptx", style=Styles.PrimaryNeutral)
slide_out.draw(xy=(72.5, 8.5), box_width=26.5, box_height=7.5, direction="left")

save()
```

## `class` Animation

Multi-frame animation coordinator imported from `drawlib.anim`. Initializing an `Animation` instance registers it with the active Drawlib canvas so calling `drawlib.canvas.save()` writes all captured frames into a lossless **APNG** (`.png`, `.apng`), lossless **Animated WebP** (`.webp`), or dither-free **Animated GIF** (`.gif`) file.

```python
from drawlib.anim import Animation

Animation(
    fps: float | None = None,
    frame_rate: float | None = None,
    loop: PosInt = 0,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `fps` | `float \| None` | `None` (`10.0`) | Target playback frame rate in frames per second (`> 0`). Defaults to `10.0` when omitted. |
| `frame_rate` | `float \| None` | `None` | Alias for `fps`; if both are supplied, `fps` takes precedence. |
| `loop` | `PosInt` (`int >= 0`) | `0` | Playback loop count (`0` = infinite continuous playback). |

### Properties & Public Methods

| Member | Kind | Signature / Type | Description |
| :--- | :--- | :--- | :--- |
| `fps` | `property` | `float` | Effective playback frame rate in frames per second. |
| `frame_rate` | `property` | `float` | Alias property returning `fps`. |
| `frame` | `method` | `(duration: float \| None = None, clear: bool = True) -> Generator[None, None, None]` | Context manager (`with anim.frame(...):`) that optionally clears previous artists (`clear=True` independent mode, `clear=False` cumulative mode) and captures the frame on block exit. `duration` is in seconds (`None` uses `1 / fps`). |
| `add_frame` | `method` | `(duration: float \| None = None, clear: bool = True) -> None` | Imperatively capture the current canvas state as a frame (`duration` in seconds) and clear canvas artists afterward when `clear=True`. |

## `class` BoundingBox

Immutable dataclass imported from `drawlib.slide` representing a rectangular region on the `1920×1080` presentation stage.

```python
from drawlib.slide import BoundingBox

BoundingBox(
    x: float,
    y: float,
    width: float,
    height: float,
) -> None
```

| Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `x` | `float` | *(required)* | Horizontal coordinate of the top-left corner in stage pixels (`0` to `1920`). |
| `y` | `float` | *(required)* | Vertical coordinate of the top-left corner in stage pixels (`0` to `1080`). |
| `width` | `float` | *(required)* | Width of the bounding box in stage pixels. |
| `height` | `float` | *(required)* | Height of the bounding box in stage pixels. |

## `class` SlideContext

Immutable dataclass imported from `drawlib.slide` holding the 1-based slide index and total slide count during deck compilation (stored inside a `contextvars.ContextVar` and exposed via [`current_slide`](#current-slide)).

```python
from drawlib.slide import SlideContext

SlideContext(
    index: int = 1,
    total: int = 1,
) -> None
```

| Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `index` | `int` | `1` | 1-based index of the current slide in sorted deck order. |
| `total` | `int` | `1` | Total number of slides in the presentation deck. |

### Properties & Public Methods

| Member | Kind | Signature / Type | Description |
| :--- | :--- | :--- | :--- |
| `text` | `property` | `str` | Standard formatted slide counter string `"{index} / {total}"` (e.g., `"4 / 9"`). |
| `format` | `method` | `(template: str = "{index} / {total}") -> str` | Format a custom counter string substituting `{index}` and `{total}` placeholders. |

## `def` build_pptx(input_dir, output_file=None, *, ...)

Compile an `i18n`-native Markdown `slide` project directory (`drawlib.toml` + `<lang>/` slides) into native editable 16:9 (`960×540 pt`) Microsoft PowerPoint (`<stem>_<lang>.pptx`) decks. Measures exact `1920×1080` stage geometry via headless Chromium (`playwright`) and converts `::: block` cards, typography, lists, tables, code blocks, `::: note` speaker notes, and high-DPI static PNG diagrams via `python-pptx` (also re-exported in [`drawlib.tools`](27_tools.md)).

```python
from drawlib.slide import build_pptx

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
    workers: int | Literal["auto"] = "auto",
) -> str
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `input_dir` | `str` | *(required)* | Slide project root directory containing `drawlib.toml` (`type = "slide"`, `[i18n]`) and `<lang>/` slide files. |
| `output_file` | `str \| None` | `None` | Optional destination `.pptx` base path or directory (emits `<stem>_<lang>.pptx` for each locale). |
| `title` | `str \| None` | `None` | Presentation title override written to `.pptx` core metadata. |
| `theme` | `str \| None` | `None` | CSS theme preset override (`"google"`, `"default"`, `"google-dark"`, `"default-dark"`, `"monochrome"`). |
| `dpi` | `int` | `240` | Rasterization DPI for embedded `drawlib` static PNG diagrams (`> 0`). |
| `anim_frame` | `Literal["first", "last"]` | `"last"` | Frame extracted as a static PNG when a slide block uses [`Animation`](#animation). |
| `styles_path` | `str \| None` | `None` | Optional path to a custom `styles.py` script. |
| `utils_path` | `str \| None` | `None` | Optional path to a custom `utils.py` script. |
| `no_cache` | `bool` | `False` | Bypass reading and writing the `.drawlib/cache.db` SQLite image cache. |
| `timestamp` | `bool` | `False` | Write the current build timestamp into OpenXML metadata instead of deterministic normalization. |
| `workers` | `int \| Literal["auto"]` | `"auto"` | Parallel worker process count (`"auto"` resolves to `1 <= (CPU cores - 1) <= 8`, honoring `DRAWLIB_BUILD_WORKERS`; `1` runs sequentially in-process). |

- **Returns (`str`)**: Absolute path to the generated default-locale `<stem>_<default_lang>.pptx` file.
- **Raises**: `ValueError` if `input_dir` is invalid, lacks `drawlib.toml`, `dpi <= 0`, `anim_frame` is invalid, or `workers` is invalid; `RuntimeError` if Playwright, Chromium, or `python-pptx` fails.

## `def` build_slide(input_dir, output_dir=None, *, ...)

Compile an `i18n`-native Markdown `slide` project directory into a standalone multi-locale 16:9 HTML presentation deck with Presenter View (`?presenter=1`), keyboard HUD controls, inline SVG font bundling, and `<canvas>` animation playback (also re-exported in [`drawlib.tools`](27_tools.md)).

```python
from drawlib.slide import build_slide

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
    workers: int | Literal["auto"] = "auto",
) -> str
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `input_dir` | `str` | *(required)* | Slide project root directory containing `drawlib.toml` (`type = "slide"`, `[i18n]`) and `<lang>/` slides. |
| `output_dir` | `str \| None` | `None` | Target output directory (defaults to `<base>_html`). |
| `title` | `str \| None` | `None` | Optional HTML `<title>` override. |
| `theme` | `str \| None` | `None` | CSS theme preset override (`"google"`, `"default"`, `"google-dark"`, `"default-dark"`, `"monochrome"`). |
| `image_format` | `str` | `"svg"` | Default output format (`"svg"`, `"webp"`, or `"png"`) for embedded `drawlib` blocks. |
| `dpi` | `int \| None` | `None` | Optional rasterization DPI override when generating raster diagrams. |
| `force_image_format` | `bool` | `False` | When `True`, rewrite explicit block filenames (such as `.svg`) to `image_format`. |
| `static_anim_frame` | `Literal["first", "last"] \| None` | `None` | If set (`"first"` or `"last"`), flatten multi-frame animations into static PNG images. |
| `styles_path` | `str \| None` | `None` | Optional path to a custom `styles.py` script. |
| `utils_path` | `str \| None` | `None` | Optional path to a custom `utils.py` script. |
| `no_cache` | `bool` | `False` | Bypass reading and writing the SQLite diagram build cache. |
| `workers` | `int \| Literal["auto"]` | `"auto"` | Parallel worker process count (`"auto"` resolves to `1 <= (CPU cores - 1) <= 8`, honoring `DRAWLIB_BUILD_WORKERS`; `1` runs sequentially in-process). |

- **Returns (`str`)**: Absolute path to `<output_dir>/<default_lang>/index.html` (an automatic root `<output_dir>/index.html` redirector is also written).
- **Raises**: `ValueError` if `input_dir` is invalid, lacks `drawlib.toml`, fails i18n structural parity validation, or `workers` is invalid.

## `const` current_slide

Dynamic runtime proxy (`_CurrentSlideProxy` instance imported from `drawlib.slide`) that reads the active [`SlideContext`](#slidecontext) during `build_slide()` or `build_pptx()` execution. Outside slide compilation (e.g., standalone `drawlib show`), it safely falls back to `SlideContext(index=1, total=1)`.

```python
from drawlib.slide import current_slide

counter_str: str = current_slide.text
custom_str: str = current_slide.format("Slide {index} of {total}")
```

| Member | Type | Description |
| :--- | :--- | :--- |
| `current_slide.index` | `int` | 1-based index of the slide currently being rendered. |
| `current_slide.total` | `int` | Total number of slides in the active locale's deck. |
| `current_slide.text` | `str` | Formatted counter string `"{index} / {total}"` (also returned by `str(current_slide)`). |
| `current_slide.format(template="{index} / {total}")` | `str` | Render a custom string using `{index}` and `{total}` format placeholders. |

## `def` draw_page_number(width=14, height=3, *, ...)

Render a standardized transparent slide page counter badge (`14×3` canvas by default) using [`current_slide`](#current-slide), designed for placement inside a bottom-right `::: block xy=(1700, 1010) width=140 height=30` stage block.

```python
from drawlib.slide import draw_page_number

draw_page_number(
    width: PosInt = 14,
    height: PosInt = 3,
    *,
    template: str = "{index} / {total}",
    style: Style | None = None,
    auto_setup: bool = True,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | `PosInt` | `14` | Badge canvas width in coordinate units (`> 0`). |
| `height` | `PosInt` | `3` | Badge canvas height in coordinate units (`> 0`). |
| `template` | `str` | `"{index} / {total}"` | Counter format string accepting `{index}` and `{total}` placeholders. |
| `style` | `Style \| None` | `None` | Optional text `Style` override (defaults to `Styles.Muted.patch(text_size=65.0)`). |
| `auto_setup` | `bool` | `True` | Automatically call `clear()` and `setup(width=width, height=height, alpha=0.0)` before drawing. |

## `def` draw_section_header(section_num, title, subtitle="", ...)

Render a full-bleed 16:9 section divider slide (`192.0×108.0` canvas, placed inside `::: block xy=(0, 0) width=1920 height=1080`) with four layout variants (`"split"`, `"centered"`, `"banner"`, `"minimal"`), optional topic preview cards, progress indicator dots, and automatic slide numbering.

```python
from drawlib.slide import draw_section_header

draw_section_header(
    section_num: PosInt,
    title: str,
    subtitle: str = "",
    topics: Sequence[str | tuple[str, str]] = (),
    total_sections: PosInt = 0,
    *,
    variant: Literal["split", "centered", "banner", "minimal"] = "split",
    section_label: str = "SECTION",
    badge_text: str | None = None,
    show_page_number: bool = True,
    show_decorations: bool = True,
    auto_setup: bool = True,
    left_panel_style: Style | None = None,
    right_panel_style: Style | None = None,
    divider_bar_style: Style | None = None,
    decoration_style: Style | None = None,
    section_label_style: Style | None = None,
    section_num_style: Style | None = None,
    active_dot_style: Style | None = None,
    completed_dot_style: Style | None = None,
    upcoming_dot_style: Style | None = None,
    badge_style: Style | None = None,
    badge_text_style: Style | None = None,
    title_style: Style | None = None,
    subtitle_style: Style | None = None,
    line_style: Style | None = None,
    topic_card_style: Style | None = None,
    topic_text_style: Style | None = None,
    topic_description_style: Style | None = None,
    topic_badge_style: Style | None = None,
    topic_badge_text_style: Style | None = None,
    page_number_style: Style | None = None,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `section_num` | `PosInt` | *(required)* | 1-based section number (`>= 1`). Raises `ValueError` if `< 1`. |
| `title` | `str` | *(required)* | Primary section heading displayed prominently on the slide. |
| `subtitle` | `str` | `""` | Optional one-line summary subtitle rendered beneath `title`. |
| `topics` | `Sequence[str \| tuple[str, str]]` | `()` | Optional topic titles or `(title, description)` tuples rendered as `CardList` preview cards. |
| `total_sections` | `PosInt` | `0` | Total sections in the deck (`> 0` enables progress indicator dots and a `"Part X of Y"` badge). |
| `variant` | `Literal["split", "centered", "banner", "minimal"]` | `"split"` | Layout design: `"split"` (left dark panel + right neutral workspace), `"centered"` (centered badge + horizontal cards), `"banner"` (top dark hero band), or `"minimal"` (light editorial with left accent stripe). |
| `section_label` | `str` | `"SECTION"` | Uppercase label prefix displayed above or beside `section_num`. |
| `badge_text` | `str \| None` | `None` | Custom badge string overriding the auto-generated `"Part X of Y"` text. |
| `show_page_number` | `bool` | `True` | Draw `current_slide.text` at the bottom-right corner when `True`. |
| `show_decorations` | `bool` | `True` | Draw subtle geometric background circles when `True`. |
| `auto_setup` | `bool` | `True` | Automatically call `clear()` and `setup(width=192, height=108)` before drawing. |
| `*_style` | `Style \| None` | `None` | Optional granular `Style` overrides for panels (`left_panel_style`, `right_panel_style`), dividers (`divider_bar_style`, `line_style`, `decoration_style`), progress dots (`active_dot_style`, `completed_dot_style`, `upcoming_dot_style`), header labels (`section_label_style`, `section_num_style`, `badge_style`, `badge_text_style`, `title_style`, `subtitle_style`), topic cards (`topic_card_style`, `topic_text_style`, `topic_description_style`, `topic_badge_style`, `topic_badge_text_style`), and `page_number_style`. |
