# 3. Recommended Remediation Roadmap

This chapter tracks all **10 prioritized engineering actions** identified during the `full_audit` diagnostic—recording the **4 `P0`/`P1` supply-chain, container, and offline-asset remediations already landed and verified in-tree** alongside the **6 remaining `P1`/`P2` maintainability, browser harness, and governance follow-ups**, with exact target files, implementation steps, and rule/CVE traceability.

```drawlib align=center code=hide file=ch03_remediation_roadmap.png caption="Phased Engineering Remediation Timeline (P0 & P1 Hardening Landed -> Remaining P1/P2 Polish)"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import KpiCards, Panel, Roadmap
from drawlib.styles import Colors, Styles

setup(width=166, height=88)

# 1. Top Target Outcome KPI Strip
kpis = KpiCards(
    style=Styles.Neutral,
    metric_style=Styles.DarkBold.patch(text_size=13.5),
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Muted.patch(text_size=10.0),
    accent_style=Styles.PrimaryFlat,
    accent_position="left_pill",
    metric_layout="left_column",
    metric_width_ratio=0.33,
    spacing=3.5,
)
kpis.add(
    "0 CVEs",
    "P0 Landed (Pillow 13.0)",
    "Cleared all 41 Pillow CVEs",
    style=Styles.SuccessNeutral,
    metric_style=Styles.SuccessBold.patch(text_size=13.0),
    accent_style=Styles.SuccessFlat,
)
kpis.add(
    "99.5%",
    "P1 Landed (UID + Icons)",
    "UID 10001 + pkg.files check",
    style=Styles.PrimaryNeutral,
    metric_style=Styles.PrimaryBold.patch(text_size=13.5),
    accent_style=Styles.PrimaryFlat,
)
kpis.add(
    "0 Cycles",
    "P2 Pure Library DAG",
    "Acyclic DAG + SECURITY.md",
    style=Styles.Neutral,
    metric_style=Styles.DarkBold.patch(text_size=12.5),
    accent_style=Styles.SecondaryFlat,
)
kpis.draw(xy=(5.0, 66.5), width=156.0, height=16.5, columns=3, align="bottom_left")

# 2. Main Phased Execution Roadmap Panel
roadmap_panel = Panel(
    "Phased Remediation Execution Timeline (P0 -> P1 -> P2)",
    "4 Landed · 6 Follow-Up Actions",
    style=Styles.White.patch(shape_line_color=Colors.Gray3, shape_line_width=1.0),
    header_style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.5),
    description_style=Styles.White.patch(text_size=10.0),
    icon=phosphor.rocket_launch,
    icon_style=Styles.White,
    header_variant="filled",
    header_height=8.5,
)
roadmap_panel.draw((5.0, 5.0), width=156.0, height=58.0, align="bottom_left")
inner_xy, inner_w, inner_h = roadmap_panel.get_content_box(
    (5.0, 5.0),
    width=156.0,
    height=58.0,
    padding=(4.0, 2.2),
    align="bottom_left",
)

rm = Roadmap(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Dark.patch(text_size=10.0),
    spine_style=Styles.DarkBold,
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=10.0),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    curve_bend=0.0,
    card_shape="rounded_rect",
    spacing=2.2,
)
rm.add(
    "P0 [LANDED]: Upgraded Pillow >=13.0.0 (Cleared All 41 CVEs)",
    "Bumped pillow>=13.0.0 in pyproject.toml & uv.lock (13.0.0); Trivy SCA verified 0 CVEs (#1)",
    badge_text="DONE · #1",
    icon=phosphor.check_circle,
    style=Styles.PrimaryNeutral,
    badge_style=Styles.SuccessFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=9.5),
    icon_style=Styles.SuccessBold,
)
rm.add(
    "P1 [3 LANDED / 2 OPEN]: Docker UID 10001, pkg.files Check & Compiler Polish",
    "Landed USER drawlib (#3,#4) & pkg.files check (#6); next: DOCX complexity (#2) & PPTX harness (#5)",
    badge_text="P1 · #2–#6",
    icon=phosphor.wrench,
    style=Styles.Neutral,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=9.5),
    icon_style=Styles.PrimaryBold,
)
rm.add(
    "P2 [OPEN]: Architectural Acyclicity & Governance Polish (Actions #7–#10)",
    "Resolve 2 sibling diagram cycles, library exceptions vs sys.exit(1), Dependabot & SECURITY.md",
    badge_text="P2 · #7–#10",
    icon=phosphor.git_merge,
    style=Styles.Neutral,
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=9.5),
    icon_style=Styles.SecondaryBold,
)
rm.draw(xy=inner_xy, width=inner_w, height=inner_h, align="bottom_left")

save()
```

