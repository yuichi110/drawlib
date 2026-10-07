# Slide Presenter View & Speaker Notes Implementation Plan

## 1. Overview & Goals

Add a Google Slides / Reveal.js style **Presenter View (プレゼンタービュー / スピーカーノート機能)** to Drawlib slide decks (`drawlib build slide`).

Key capabilities:
1. **Markdown Speaker Notes (`::: note` / `::: notes`)**:
   - Authors can write speaker notes inside any slide `.md` file using `::: note` (or `::: notes`).
   - Notes are excluded from the main 1920×1080 presentation stage and PDF exports, and embedded as hidden `<aside class="slide-notes">` markup inside each `<section class="slide">`.
2. **Synchronized Dual-Window Presenter View**:
   - Pressing `P` or `S` on the keyboard, or clicking the Presenter View button (`🗒` / Notes icon) in `.slide-controls`, opens a synchronized secondary browser window (`index.html?presenter=1#<currentSlide>`).
   - Main window and Presenter View window stay bidirectionally synchronized via `BroadcastChannel('drawlib_slide_sync')` and `window.opener` / popup `postMessage` fallback (so it works on both `http://localhost` and `file://`).
3. **Custom 2-Column Presenter View Layout**:
   ```text
   +--------------------+---------------------------------------------------+
   |  Slide List        |                                                   |
   |  (縦スクロール)     |              現在のページ (16:9 Preview)            |
   |                    |        ※アニメーション進行状態もメイン画面と同期       |
   |  +--------------+  |                                                   |
   |  | 1. Title     |  |                                                   |
   |  +--------------+  +---------------------------------------------------+
   |  | 2. Agenda    |  | [◀ 前へ]  5 / 9  [次へ ▶]  | [▶ アニメ再生] | 03:42 |
   |  +--------------+  +---------------------------------------------------+
   |  | 3. Why ...   |  | Speaker Notes                               [A-][A+]|
   |  +--------------+  |                                                   |
   |  | ...          |  | ・ここには発表者用のカンペ（Markdown）を表示します     |
   |                    | ・メイン画面やPDFには一切表示されません               |
   +--------------------+---------------------------------------------------+
   ```
   - **Left Column**: Vertical scrollable list of live scaled slide thumbnails (`1..N`). Clicking any thumbnail jumps both Presenter View and the Main Window to that slide. Active slide is highlighted and auto-scrolled into view.
   - **Right Top**: Large 16:9 live preview of the current slide, including synchronized `<canvas>` animation frames.
   - **Right Middle (Control Bar)**:
     - Slide navigation: `[◀ Prev]`, slide indicator (`5 / 9`), `[Next ▶]`
     - **Animation Control Button**:
       - Disabled (grayed out) if the current slide has no `.drawlib-anim-container`.
       - Enabled if the current slide has an animation, dynamically updating its label/icon based on player state (`▶ Play`, `⏸ Pause`, `▶ Resume`, `↻ Replay`). Clicking it triggers the animation step on both the Main Window and Presenter View simultaneously.
     - **Elapsed Timer**: `00:00` stopwatch (click to pause/resume, reset button `↺`).
   - **Right Bottom (Speaker Notes Pane)**:
     - Renders the HTML compiled from `::: note` / `::: notes` for the current slide (or a subtle placeholder `"No speaker notes for this slide."` when empty).
     - Includes font-size adjustment buttons (`A-` / `A+`) for comfortable reading.

---

## 2. Markdown Syntax for Speaker Notes

In any slide `.md` file (e.g., `01_title.md`, `05_workflows.md`):

```markdown
::: note
- Emphasize that **SQLite hash caching** restores unchanged diagrams in `< 1ms`.
- Click the animation button twice to walk through the `Hit` and `Miss` branches.
:::
```

- Both `::: note` and `::: notes` are supported.
- If multiple `::: note` blocks exist in the same slide file (for example, placing a note right after each corresponding `::: block`), their raw Markdown contents are stripped and joined with a blank line (`"\n\n".join(note_chunks)`) before compiling to HTML via `parse_markdown_to_html()`.
- Markdown inside `::: note` (lists, bold, inline code, headings, links, horizontal rules) is compiled to HTML via `parse_markdown_to_html()`.

---

## 3. Architecture & File Changes

### Phase 1: Note Extraction & HTML Compilation (`src/drawlib/_slide/`)

1. **[`src/drawlib/_slide/_blocks.py`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_slide/_blocks.py)**
   - Add `PATTERN_SLIDE_NOTE`:
     ```python
     PATTERN_SLIDE_NOTE: Final[re.Pattern[str]] = re.compile(
         r"(?:\n|^)[ \t]*:::+[ \t]*notes?(?:[ \t]+[^\n]*)?\n(.*?)\n[ \t]*:::+",
         re.DOTALL | re.IGNORECASE,
     )
     ```
   - Add `extract_slide_notes(text: str) -> tuple[str, str]`:
     - Extracts all `::: note` / `::: notes` blocks from raw slide Markdown before container box processing.
     - Joins multiple extracted note chunks with a blank line (`"\n\n".join(chunks)`) and compiles the combined Markdown via `parse_markdown_to_html()`.
     - Returns `(cleaned_markdown_without_notes, rendered_notes_html)`.
     - Ensures a slide that has raw Markdown + `::: note` (without explicit `::: block`) still auto-wraps the remaining slide content properly.

2. **[`src/drawlib/_slide/compiler.py`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_slide/compiler.py)**
   - In `build_slide()`, call `extract_slide_notes(raw_content)` before `PATTERN_CONTAINER_BOX.search()`.
   - Update `_assemble_slide_section(rendered_body: str, idx: int, notes_html: str = "") -> str` to include:
     ```html
     <section class="slide" data-slide-index="1">
       <div class="slide-body">...</div>
       <aside class="slide-notes" hidden>...</aside>
     </section>
     ```
   - Add Presenter View button (`#btn-presenter`) to `.slide-controls`:
     ```html
     <button id="btn-presenter" title="Presenter View (P / S)">🗒</button>
     ```

