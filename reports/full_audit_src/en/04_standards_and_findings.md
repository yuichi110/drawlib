# 4. Audit Standards, Rule Compliance & Findings

This chapter bridges the executive roadmap to the technical deep-dive chapters by presenting scores across all **8 executed audit dimensions** (weakest-first: `76` to `94`), the **16-rule compliance matrix** (`2 FAIL`, `6 WARN`, `8 PASS`), and the complete **21-location consolidated findings index** (`CRITICAL -> INFO`, deduplicated by `file:line` from 22 raw findings).

```drawlib align=center code=hide file=ch04_audit_steps_and_compliance.png caption="Executed Audit Dimension Scores (Weakest-First) and 16-Rule Compliance Matrix (FAIL -> WARN -> PASS)"
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.icons import phosphor
from drawlib.smartarts import Panel, Table
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=168, height=96)

# 1. Left Zone: Executed Audit Step Score Comparison (Weakest -> Strongest)
left_panel = Panel(
    "Audit Step Scores",
    "Weakest -> Strongest",
    style=Styles.White.patch(shape_line_color=Colors.Gray3, shape_line_width=1.0),
    header_style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.0),
    description_style=Styles.White.patch(text_size=10.0),
    icon=phosphor.chart_bar,
    icon_style=Styles.White,
    header_variant="filled",
    header_height=8.2,
)
left_panel.draw((4.0, 4.5), width=75.0, height=87.0, align="bottom_left")

step_chart = BarChart(
    axis_line_style=Styles.Muted,
    categories=[
        "security_vuln",
        "container_runtime",
        "supply_chain",
        "repo_structure",
        "library_hygiene",
        "python_ast",
        "python_test",
        "cli_guidelines",
    ],
    width=59.5,
    height=73.0,
    orientation="horizontal",
    bar_mode="group",
    bar_width_ratio=0.62,
    bar_r=0.8,
    axis_text_style=Styles.Dark.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=10.0),
    value_format="{:.0f}",
)
step_chart.add_series(
    "Audit Score",
    [76.0, 84.0, 86.0, 89.0, 90.0, 91.0, 93.0, 94.0],
    style=Styles.PrimaryFlat,
)
step_chart.configure_x_axis(min_value=0.0, max_value=110.0, tick_step=25.0)
step_chart.draw(xy=(16.5, 7.5), align="bottom_left")

# 2. Right Zone: 16-Rule Compliance Summary Table (FAIL -> WARN -> PASS)
text(
    (123.0, 91.8),
    "16-Rule Compliance Matrix (2 FAIL · 6 WARN · 8 PASS)",
    style=Styles.DarkBold.patch(text_size=11.5),
)

rule_table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=10.0),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=10.2),
    border_style=Styles.MutedThin,
    has_header=True,
)

rule_table.set_style_cell_evenodd(
    even_color=Colors.Light,
    even_text_style=Styles.Dark.patch(text_size=10.0),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=10.0),
)

# Status badges in Column 0 (rows 1..2 FAIL, 3..8 WARN, 9..16 PASS)
rule_table.set_style_cell(
    background_color=Colors.DangerNeutral,
    text_style=Styles.DangerBold.patch(text_size=10.0),
    rows=[1, 2],
    columns=[0],
)
rule_table.set_style_cell(
    background_color=Colors.WarningNeutral,
    text_style=Styles.DarkBold.patch(text_size=10.0),
    rows=[3, 4, 5, 6, 7, 8],
    columns=[0],
)
rule_table.set_style_cell(
    background_color=Colors.SuccessNeutral,
    text_style=Styles.SuccessBold.patch(text_size=10.0),
    rows=[9, 10, 11, 12, 13, 14, 15, 16],
    columns=[0],
)

# Re-apply header row style AFTER set_style_cell_evenodd
rule_table.set_style_cell_header(
    background_color=Colors.Primary,
    text_style=Styles.WhiteBold.patch(text_size=10.2),
)

rule_table.set_style_border(
    top=Styles.Dark.patch(line_width=1.3),
    top2=Styles.Dark.patch(line_width=1.0),
    bottom=Styles.Dark.patch(line_width=1.3),
    left=Styles.MutedThin,
    left2=Styles.MutedThin,
    right=Styles.MutedThin,
    between_columns=Styles.MutedThin,
    between_rows=Styles.MutedThin,
)

rules_data = [
    ["Status", "Evaluated Rule ID", "Key Diagnostic Gate"],
    ["FAIL", "common/runtime_verification", "19 offline DNS fails"],
    ["FAIL", "common/security_vulnerability", "41 CVEs + root Docker"],
    ["WARN", "common/architecture", "2 sibling diag cycles"],
    ["WARN", "common/library_guidelines", "sys.exit(1) in library"],
    ["WARN", "common/maintainability", "DOCX/fence complexity"],
    ["WARN", "common/security", "5 exec() + root USER"],
    ["WARN", "common/supply_chain", "No SECURITY/Dependabot"],
    ["WARN", "python/dependencies", "uv.lock gitignored"],
    ["PASS", "common/cli_guidelines", "9 subcommands + CI UX"],
    ["PASS", "common/documentation", "Diataxis + 99.3% docs"],
    ["PASS", "common/git_workflow", "Linear main + commits"],
    ["PASS", "common/production_readiness", "60s timeouts + chains"],
    ["PASS", "python/code_quality", "Ruff clean + 0 globals"],
    ["PASS", "python/modern_stack", "PEP 621 + 99.3% imports"],
    ["PASS", "python/testing", "1,293 pixel+unit tests"],
    ["PASS", "python/typing", "100% typed + 0 ignores"],
]

rule_table.draw_flexible(
    xy=(82.0, 88.9),
    column_widths=[11.5, 36.5, 34.0],
    row_heights=[5.2] + [4.95] * 16,
    data=rules_data,
    align="top_left",
)

save()
```