---

## 3.1 Remediation Strategy & Priority Horizons

Starting from its initial **90/100** diagnostic baseline, Drawlib v0.3.5 executed immediate closed-loop fixes across its `P0` and `P1` supply-chain, container, and offline-asset targets—raising overall health to **94/100 (Grade S)** with **0 `FAIL` rules**, **0 application CVEs**, and **0 container IaC misconfigurations**:

1. **`P0` — Urgent Supply-Chain Vulnerability Closure (Action `#1` — `COMPLETED`)**: Upgraded `pillow` to `>=13.0.0` in `pyproject.toml` and `13.0.0` in `uv.lock`, eliminating all **41 application CVEs** (`5 CRITICAL`, `23 HIGH`, `13 MEDIUM` -> `0`) across Trivy SCA.
2. **`P1` — Container Least Privilege, Offline Asset Fast-Fail & Compiler Complexity (Actions `#2`–`#6` — `3 COMPLETED`, `2 OPEN`)**:
   - **Completed (`#3`, `#4`, `#6`)**: Added non-root `USER drawlib` (`UID 10001`) across `tools/docker/Dockerfile.{prod,test_local,test_pypi}` and `.pni/dockerfiles/root/Dockerfile` (clearing all 3 `HIGH` `DS-0002` findings), and added `pkg.files` membership checks in `src/drawlib/_release_assets.py` and `src/drawlib/_icons/png_icons/_base.py` (fixing all 12 `test_nonexistent_*_icon_error` offline failures and raising offline pass rate to `99.5%`).
   - **Open (`#2`, `#5`)**: Decompose high-complexity DOCX/HTML AST walkers (`cognitive <= 15`) and pre-bake Chromium into `.pni/dockerfiles/Dockerfile` alongside synthetic `PptxSlide` unit tests for `_pptx_writer.py`.
3. **`P2` — Architectural Acyclicity, Library Exception Hygiene & Governance Polish (Actions `#7`–`#10` — `OPEN`)**: Eliminate the final 2 intra-package `_edge <-> _junction` sibling cycles, replace library-level `sys.exit(1)` calls with typed exceptions caught at the CLI boundary, publish `SECURITY.md` + `.github/dependabot.yml`, and align `test_api_docs_completeness.py` with clean-room Docker test contexts.

---

## 3.2 Action Plan Traceability Matrix (`P0 -> P1 -> P2`)

The visual matrix below maps all **10 remediation items** (`P0 -> P1 -> P2`), highlighting the 4 completed in-tree fixes (`DONE`) and the 6 remaining engineering follow-ups.

