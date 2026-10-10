# HTML Presentation Slide Deck

This directory contains a self-contained HTML presentation compiled by **Drawlib**.

---

## 1. How to Open & Present

- **Direct Browser Open (Zero Dependencies)**:
  Double-click or open `index.html` directly in any modern browser (Chrome, Edge, Firefox, Safari). No Python, Drawlib, or web server is required.
- **Local HTTP Server (Optional)**:
  ```bash
  python3 -m http.server 8000
  ```

---

## 2. Keyboard Shortcuts & On-Screen Controls

| Key / Control | Action | Description |
| :--- | :--- | :--- |
| `→` / `Space` / `PageDown` | **Next Slide** | Advance to the next slide. |
| `←` / `PageUp` | **Previous Slide** | Return to the previous slide. |
| `Home` / `End` | **First / Last Slide** | Jump to the first or last slide. |
| `A` (or click diagram) | **Animation Control** | Play, pause, resume, or reset interactive diagram animations on the current slide. |
| `P` / `S` (or `🗒` button) | **Presenter View** | Open the synchronized Dual-Window Presenter View. |
| `O` / `Esc` (or `⊞` button) | **Slide Overview** | Toggle the thumbnail overview grid to jump to any slide. |
| `F` (or `⛶` button) | **Fullscreen** | Toggle browser fullscreen mode. |

---

## 3. Dual-Window Presenter View

Press **`P`** or **`S`** (or click the **`🗒`** icon in the bottom-right control bar) to open the **Presenter View** window (`index.html?presenter=1`):

- **Real-Time Dual-Window Sync**: Moving between slides or triggering animations in either window keeps the audience screen and Presenter View synchronized automatically.
- **Interactive Animation Button**: Click **`▶ Play Animation`** / **`⏸ Pause`** / **`▶ Resume`** / **`↻ Reset`** (or press `A`) to step through animated diagrams without touching the audience screen.
- **Presentation Timer**:
  - **Click** the timer (`00:00`) to pause or resume counting.
  - **Double-click** the timer to reset to `00:00`.
- **Customizable Layout & Speaker Notes**:
  - Click **`A-`** / **`A+`** to adjust the speaker notes font size.
  - Drag the vertical divider (between slide thumbnails and preview) or horizontal divider (above Speaker Notes) to resize panels.