---

## 4.1 Executed Audit Dimensions (`Weakest -> Strongest`)

The `full_audit` workflow (`wf-8093775c`) executed **8 specialized static, architectural, containerized runtime, and supply-chain security audit steps**. Four steps achieved **Grade S (`>= 90`)**, three achieved **Grade A (`84–89`)**, and only `security_vulnerability_audit` scored **76/100 (Grade B)** solely due to the upstream `pillow@12.3.0` lockfile advisories and root container `USER` configuration.

| Rank | Audit Step ID (`action_id`) | Score & Grade | Pass / Warn / Fail | Evaluated Rules | Key Diagnostic Summary |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `security_vulnerability_audit` (`act-15`) | **76/100 (B)** | `0 / 1 / 1` | `common/security_vulnerability`, `common/supply_chain` | Strong first-party security (`0` SQLi/CMDi/XSS, `0` hardcoded source secrets, `permissions: contents: read`, SHA-256 asset verification, `0` OS CVEs); **41 app CVEs** (`5 CRITICAL`, `23 HIGH`, `13 MEDIUM`) come exclusively from `pillow@12.3.0` (fixed in `13.0.0`), and `Dockerfile.{prod,test_local,test_pypi}` run as `root` (`DS-0002`). Five `CWE-94` `exec()` sites power intentional *Illustration as Code* rendering. |
| **2** | `container_runtime_audit` (`act-13`) | **84/100 (A)** | `1 / 0 / 1` | `common/runtime_verification`, `common/production_readiness` | Clean-room build passed (`3.76s`), CLI/library smoke check passed (`2.42s`), and measured coverage reached **86.3% line** (`37,221/43,108`) and **75.5% branch**. Air-gapped `--network=none` testing passed **1,393/1,412** executed tests (`98.7%`, `8` skipped), exposing `12` invalid-icon tests calling HTTPS without checking `pkg.files`, `1` uncached CJK font test, and `6` PPTX tests attempting runtime Chromium downloads. |
| **3** | `supply_chain_audit` (`act-10`) | **86/100 (A)** | `1 / 2 / 0` | `common/supply_chain`, `common/security`, `common/git_workflow` | SHA-256 verified GitHub Release asset downloads (`timeout=60` in `_package.py`), `permissions: contents: read` across all 4 workflows, zero hardcoded secrets, and gitignored credential files; deductions for missing non-root `USER` in `Dockerfile.prod`, mutable `@v4`/`@v5` GitHub Action tags, and missing `SECURITY.md` / Dependabot. |
| **4** | `repo_structure_audit` (`act-02`) | **89/100 (A)** | `3 / 2 / 0` | `common/supply_chain`, `common/documentation`, `common/git_workflow`, `common/security`, `python/dependencies` | Exemplary PEP 621 `pyproject.toml` with 13 SemVer-bounded runtime dependencies, isolated `[dependency-groups].dev`, PEP 561 `py.typed`, least-privilege CI workflows, and full Diataxis documentation (`README.md`, `docs/`, `docs/api/`, `docs/architecture/`); minor governance gaps around `SECURITY.md`, Dependabot, and gitignored `uv.lock`. |
| **5** | `library_hygiene_audit` (`act-08`) | **90/100 (S)** | `1 / 2 / 0` | `common/library_guidelines`, `common/documentation`, `common/maintainability` | PEP 562 lazy submodule loading in `src/drawlib/__init__.py` (zero import-time heavy/network side effects), curated `__all__` across 20 public facades, `py.typed`, flexible `>=` SemVer bounds, and 100% API docs completeness; minor coupling where `_settings.py` and `viewer.py` call `sys.exit(1)` directly plus `30` `print()` calls and `9` direct `os.environ` reads in `_builder/`. |
| **6** | `python_ast_audit` (`act-04`) | **91/100 (S)** | `3 / 4 / 0` | `common/architecture`, `common/maintainability`, `common/security`, `common/security_vulnerability`, `python/code_quality`, `python/typing`, `python/modern_stack` | Across 424 files (`85,323` LOC, `300` classes, `1,958` functions): **100.0% type coverage**, `0` unscoped `# type: ignore`, **99.3% docstrings**, **99.3% import hygiene**, `0` undeclared deps, `0` missing I/O timeouts, and `0` mutable globals. Acyclic core layering with only `2` sibling `_edge <-> _junction` cycles and localized DOCX/HTML parser complexity. |
| **7** | `python_test_audit` (`act-11`) | **93/100 (S)** | `1 / 0 / 0` | `python/testing` | `150` test files and `1,293` test functions achieving **100.0% module mirror coverage**, `0` assertion-free tests, automatic `Canvas` state reset, and pixel-by-pixel PNG regression hooks in `tests/conftest.py`; minor clean-room drift in `test_api_docs_completeness.py` when `docs_src/api/` is excluded by `.dockerignore`. |
| **8** | `cli_guidelines_audit` (`act-09`) | **94/100 (S)** | `2 / 0 / 0` | `common/cli_guidelines`, `common/documentation` | Exemplary Typer + Rich CLI (`src/drawlib/_cli/_drawlib.py`) featuring `-h`/`--help` with `HELP_EPILOG`, `no_args_is_help=True`, eager `-v`/`--version`, validated `--quiet`/`--verbose`/`--debug`/`--developer` flags, headless automation modes (`serve --check`, `show -o -g`, `cache download --all`), and `211` CLI tests. |