```drawlib align=center code=hide file=ch03_action_plan_matrix.png caption="Action Plan Traceability Matrix Across All 10 Prioritized Engineering Items (4 Completed, 6 Open)"
from drawlib.canvas import save, setup
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=168, height=96)

text(
    (84.0, 91.2),
    "Action Plan Traceability Matrix — 10 Engineering Actions (4 Landed, 6 Follow-Ups)",
    style=Styles.DarkBold.patch(text_size=12.5),
)

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=10.0),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=10.5),
    border_style=Styles.MutedThin,
    has_header=True,
)

# 1. Alternating neutral row fills first
table.set_style_cell_evenodd(
    even_color=Colors.Light,
    even_text_style=Styles.Dark.patch(text_size=10.0),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=10.0),
)

# 2. Priority column semantic neutral badges (rows 1, 3, 4, 6 completed)
table.set_style_cell(
    background_color=Colors.SuccessNeutral,
    text_style=Styles.SuccessBold.patch(text_size=9.8),
    rows=[1, 3, 4, 6],
    columns=[0],
)
table.set_style_cell(
    background_color=Colors.PrimaryNeutral,
    text_style=Styles.PrimaryBold.patch(text_size=9.8),
    rows=[2, 5],
    columns=[0],
)
table.set_style_cell(
    background_color=Colors.Neutral,
    text_style=Styles.DarkBold.patch(text_size=9.8),
    rows=[7, 8, 9, 10],
    columns=[0],
)

# 3. Re-apply header row style AFTER set_style_cell_evenodd so row 0 stays PrimaryFlat
table.set_style_cell_header(
    background_color=Colors.Primary,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)

table.set_style_border(
    top=Styles.Dark.patch(line_width=1.4),
    top2=Styles.Dark.patch(line_width=1.1),
    bottom=Styles.Dark.patch(line_width=1.4),
    left=Styles.MutedThin,
    left2=Styles.MutedThin,
    right=Styles.MutedThin,
    between_columns=Styles.MutedThin,
    between_rows=Styles.MutedThin,
)

matrix_data = [
    ["Status · #", "Action Title", "Target Files", "Verified / Expected Impact", "Related Rules / CVEs"],
    [
        "DONE · #1\n[P0]",
        "Upgrade Pillow >=13.0.0 &\nverify raster baselines",
        "pyproject.toml,\nuv.lock",
        "Cleared all 41 app CVEs\n(5 CRIT, 23 HIGH -> 0)",
        "security_vulnerability,\n5 CRIT CVEs + GHSA",
    ],
    [
        "OPEN · #2\n[P1]",
        "Decompose high-complexity\nDOCX & fence parsers",
        "exporter_docx.py,\noptions.py, merger.py",
        "Cognitive complexity <=15;\nlowers compiler risk",
        "common/maintainability",
    ],
    [
        "DONE · #3\n[P1]",
        "Non-root Docker USER\nacross all Dockerfiles",
        "Dockerfile.{prod,\ntest_local,test_pypi}",
        "Cleared all 3 HIGH DS-0002\nIaC misconfigurations",
        "security_vulnerability,\nsupply_chain, DS-0002",
    ],
    [
        "DONE · #4\n[P1]",
        "Run production Docker image\nas non-root UID 10001",
        "tools/docker/\nDockerfile.prod",
        "Enforces least privilege\nin Docker PDF/exec runs",
        "common/supply_chain,\ncommon/security",
    ],
    [
        "OPEN · #5\n[P1]",
        "Bake Chromium & assets +\n_pptx_writer unit tests",
        "_pptx_writer.py, pdf.py,\ntest_pptx.py",
        "100% offline pass rate;\n>80% PPTX writer cov",
        "common/\nruntime_verification",
    ],
    [
        "DONE · #6\n[P1]",
        "Validate pkg.files before\nHTTPS asset downloads",
        "_release_assets.py,\npng_icons/_base.py",
        "Fast-fails invalid icons;\nfixed 12 offline tests",
        "common/\nruntime_verification",
    ],
    [
        "OPEN · #7\n[P2]",
        "Eliminate 2 intra-diagram\nsibling import cycles",
        "architecture & flow\n_edge.py / _junction.py",
        "0 runtime circular deps\nacross all 424 modules",
        "common/architecture",
    ],
    [
        "OPEN · #8\n[P2]",
        "Replace library sys.exit(1)\nwith typed exceptions",
        "_settings.py, viewer.py,\n_cli/_drawlib.py",
        "Prevents host termination\nfor library callers",
        "common/\nlibrary_guidelines",
    ],
    [
        "OPEN · #9\n[P2]",
        "Publish SECURITY.md &\nconfigure Dependabot",
        "pyproject.toml,\nquality.yml",
        "Closes OpenSSF disclosure\n& supply-chain gaps",
        "common/supply_chain",
    ],
    [
        "OPEN · #10\n[P2]",
        "Include docs_src/api or\nguard with pytest.skip",
        "test_api_docs_*.py,\n.dockerignore, Dockerfile",
        "Keeps dcli docker test\ngreen (local & PyPI)",
        "python/testing",
    ],
]

table.draw_flexible(
    xy=(5.0, 86.3),
    column_widths=[15.0, 42.0, 34.0, 37.0, 30.0],
    row_heights=[7.3] + [7.4] * 10,
    data=matrix_data,
    align="top_left",
)

save()
```

### Summary Table of All 10 Pre-Sorted Action Items