### Phase 2: Presenter View UI & Cross-Window Sync (`src/drawlib/_templates/project/slide/slide.js`)

1. **Cross-Window Synchronization Channel**:
   - Create a sync manager using `BroadcastChannel('drawlib_slide_sync')` (when available) + `window.opener` / `presenterWindow` `postMessage` fallback so synchronization works seamlessly across both `http://` and `file://` origins.
   - Message types:
     - `{ type: 'SYNC_SLIDE', slide: number }`: Synchronizes `goToSlide(slide, { broadcast: false })`.
     - `{ type: 'SYNC_ANIM_ACTION', slide: number, playerIndex: number }`: Triggers `handleClick()` on the target animation player in both windows so frame progression stays in lockstep.
     - `{ type: 'PRESENTER_READY' }`: Sent when Presenter View opens so the Main Window immediately replies with its current `currentSlide`.

2. **Animation Player State Hooks**:
   - Extend `createAnimPlayer()` in `slide.js` to accept an `onStateChange` callback and expose `getCurrentFrame()` / `getTotalFrames()` / `getState()`.
   - When the user clicks an animated diagram directly on the slide or clicks the Presenter View's Animation Button, broadcast `SYNC_ANIM_ACTION` so both windows advance together.

3. **Presenter View Mode (`?presenter=1`)**:
   - Detect `const isPresenterMode = new URLSearchParams(window.location.search).get('presenter') === '1';`.
   - When `isPresenterMode` is true:
     - Add `document.body.classList.add('presenter-mode')`.
     - Dynamically construct `.presenter-layout` with:
       - **Left Sidebar (`.presenter-sidebar`)**: Vertical list of `.presenter-thumb-item` cards (reusing the `.overview-thumb` live scaled DOM preview mechanism).
       - **Right Top (`.presenter-Main-preview`)**: Wraps `.presentation-viewport` / `.presentation-stage` scaled to fit the preview pane container via `ResizeObserver` / `window.resize`.
       - **Right Middle (`.presenter-toolbar`)**:
         - `#pv-btn-prev` (`◀ Prev`), `#pv-slide-indicator` (`1 / 9`), `#pv-btn-next` (`Next ▶`)
         - `#pv-btn-anim` (`▶ Play Animation` / `▶ Next Step (Paused)` / `⏸ Pause` / `↻ Replay` — disabled & grayed out when current slide has no animation)
         - `#pv-timer` (`00:00`) + `#pv-btn-timer-reset` (`↺`)
       - **Right Bottom (`.presenter-notes-panel`)**:
         - Header with `"Speaker Notes"` title and `A-` / `A+` font size buttons (`#pv-font-dec`, `#pv-font-inc`).
         - Scrollable `#pv-notes-content` populated from the active slide's `<aside class="slide-notes">`.

4. **Shortcut Keys**:
   - Press `P` or `S` in the main window (or click `#btn-presenter`) to open `index.html?presenter=1#${currentSlide}` via `window.open(..., 'drawlib_presenter', 'width=1280,height=860')`.

### Phase 3: Presenter View Styles (`src/drawlib/_templates/css/targets/slide.css` & `slide_about_drawlib_src/style.css`)

- Add `.slide-notes { display: none !important; }` so speaker notes never appear on the main stage or in print/PDF.
- Add `body.presenter-mode` styles:
  - CSS Grid / Flexbox 2-column layout (`280px` left sidebar + `1fr` right column).
  - Right column split into:
    - Top: `.presenter-preview-pane` (`flex: 1 1 52%; min-height: 240px;`)
    - Middle: `.presenter-toolbar` (`height: 56px; flex-shrink: 0;`) with styled buttons and `:disabled` grayed-out state for `#pv-btn-anim`.
    - Bottom: `.presenter-notes-pane` (`flex: 1 1 38%; min-height: 180px; overflow-y: auto;`).

### Phase 4: Sample Slide Notes, Docs & Unit Tests

1. **Sample Slide Deck (`slide_about_drawlib_src/`)**:
   - Add realistic `::: note` speaker notes to `slide_about_drawlib_src/01_title.md` .. `09_ecosystem.md` (especially `05_workflows.md` explaining the click-to-play animation and pause points) and template slides (`src/drawlib/_templates/project/slide/`).
2. **Documentation & Rules**:
   - Update [`docs_src/07_doc_builder_and_cli/project_slide.md`](file:///usr/local/google/home/yuichiito/git_github/drawlib/docs_src/07_doc_builder_and_cli/project_slide.md) and [`src/drawlib/_rules/lib_slide.md`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_rules/lib_slide.md) with `::: note` syntax and Presenter View (`P` / `S` shortcut) documentation.
3. **Unit Tests (`tests/drawlib/slide/test_slide.py`)**:
   - Test `extract_slide_notes()` and `build_slide()` with `::: note` and `::: notes` blocks:
     - Verify notes are rendered inside `<aside class="slide-notes" hidden>` and stripped from `.slide-body`.
     - Verify `#btn-presenter` and Presenter View logic are present in compiled output.
4. **Verification**:
   - Run `./dcli code-check all`, `./dcli test target slide --no-cov`, and `./dcli docs build slide`.
   - Visually inspect Presenter View (`?presenter=1`) via Playwright screenshot (`view_file`) on both non-animated and animated slides to verify the disabled/enabled animation button, vertical slide list, current slide preview, and speaker notes!