---

## 4.2 Complete 16-Rule Compliance Matrix (`FAIL -> WARN -> PASS`)

Overall rule compliance stands at **8/16 rules passed (`50.0%` strict pass, `87.5%` pass-or-warn)**, with **2 `FAIL`**, **6 `WARN`**, and **8 `PASS`** evaluations preserved in exact severity order below.

| # | Status | Rule ID | Source Audit | Concise Assessment | Full Quantitative & Diagnostic Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **`FAIL`** | `common/runtime_verification` | `container_runtime_audit` | Clean build, startup smoke check, and 86.3%/75.5% coverage pass; `--network=none` exposed 19 tests relying on live HTTPS downloads. | `RV-01` `harness_build=passed` (`3.76s`, `.pni/dockerfiles/Dockerfile`); `RV-04` `smoke_check=passed` (`2.42s`, `drawlib --help` exited `0` and `import drawlib` succeeded); `RV-03` `coverage=86.3%` line (`37,221/43,108`) and `75.5%` branch (lowest non-generated: `__main__.py` `0.0%`, `_pptx_writer.py` `11.1%`, `_icons/__init__.py` `33.3%`, `compiler/pdf.py` `52.2%`, `_pptx_dom.py` `58.6%`); `RV-02` `test_execution=failed` under `--network=none` (`1,393` passed, `19` failed, `8` skipped: `13` GitHub Release asset DNS failures + `6` Playwright CDN DNS failures). |
| **2** | **`FAIL`** | `common/security_vulnerability` | `security_vulnerability_audit` | Zero first-party injection/crypto flaws, but `uv.lock` pins `pillow@12.3.0` (41 CVEs fixed in `13.0.0`) and Dockerfiles omit non-root `USER`. | `SEC-01`: `app_vuln_counts={critical:5, high:23, medium:13, low:0, total:41}` all in `pillow@12.3.0` (`uv.lock`, `fixed_version=13.0.0`: `CVE-2026-112393`, `CVE-2026-112398`, `CVE-2026-112403`, `CVE-2026-112900`, `CVE-2026-96639`, `GHSA-78g4-xqwv-q3g8`, etc.), `os_vuln_counts={total:0}`, `0` CVEs in the other 12 direct packages; `SEC-02`: `3 HIGH DS-0002` missing non-root `USER` in `tools/docker/Dockerfile.{prod,test_local,test_pypi}`; `SEC-03`: `0` hardcoded source secrets, `1` gitignored/dockerignored local `.env` PyPI token (redacted); `SEC-04`: `0` CWE-89/78/79/502, `5` intentional `CWE-94` `exec()` sites (`styles_loader.py:78,158`, `processor.py:121,123`, `_image_code.py:54`); `SEC-05/SEC-06`: N/A (`api_endpoints=[]`). |
| **3** | **`WARN`** | `common/architecture` | `act-04` | Core engine and public facade layers are strictly acyclic; only 2 minor intra-package `_edge <-> _junction` cycles remain inside `_diagrams`. | Strict downward core layering (`l1_core -> l2_types -> l3_* -> l4_canvas -> domains -> facades`) with `0` cross-layer or facade runtime cycles and `40` properly guarded `TYPE_CHECKING` imports; `2` intra-package sibling runtime cycles remain in `drawlib._diagrams.architecture` (`_edge` <-> `_junction`) and `drawlib._diagrams.flow` (`_edge` <-> `_junction`). |
| **4** | **`WARN`** | `common/library_guidelines` | `act-08` | Exemplary PEP 562 lazy import purity, explicit `__all__`, `py.typed`, and `>=` SemVer bounds; minor deduction for `sys.exit(1)` and `print()` in library/builder code. | PEP 562 lazy `__getattr__` in `src/drawlib/__init__.py`, explicit `__all__` on public facades, `py.typed=True`, and `>=` SemVer lower bounds on all 13 dependencies; however `sys.exit(1)` appears in `src/drawlib/_core/l1_core/_settings.py:123,297,304,313` and `src/drawlib/_builder/doc_builder/processor/viewer.py:189,193,245`, plus `unstructured_logging=30` `print()` calls in `_builder/`. |
| **5** | **`WARN`** | `common/maintainability` | `act-04` | Zero shared mutable global state and cohesive domain packages, with localized cognitive-complexity hotspots in DOCX/HTML AST walkers. | `global_state_usages=0` across 424 files; `complex_functions=399` peaking in `exporter_docx.py:565` `render_chapter` (`cognitive=174`, `283` LOC), `options.py:93` `parse_block_info` (`cognitive=106`), and `merger.py:142` `build_merged_html` (`cognitive=87`); `excessive_parameters=330` (keyword styling/compiler APIs) and `scattered_env_access=9` across `_builder/_common/{browser.py,cache.py,office.py}` and `exporter_pdf.py`. |
| **6** | **`WARN`** | `common/security` | `act-04` | Zero hardcoded secrets, zero SQL/shell injection sinks, and explicit HTTP timeouts; local `exec()` requires trusted inputs and `Dockerfile.prod` lacks non-root `USER`. | All 4 CI workflows enforce `permissions: contents: read`; `.gitignore` excludes `.env` (`git ls-files .env` is empty); `hardcoded_secrets=[]`, `missing_io_timeouts=[]`, SQL/shell injection idioms=`0`, and Pydantic `@validate_call` guards public API boundaries; `5` intentional `exec()` calls render author Python blocks, and `tools/docker/Dockerfile.prod` lacks a non-root `USER`. |
| **7** | **`WARN`** | `common/supply_chain` | `act-02` | Explicit `LICENSE`, default-deny `.dockerignore`, and least-privilege CI permissions present, while `SECURITY.md`, Dependabot, and SHA action pins are missing. | `LICENSE=True`, `ci_supply_chain_issues=[]`, `unpinned_dependencies=[]`, `ci_workflows_found=4` (all `permissions: contents: read`), default-deny `.dockerignore` present; however `SECURITY.md=False`, `dependency_automation=False` (`.github/dependabot.yml` missing), `tools/docker/Dockerfile.prod` omits non-root `USER`, and `.github/workflows/*.yml` use major tags (`@v4`, `@v5`). |
| **8** | **`WARN`** | `python/dependencies` | `act-02` | PEP 621 metadata, explicit runtime bounds, and dev group separation are exemplary; `uv.lock` exists locally but is gitignored by library policy. | `pyproject.toml` uses PEP 621 with 13 SemVer-bounded runtime dependencies (`unpinned_dependencies=[]`) and `[dependency-groups].dev`; `uv.lock` exists locally for reproducible builds while `.gitignore` (`line 182`) excludes `uv.lock` to allow cross-version Python 3.11–3.13 CI resolution. |
| **9** | **`PASS`** | `common/cli_guidelines` | `act-09` | Comprehensive CLI UX with `-h`/`--help`, `-v`/`--version`, structured verbosity flags, actionable validation errors, and headless CI/AI-agent flags. | `src/drawlib/_cli/_drawlib.py` configures `help_option_names=['-h', '--help']`, `no_args_is_help=True`, eager `-v`/`--version` callback, mutually validated `--quiet`/`--verbose`/`--debug`/`--developer` flags, and non-interactive automation flags across all 9 subcommands (`build`, `show`, `init`, `serve`, `cache`, `rules`, `styles`, `colors`, `css`). |
| **10** | **`PASS`** | `common/documentation` | `act-02` | Exceeds Standard Readme and Diataxis documentation standards with a multi-site dogfooded documentation ecosystem and 99.3% docstrings. | `has_readme=True` (`218` lines, `14` headings), `docs_inventory=['README.md', 'docs/README.md', 'docs/api/README.md', 'docs/architecture/README.md']`, `99.3%` docstring coverage, embedded `drawlib rules show` manuals, and automated `test_api_docs_completeness.py` enforcing 100% public symbol documentation. |
| **11** | **`PASS`** | `common/git_workflow` | `act-02` | Clean trunk-based Git history on `main` with atomic Conventional Commits and zero stale branches or conflict markers. | Linear trunk-based history on `main` with `0` stale branches, `0` conflict markers, `>85%` Conventional Commits compliance (`feat:`, `docs:`, `refactor:`, `ci:`), and `pull_request` + `push` quality gates in `.github/workflows/quality.yml`. |
| **12** | **`PASS`** | `common/production_readiness` | `container_runtime_audit` | Outbound HTTP timeouts and causal error propagation meet production readiness standards for CLI and library execution. | `runtime_types=['cli', 'library']`; `AstFacts.missing_io_timeouts=0` (`urllib.request.urlopen` in `_package.py:165` sets `timeout=60`); `0` silent `try-except-pass` blocks; causal exception chaining (`raise RuntimeError(...) from err`) preserved across `_package.py` and `browser.py`. |
| **13** | **`PASS`** | `python/code_quality` | `act-04` | 99.3% Google-style docstring coverage, strict PEP 8 / Ruff enforcement, zero global state, and zero silent exception swallowing. | `docstring_coverage_pct=99.3%` (`missing_docstrings=12` fluent builder methods, `empty_docstrings=0`), Ruff lint/format clean across `src/`, `tests/`, and `tools/`, `global_state_usages=0`. |
| **14** | **`PASS`** | `python/modern_stack` | `act-04` | Modern Python 3.11+ stack (Pydantic v2, Typer, PEP 621) with 99.3% import hygiene and zero undeclared runtime dependencies. | `import_hygiene_coverage_pct=99.3%`, `wildcard_imports=[]`, `undeclared_dependencies=[]`, `framework_issues=[]`, Pydantic v2 + Typer + PEP 621 `pyproject.toml` (`unused_dependencies=['python_docx']` is a benign package-vs-import alias for `import docx`). |
| **15** | **`PASS`** | `python/testing` | `act-11` | 100.0% module test coverage with 1,293 tests combining structural assertions and automated pixel-accuracy regression baselines. | `150` test files and `1,293` test functions mirroring `src/drawlib/` (`module_test_coverage_pct=100.0%`, `assertion_free_tests=[]`), autouse `preprocess()` Canvas reset + `pytest_runtest_call` pixel-match hook in `tests/conftest.py`, and cross-OS Python 3.11–3.13 CI matrix. |
| **16** | **`PASS`** | `python/typing` | `act-04` | 100.0% callable type-annotation coverage with zero unscoped `type: ignore` comments and clean static + runtime type verification. | `type_safety_coverage_pct=100.0%` across `1,958` functions, `unscoped_type_ignores=[]`, `0` `ty` static type errors, plus runtime `@validate_call` boundary validation. |