| # | Priority & Status | Category | Action Title | Target Files | Related Rules / Advisories | Verified / Expected Impact |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **`P0` (`COMPLETED`)** | `security` | **Upgrade locked Pillow dependency to >=13.0.0 and re-verify raster baselines** | `pyproject.toml`, `uv.lock` | `common/security_vulnerability`, `CVE-2026-112393`..`GHSA-78g4-xqwv-q3g8` | **Landed**: Upgraded to `pillow>=13.0.0` (`13.0.0` in `uv.lock`); eliminated all 41 Trivy application CVEs (`app_vuln_counts = 0`). |
| **2** | **`P1` (`OPEN`)** | `code_quality` | **Decompose High-Complexity DOCX & Fence Parser Routines** | `src/drawlib/_builder/doc_builder/exporter_docx.py`, `src/drawlib/_builder/doc_builder/processor/options.py`, `src/drawlib/_builder/doc_builder/merger.py` | `common/maintainability` | Substantially lowers maintenance risk and unit test surface in the document compiler pipeline (`cognitive <= 15`). |
| **3** | **`P1` (`COMPLETED`)** | `security` | **Add non-root USER to Dockerfiles (`DS-0002`)** | `tools/docker/Dockerfile.prod`, `tools/docker/Dockerfile.test_local`, `tools/docker/Dockerfile.test_pypi` | `common/security_vulnerability`, `common/supply_chain`, `DS-0002` | **Landed**: Added `USER drawlib` (`UID 10001`) across all Dockerfiles; cleared all 3 `HIGH` `DS-0002` container misconfigurations. |
| **4** | **`P1` (`COMPLETED`)** | `security` | **Run Production Docker Image as Non-Root User** | `tools/docker/Dockerfile.prod` | `common/supply_chain`, `common/security` | **Landed**: Configured `/opt/ms-playwright`, `/opt/drawlib-cache`, and `USER drawlib` (`UID 10001`) in `Dockerfile.prod`. |
| **5** | **`P1` (`OPEN`)** | `testing` | **Bake Chromium shell & asset cache into .pni/dockerfiles/Dockerfile and add unit tests for _pptx_writer.py** | `src/drawlib/_slide/_pptx_writer.py`, `src/drawlib/_builder/doc_builder/compiler/pdf.py`, `tests/drawlib/slide/test_pptx.py` | `common/runtime_verification` | Achieves 100% offline `--network=none` test pass rate and lifts `_pptx_writer.py` and `_pptx_dom.py` coverage above 80%. |
| **6** | **`P1` (`COMPLETED`)** | `testing` | **Validate asset filename membership in pkg.files before network downloads** | `src/drawlib/_release_assets.py`, `src/drawlib/_icons/png_icons/_base.py` | `common/runtime_verification` | **Landed**: `find_package_for_resource_path()` and `resolve_png_icon_path()` verify `pkg.files` before network I/O, fixing all 12 offline invalid-icon test failures (`99.5%` offline pass rate). |
| **7** | **`P2` (`OPEN`)** | `architecture` | **Eliminate Remaining 2 Intra-Diagram Sibling Import Cycles** | `src/drawlib/_diagrams/architecture/_edge.py`, `src/drawlib/_diagrams/architecture/_junction.py`, `src/drawlib/_diagrams/flow/_edge.py`, `src/drawlib/_diagrams/flow/_junction.py` | `common/architecture` | Achieves `0` runtime circular dependencies across all 424 modules. |
| **8** | **`P2` (`OPEN`)** | `code_quality` | **Replace Library-Level sys.exit(1) Calls with Typed Exceptions** | `src/drawlib/_core/l1_core/_settings.py`, `src/drawlib/_builder/doc_builder/processor/viewer.py`, `src/drawlib/_cli/_drawlib.py` | `common/library_guidelines` | Prevents unexpected interpreter termination for programmatic Python library callers. |
| **9** | **`P2` (`OPEN`)** | `security` | **Publish SECURITY.md and Configure Dependabot Updates** | `pyproject.toml`, `.github/workflows/quality.yml` | `common/supply_chain` | Closes OpenSSF Scorecard governance gaps for vulnerability disclosure and automated supply-chain maintenance. |
| **10** | **`P2` (`OPEN`)** | `testing` | **Include docs_src/api in Clean-Room Docker Test Context or Guard with pytest.skip** | `tests/drawlib/doc_builder/test_api_docs_completeness.py`, `.dockerignore`, `tools/docker/Dockerfile.test_local` | `python/testing` | Keeps `./dcli docker test` green across both local source and PyPI clean-room modes. |

---

## 3.3 Detailed Engineering Specifications by Priority Tier

### Phase `P0` — Urgent Security Remediation (`COMPLETED`)