---

## 4.3 Consolidated Location Findings Index (`CRITICAL -> INFO`)

Across all static AST, governance, Trivy SCA/IaC/secret, and air-gapped container runtime checks, **22 raw findings** (`1 CRITICAL`, `2 HIGH`, `6 MEDIUM`, `9 LOW`, `4 INFO`) consolidated into **21 unique `file:line` locations** (`1 CRITICAL`, `2 HIGH`, `6 MEDIUM`, `8 LOW`, `4 INFO`, merging two `pyproject.toml:1` supply-chain findings into a single row).

```drawlib align=center code=hide file=ch04_consolidated_findings_overview.png caption="Consolidated Findings Severity Distribution and Top Priority Hotspots (#1–#9 CRITICAL -> MEDIUM)"
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.icons import phosphor
from drawlib.smartarts import KpiCards, Panel, Table
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=168, height=94)

# 1. Left Zone: Consolidated Severity Distribution + Summary KPIs
sev_panel = Panel(
    "Severity Summary (21 Total)",
    style=Styles.White.patch(shape_line_color=Colors.Gray3, shape_line_width=1.0),
    header_style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.0),
    icon=phosphor.funnel,
    icon_style=Styles.White,
    header_variant="filled",
    header_height=8.2,
)
sev_panel.draw((4.0, 5.0), width=52.0, height=84.0, align="bottom_left")

sev_chart = BarChart(
    axis_line_style=Styles.Muted,
    categories=["CRIT", "HIGH", "MED", "LOW", "INFO"],
    width=46.0,
    height=46.0,
    orientation="vertical",
    bar_mode="group",
    bar_width_ratio=0.58,
    bar_r=0.8,
    title="Locations by Severity",
    title_style=Styles.DarkBold.patch(text_size=11.0),
    axis_text_style=Styles.Dark.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=10.5),
    value_format="{:.0f}",
)
sev_chart.add_series("Locations", [1.0, 2.0, 6.0, 8.0, 4.0], style=Styles.PrimaryFlat)
sev_chart.configure_y_axis(min_value=0.0, max_value=10.0, tick_step=2.0)
sev_chart.draw(xy=(7.0, 31.5), align="bottom_left")

sev_kpis = KpiCards(
    style=Styles.Neutral,
    metric_style=Styles.DarkBold.patch(text_size=12.5),
    text_style=Styles.DarkBold.patch(text_size=10.2),
    description_style=Styles.Muted.patch(text_size=10.0),
    accent_style=Styles.DangerFlat,
    accent_position="left_pill",
    metric_layout="left_column",
    metric_width_ratio=0.28,
    spacing=2.4,
)
sev_kpis.add(
    "9",
    "CRIT / HIGH / MED",
    "Top hotspots (#1–#9)",
    style=Styles.PrimaryNeutral,
    metric_style=Styles.DangerBold.patch(text_size=13.0),
    accent_style=Styles.DangerFlat,
)
sev_kpis.add(
    "12",
    "LOW & INFO Polish",
    "8 LOW + 4 INFO (#10–#21)",
    style=Styles.Neutral,
    metric_style=Styles.DarkBold.patch(text_size=13.0),
    accent_style=Styles.SecondaryFlat,
)
sev_kpis.draw(xy=(7.0, 7.5), width=46.0, height=21.0, columns=1, align="bottom_left")

# 2. Right Zone: Top Consolidated Hotspots Table (#1-#9 + #10-#21 Rollup)
text(
    (111.5, 89.2),
    "Priority Consolidated Hotspots (#1–#9 CRIT -> MED + #10–#21 Rollup)",
    style=Styles.DarkBold.patch(text_size=11.0),
)

hotspot_table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=10.0),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=10.2),
    border_style=Styles.MutedThin,
    has_header=True,
)

hotspot_table.set_style_cell_evenodd(
    even_color=Colors.Light,
    even_text_style=Styles.Dark.patch(text_size=10.0),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=10.0),
)

# Severity badges on Column 0
hotspot_table.set_style_cell(
    background_color=Colors.Danger,
    text_style=Styles.WhiteBold.patch(text_size=10.0),
    rows=[1],
    columns=[0],
)
hotspot_table.set_style_cell(
    background_color=Colors.DangerNeutral,
    text_style=Styles.DangerBold.patch(text_size=10.0),
    rows=[2, 3],
    columns=[0],
)
hotspot_table.set_style_cell(
    background_color=Colors.WarningNeutral,
    text_style=Styles.DarkBold.patch(text_size=10.0),
    rows=[4, 5, 6, 7, 8, 9],
    columns=[0],
)
hotspot_table.set_style_cell(
    background_color=Colors.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.0),
    rows=[10],
    columns=[0],
)

# Re-apply header row style AFTER set_style_cell_evenodd
hotspot_table.set_style_cell_header(
    background_color=Colors.Primary,
    text_style=Styles.WhiteBold.patch(text_size=10.2),
)

hotspot_table.set_style_border(
    top=Styles.Dark.patch(line_width=1.3),
    top2=Styles.Dark.patch(line_width=1.0),
    bottom=Styles.Dark.patch(line_width=1.3),
    left=Styles.MutedThin,
    left2=Styles.MutedThin,
    right=Styles.MutedThin,
    between_columns=Styles.MutedThin,
    between_rows=Styles.MutedThin,
)

hotspot_rows = [
    ["Sev · #", "Consolidated file:line", "Rule Tag", "Primary Fix"],
    ["CRIT #1", "uv.lock:1\n(pillow@12.3.0)", "security_\nvulnerability", "Upgrade pillow >=13.0.0\n(clears all 41 CVEs)"],
    ["HIGH #2", "_core/l3_external/\n_download.py:94", "runtime_\nverification", "Check pkg.files before\nHTTPS archive download"],
    ["HIGH #3", "tools/docker/\nDockerfile.prod:1", "security_\nvulnerability", "Add non-root USER\ndrawlib (UID 10001)"],
    ["MED #4", "pyproject.toml:1\n(governance)", "common/\nsupply_chain", "Publish SECURITY.md,\nDependabot & PyPI OIDC"],
    ["MED #5", "_builder/_common/\nbrowser.py:247", "runtime_\nverification", "Pre-bake Chromium shell\nin PNI Docker harness"],
    ["MED #6", "doc_builder/\nexporter_docx.py:884", "common/\nmaintainability", "Split render_chapter &\n_render_inline handlers"],
    ["MED #7", "processor/\noptions.py:93", "common/\nmaintainability", "Extract fence validators\n& HTML merge helpers"],
    ["MED #8", "processor/\nprocessor.py:121", "security_\nvulnerability", "Document CWE-94 exec()\ncontainer trust model"],
    ["MED #9", "tools/docker/\nDockerfile.prod:42", "common/\nsupply_chain", "Switch to USER drawlib\n+ /opt/ms-playwright"],
    ["LOW/INF\n#10–#21", "12 locations (8 LOW,\n4 INFO — table below)", "supply_chain, arch,\nlib, testing, cli", "SHA pins, timeouts,\nsys.exit, 0 cycles, docs"],
]

hotspot_table.draw_flexible(
    xy=(59.0, 86.2),
    column_widths=[14.5, 34.5, 25.0, 31.0],
    row_heights=[6.8] + [7.4] * 10,
    data=hotspot_rows,
    align="top_left",
)

save()
```