#### Action #1 (`[P0]` · `security` · `COMPLETED`): Upgrade locked Pillow dependency to `>=13.0.0` and re-verify raster baselines
- **Target Files**: `pyproject.toml`, `uv.lock`, `.pni/dockerfiles/root/Dockerfile`
- **Related Rules & Advisories**: `common/security_vulnerability`, `CVE-2026-112393`, `CVE-2026-112398`, `CVE-2026-112403`, `CVE-2026-112900`, `CVE-2026-96639`, `GHSA-78g4-xqwv-q3g8`
- **Implemented Remediation**: Upgraded `pillow` in `uv.lock` to `13.0.0` and bumped the runtime lower bound in `pyproject.toml` to `pillow>=13.0.0`. Re-ran Trivy SCA (`trivy_fs.json` / `security_facts.json`) and verified that all **41 application CVEs** (`5 CRITICAL` CVSS 9.8, `23 HIGH`, `13 MEDIUM`) are completely resolved (`app_vuln_counts = 0`).

---

### Phase `P1` — High-Value Hardening, Maintainability & Air-Gapped Testing (`3 COMPLETED`, `2 OPEN`)

#### Action #2 (`[P1]` · `code_quality` · `OPEN`): Decompose High-Complexity DOCX & Fence Parser Routines
- **Target Files**: `src/drawlib/_builder/doc_builder/exporter_docx.py`, `src/drawlib/_builder/doc_builder/processor/options.py`, `src/drawlib/_builder/doc_builder/merger.py`
- **Related Rules**: `common/maintainability`
- **Implementation Guidance**: Refactor `render_chapter` (`cognitive=174`, 283 LOC) and `_render_inline` (`cognitive=102`) in `exporter_docx.py` into per-token dispatch handlers (headings, code fences, callouts, lists, tables). Extract per-attribute validators from `parse_block_info` (`cognitive=106`) in `options.py`, and split TOC assembly, asset path rewriting, and heading normalization out of `build_merged_html` (`cognitive=87`) in `merger.py` so each helper maintains SIG cognitive complexity `<= 15`.
- **Expected Impact**: Substantially lowers maintenance risk, cyclomatic branch density, and isolated unit-testing effort across the HTML and OpenXML `.docx` compilation pipelines.

#### Action #3 & #4 (`[P1]` · `security` · `COMPLETED`): Run Production and Test Docker Images as Non-Root User (`UID 10001`)
- **Target Files**: `tools/docker/Dockerfile.prod`, `tools/docker/Dockerfile.test_local`, `tools/docker/Dockerfile.test_pypi`, `.pni/dockerfiles/root/Dockerfile`
- **Related Rules & Advisories**: `common/security_vulnerability`, `common/supply_chain`, `common/security`, `DS-0002`
- **Implemented Remediation**: Created a dedicated unprivileged `drawlib` user and group (`UID/GID 10001`), configured `/opt/ms-playwright` and `/opt/drawlib-cache` with world-readable/executable permissions (`chmod -R a+rX`), and switched to `USER drawlib` prior to `WORKDIR` / `CMD`. Trivy IaC verification confirmed **0 `DS-0002` findings** across all Dockerfiles.

#### Action #5 (`[P1]` · `testing` · `OPEN`): Bake Chromium shell & asset cache into `.pni/dockerfiles/Dockerfile` and add unit tests for `_pptx_writer.py`
- **Target Files**: `src/drawlib/_slide/_pptx_writer.py`, `src/drawlib/_builder/doc_builder/compiler/pdf.py`, `tests/drawlib/slide/test_pptx.py`
- **Related Rules**: `common/runtime_verification`
- **Implementation Guidance**: Pre-install `chromium-headless-shell` (with OS shared libraries) and pre-populate `drawlib cache download --all` inside `.pni/dockerfiles/Dockerfile`, add a graceful offline skip guard when Chromium binaries are intentionally absent, and add pure-Python unit tests feeding synthetic `PptxSlide` dataclasses directly into `src/drawlib/_slide/_pptx_writer.py` without invoking Playwright.
- **Expected Impact**: Lifts offline `--network=none` test pass rate from `99.5%` (`1,405/1,412`) to **100.0%** while raising `_pptx_writer.py` (`11.1%`) and `_pptx_dom.py` (`58.6%`) coverage above `80%`.

#### Action #6 (`[P1]` · `testing` · `COMPLETED`): Validate asset filename membership in `pkg.files` before network downloads
- **Target Files**: `src/drawlib/_release_assets.py`, `src/drawlib/_icons/png_icons/_base.py`, `tests/drawlib/release_assets/test_release_assets_download.py`
- **Related Rules**: `common/runtime_verification`
- **Implemented Remediation**: Updated `find_package_for_resource_path()` and `find_package_for_icon_path()` in `src/drawlib/_release_assets.py` to check `normalized in pkg.files` before returning a package, and updated `resolve_png_icon_path()` in `src/drawlib/_icons/png_icons/_base.py` to raise `ValueError(f'Icon "{file_name}" not found in "{category}" icon set.')` immediately when no package contains the requested icon path. Verified via unit tests that invalid icon lookups never invoke `download_if_not_exist()`, resolving all **12 offline negative icon test failures**.

---

### Phase `P2` — Architectural, Library & Governance Polish (`OPEN`)

#### Action #7 (`[P2]` · `architecture` · `OPEN`): Eliminate Remaining 2 Intra-Diagram Sibling Import Cycles
- **Target Files**: `src/drawlib/_diagrams/architecture/_edge.py`, `src/drawlib/_diagrams/architecture/_junction.py`, `src/drawlib/_diagrams/flow/_edge.py`, `src/drawlib/_diagrams/flow/_junction.py`
- **Related Rules**: `common/architecture`
- **Implementation Guidance**: Extract a lightweight connectable node/endpoint `Protocol` or base class into `_types.py` within `_diagrams/architecture/` and `_diagrams/flow/`, and guard concrete `_edge <-> _junction` cross-imports behind `if TYPE_CHECKING:` blocks.
- **Expected Impact**: Achieves **0 runtime circular dependencies** across all 424 Python source modules.

#### Action #8 (`[P2]` · `code_quality` · `OPEN`): Replace Library-Level `sys.exit(1)` Calls with Typed Exceptions
- **Target Files**: `src/drawlib/_core/l1_core/_settings.py`, `src/drawlib/_builder/doc_builder/processor/viewer.py`, `src/drawlib/_cli/_drawlib.py`
- **Related Rules**: `common/library_guidelines`
- **Implementation Guidance**: Replace direct `sys.exit(1)` calls in `DrawlibSettings` (`_settings.py:123,297,304,313`) and `viewer.py` (`lines 189,193,245`) with `ValueError` or a typed `DrawlibError` exception, translating those exceptions to exit code `1` exclusively inside `src/drawlib/_cli/_drawlib.py:call_command()`.
- **Expected Impact**: Prevents unexpected host Python interpreter termination when `drawlib` is embedded programmatically inside notebooks, web backends, or automation services.

#### Action #9 (`[P2]` · `security` · `OPEN`): Publish `SECURITY.md` and Configure Dependabot Updates
- **Target Files**: `pyproject.toml`, `.github/workflows/quality.yml`
- **Related Rules**: `common/supply_chain`
- **Implementation Guidance**: Publish a root `SECURITY.md` policy enabling GitHub Private Vulnerability Reporting and documenting supported versions, add `.github/dependabot.yml` covering `pip`/`uv` and `github-actions`, and pin third-party GitHub Actions (`actions/checkout`, `astral-sh/setup-uv`, `actions/setup-python`) to full 40-character commit SHAs.
- **Expected Impact**: Closes OpenSSF Scorecard supply-chain governance gaps for coordinated vulnerability disclosure and automated dependency maintenance.

#### Action #10 (`[P2]` · `testing` · `OPEN`): Include `docs_src/api` in Clean-Room Docker Test Context or Guard with `pytest.skip`
- **Target Files**: `tests/drawlib/doc_builder/test_api_docs_completeness.py`, `.dockerignore`, `tools/docker/Dockerfile.test_local`
- **Related Rules**: `python/testing`
- **Implementation Guidance**: Unignore `docs_src/api/` in `.dockerignore` and copy it into `tools/docker/Dockerfile.test_local` for local source container verification, while adding a `pytest.skip("docs_src/api not present in packaged test environment")` guard in `test_api_docs_completeness.py` when testing standalone PyPI wheels via `Dockerfile.test_pypi`.
- **Expected Impact**: Ensures `./dcli docker test` remains consistently green across both local source and published PyPI clean-room container modes.