### Complete 21-Row Consolidated Location Findings Evidence Table (`CRITICAL -> INFO`)

Every unique `file:line` location is listed exactly once below in pre-sorted severity order (`CRITICAL -> HIGH -> MEDIUM -> LOW -> INFO`), preserving all rule tags, raw scanner/AST/runtime evidence, and remediation steps.

| # | Severity | Consolidated Location (`file:line`) | Symbol | Rule Tags | Verbatim Diagnostic Evidence | Recommended Fix |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **`CRITICAL`** | `uv.lock:1` | `pillow@12.3.0` | `common/security_vulnerability` | Trivy SCA (`SEC-01`) reported 41 application CVEs in `pillow@12.3.0` (`5 CRITICAL` CVSS 9.8: `CVE-2026-112393`, `CVE-2026-112398`, `CVE-2026-112403`, `CVE-2026-112900`, `CVE-2026-96639`; `23 HIGH` including `CVE-2026-96778` and `GHSA-78g4-xqwv-q3g8`; `13 MEDIUM`), all fixed in `pillow 13.0.0`. | Run `uv lock --upgrade-package pillow` to resolve `pillow>=13.0.0` (updating `pyproject.toml` lower bound to `pillow>=13.0.0` once Python 3.11–3.13 wheel compatibility and pixel-exact test baselines are verified). |
| **2** | **`HIGH`** | `src/drawlib/_core/l3_external/_download.py:94` | `download_if_not_exist` | `common/runtime_verification` | `12` `test_nonexistent_*_icon_error` tests failed under `--network=none` with `RuntimeError: Failed to download asset package ... <urlopen error [Errno -3] Temporary failure in name resolution>` because `find_package_for_icon_path()` matches directory prefixes without checking `pkg.files` and `download_if_not_exist()` unconditionally calls `pkg.download_and_extract()`. | Check whether the requested relative filename exists in `pkg.files` before attempting network I/O (raising `FileNotFoundError` immediately for nonexistent asset names), check `pkg.is_downloaded()` before re-downloading, and pre-seed external assets in `.pni/dockerfiles/Dockerfile`. |
| **3** | **`HIGH`** | `tools/docker/Dockerfile.prod:1` | `Dockerfile.prod` | `common/security_vulnerability` | Trivy `DS-0002` (`HIGH`) on `tools/docker/Dockerfile.prod`, `tools/docker/Dockerfile.test_local`, and `tools/docker/Dockerfile.test_pypi`: *Specify at least 1 USER command in Dockerfile with non-root user as argument*. | Create a dedicated unprivileged user (e.g., `useradd --uid 10001 --create-home drawlib`) and switch to `USER drawlib` before `ENTRYPOINT`/`CMD` in `tools/docker/Dockerfile.prod` and test Dockerfiles. |
| **4** | **`MEDIUM`** | `pyproject.toml:1` | `supply_chain_governance` | `common/supply_chain` | `ProjectFacts`: `SECURITY.md=False`, `dependency_automation=False`; Trivy `SEC-03` also detected a local untracked/gitignored `.env` file containing a redacted `pypi-upload-token` (`PYPI_TOKEN=***`). `ProjectFacts.has_security_policy == False` (no `SECURITY.md` at repository root). | Add `SECURITY.md` (covering supported versions, GitHub Private Vulnerability Reporting, and the `exec()` trust boundary), add `.github/dependabot.yml` for `pip`/`uv` and `github-actions`, and migrate PyPI publishing to GitHub Actions OIDC Trusted Publishing or OS keyring. |
| **5** | **`MEDIUM`** | `src/drawlib/_builder/_common/browser.py:247` | `launch_headless_chromium` | `common/runtime_verification` | `6` PPTX export tests (`tests/drawlib/cli/test_cli_build.py::test_cli_build_pptx` and `5` tests in `tests/drawlib/slide/test_pptx.py`) failed under `--network=none` with `EAI_AGAIN` resolving `cdn.playwright.dev` when `chromium-headless-shell` was not pre-installed in `.pni/dockerfiles/Dockerfile`. | Pre-install `chromium-headless-shell` and OS dependencies in `.pni/dockerfiles/Dockerfile` for full offline PPTX/PDF coverage, and guard browser integration tests with a clear skip/fixture check when running offline without local Chromium binaries. |
| **6** | **`MEDIUM`** | `src/drawlib/_builder/doc_builder/exporter_docx.py:884` | `export_chapters_to_docx` | `common/maintainability` | `exporter_docx.py` (`945` LOC) contains top cognitive-complexity routines `render_chapter` (`line 565`, `cognitive=174`, `283` lines), `_render_inline` (`line 301`, `cognitive=102`), and `export_chapters_to_docx` (`line 884`, `cognitive=46`, `202` lines). | Decompose `render_chapter` and `_render_inline` into per-token handler functions (heading, code fence, callout, list, table) dispatched via a token-type table. |
| **7** | **`MEDIUM`** | `src/drawlib/_builder/doc_builder/processor/options.py:93` | `parse_block_info` | `common/maintainability` | `parse_block_info` (`length=74` lines, `branches=33`, `cognitive=106`) and `merger.py:142` `build_merged_html` (`length=260` lines, `branches=40`, `cognitive=87`) exceed SIG cognitive complexity `<= 15`. | Extract per-attribute validators from `parse_block_info` and split TOC assembly, asset rewriting, and heading normalization out of `build_merged_html`. |
| **8** | **`MEDIUM`** | `src/drawlib/_builder/doc_builder/processor/processor.py:121` | `exec` | `common/security_vulnerability` | `5` `CWE-94` `exec()` call sites: `src/drawlib/_builder/_common/styles_loader.py:78,158`, `src/drawlib/_builder/doc_builder/processor/processor.py:121,123`, and `src/drawlib/_core/l4_canvas/_image_code.py:54`. | Document the code-execution trust model prominently in `SECURITY.md` and `README.md`, recommending isolated non-root containers (`--network=none`) whenever rendering untrusted Markdown or diagram sources. |
| **9** | **`MEDIUM`** | `tools/docker/Dockerfile.prod:42` | `Dockerfile.prod` | `common/supply_chain` | `tools/docker/Dockerfile.prod` (`lines 1–44`) installs `drawlib` into `python:3.12-slim` and sets `WORKDIR /workspace` without creating or switching to a non-root `USER`. | Create a dedicated unprivileged user (e.g., `groupadd`/`useradd -u 10001 drawlib`), set `PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright` with world-readable permissions, and switch to `USER drawlib` before `WORKDIR /workspace`. |
| **10** | **`LOW`** | `.github/workflows/quality.yml:1` | `quality.yml` | `common/supply_chain` | `ProjectFacts.has_dependency_automation == False` (no `.github/dependabot.yml` or `renovate.json` found). | Add `.github/dependabot.yml` covering `pip`/`uv` and `github-actions` ecosystems on a weekly or monthly schedule. |
| **11** | **`LOW`** | `.github/workflows/quality.yml:20` | `quality.yml` | `common/supply_chain` | `uses: actions/checkout@v4` (`line 20`), `astral-sh/setup-uv@v5` (`line 23`), and `actions/setup-python@v5` (`line 28`) across `.github/workflows/*.yml`. | Pin third-party GitHub Actions (especially `astral-sh/setup-uv`) to full 40-character commit SHAs with version comments and keep them updated via Dependabot. |
| **12** | **`LOW`** | `src/drawlib/_builder/_common/browser.py:210` | `install_headless_chromium` | `common/production_readiness` | `subprocess.run([str(exec_path), str(cli_path), *_INSTALL_ARGS], ...)` at `browser.py:210` omits an explicit `timeout=...` argument. | Pass an explicit timeout (e.g., `timeout=300`) to `subprocess.run()` in `install_headless_chromium()` and translate `subprocess.TimeoutExpired` into an actionable `RuntimeError`. |
| **13** | **`LOW`** | `src/drawlib/_core/l1_core/_settings.py:123` | `DrawlibSettings` | `common/library_guidelines` | `sys.exit(1)` called directly in `src/drawlib/_core/l1_core/_settings.py` (`lines 123, 297, 304, 313`) and `src/drawlib/_builder/doc_builder/processor/viewer.py` (`lines 189, 193, 245`). | Raise `ValueError` or a dedicated `DrawlibError` subclass in `_settings.py` and `viewer.py`, and translate those exceptions to exit code `1` solely in `_cli/_drawlib.py:call_command`. |
| **14** | **`LOW`** | `src/drawlib/_core/l4_canvas/_image_code.py:54` | `get_dimage_from_code` | `common/security_vulnerability` | `5` `CWE-94` `exec()` call sites: `styles_loader.py:78,158`, `processor.py:121,123`, and `_image_code.py:54`. | Preserve `exec()` for local *Illustration as Code* authoring, and explicitly document in security docs/CLI help that `drawlib build`/`show` must only be run on trusted Markdown and Python sources (or inside an isolated `--network=none` container for untrusted inputs). |
| **15** | **`LOW`** | `src/drawlib/_diagrams/architecture/_edge.py:1` | `Edge` | `common/architecture` | `AstFacts.circular_dependencies` = `[['drawlib._diagrams.architecture._edge', 'drawlib._diagrams.architecture._junction', 'drawlib._diagrams.architecture._edge'], ['drawlib._diagrams.flow._edge', 'drawlib._diagrams.flow._junction', 'drawlib._diagrams.flow._edge']]`. | Move runtime cross-type checks to a shared `_types.py` protocol/base class and guard concrete sibling imports under `if TYPE_CHECKING:`. |
| **16** | **`LOW`** | `src/drawlib/_slide/_pptx_writer.py:81` | `write_pptx` | `common/runtime_verification` | Lowest covered non-generated modules: `src/drawlib/__main__.py` (`0.0%`, `lines 12–23`), `src/drawlib/_slide/_pptx_writer.py` (`11.1%` line / `0.0%` branch, `lines 81–90`), `src/drawlib/_icons/__init__.py` (`33.3%`, `lines 99–109`), `src/drawlib/_builder/doc_builder/compiler/pdf.py` (`52.2%` line / `38.9%` branch, `lines 51, 97–115`), and `src/drawlib/_slide/_pptx_dom.py` (`58.6%` line / `4.0%` branch, `lines 989–1011`). | Add direct unit tests for `_pptx_writer.py` OpenXML shape/table generation using synthetic `PptxSlide` DOM fixtures (decoupled from Playwright) plus lightweight CLI `__main__` and icon `__getattr__` error-path tests. |
| **17** | **`LOW`** | `tests/drawlib/doc_builder/test_api_docs_completeness.py:31` | `test_python_public_api_100_percent_documented` | `python/testing` | `test_api_docs_completeness.py:31` reads `REPO_ROOT / 'docs_src' / 'api'`, whereas root `.dockerignore` ignores `docs_src/` and `tools/docker/Dockerfile.test_local:27` runs `rm -rf ./src ./docs_src`. | Unignore `docs_src/api/` in `.dockerignore` + `COPY docs_src/api/` in `Dockerfile.test_local`, or call `pytest.skip('docs_src/api not present in packaged test environment')` when `API_DOCS_DIR` is absent. |
| **18** | **`INFO`** | `.gitignore:182` | `uv.lock` | `python/dependencies` | `.gitignore` excludes `uv.lock` even though `uv.lock` is generated locally (`lockfiles_found=['uv.lock']`). | Document the intentional library lockfile policy in contributor docs or commit `uv.lock` while running separate `--resolution=lowest-direct` / matrix checks in CI. |
| **19** | **`INFO`** | `src/drawlib/_builder/_common/browser.py:40` | `launch_headless_chromium` | `common/library_guidelines` | `scattered_env_access=9` across `browser.py:40,45,48`, `cache.py:516,518`, `office.py:40`, `exporter_pdf.py:31`, `viewer.py:161`, and `rules_builder.py:174`; `unstructured_logging=30` `print()` calls in `_builder/`. | Centralize `DRAWLIB_*` environment resolution in a typed builder config helper and route non-CLI diagnostic output through `drawlib`'s logger. |
| **20** | **`INFO`** | `src/drawlib/_cli/_drawlib.py:38` | `main_callback` | `common/cli_guidelines` | `typer.Typer(..., add_completion=False)` in `src/drawlib/_cli/_drawlib.py:38` and progress `print()` statements in `src/drawlib/_builder/_common/progress.py:138` writing to `stdout`. | Consider enabling optional shell completion or routing human progress messages to `stderr` if future subcommands emit machine-parseable JSON to `stdout`. |
| **21** | **`INFO`** | `src/drawlib/_smartarts/_mindmap.py:93` | `MindMapNode` | `python/code_quality` | `missing_docstrings=12` across fluent setter methods on `MindMapNode` (`_mindmap.py:93–156`), `TreeNode` (`_tree.py:86`), and `BulletPoints` (`_bulletpoints.py:48`). | Add concise Google-style one-line docstrings to fluent builder methods in `_mindmap.py`, `_tree.py`, and `_bulletpoints.py` to reach `100.0%` docstring coverage. |
