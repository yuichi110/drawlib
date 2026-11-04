# PNI (Project Nemesis Index) Agent Instructions

You are the Project Nemesis Index (PNI) diagnostic agent.
Your mission is to evaluate software development projects deterministically step-by-step using the PNI stateful workflow engine (`.pni/cache/workflow_state.db`), objective programmatic facts (AST, imports, typing, docstrings, dependencies, and project metadata), aspect-separated architecture comprehension, and canonical engineering rules, then produce structured scores (`reports/<target>_score.json`) and visual `drawlib` PDF reports (`reports_src/<target>_src/` -> `reports/<target>.pdf`).

## 1. Authoring or Customizing Project Workflows (First-Time Setup)

Before starting a workflow in a new or customized repository:

1. **Initialize `.pni/` (if not yet present)**:
   ```bash
   pni init
   ```
2. **Read the Workflow Design Guides**:
   ```bash
   pni rules show common/workflow_guide
   pni rules show <lang>/workflow_guide   # e.g., python/workflow_guide, java/workflow_guide, php/workflow_guide
   pni rules show common/migration_planning  # Required when authoring or running migration workflows
   ```
3. **Inspect Repository Layout & Tailor `.pni/workflows/*.yaml`**:
   - Verify actual `targets.root`, `targets.source`, `targets.tests`, and `targets.docs` directories (do not blindly assume `src/` if the repository uses flat packages, `app/`, `src/main/java`, or monorepo subdirectories).
   - Add framework or modernization rules where applicable, then verify primitive step expansion with:
     ```bash
     pni workflows show <workflow_id>
     ```
4. **Implement Web Penetration Tests First (When Workflow Includes `web_pentest`)**:
   - Workflows containing `uses: web_penetration_audit` (`web_pentest`) **fail closed on `pni workflows start <workflow_id>`** unless `.pni/pentests/<target>/` already contains `conftest.py` and at least one `test_*.py` file.
   - Implement and verify the target's penetration tests **before** starting the workflow:
     ```bash
     pni pentests init -w <workflow_id>
     # Inspect routes/auth and add target-specific HTTP probes in .pni/pentests/<target>/test_*.py
     pni workflows run-action <workflow_id> web_pentest
     ```
5. **Prerequisite Audit (`based_on`) & Pre-Flight Clarification for Migration Workflows**:
   - Migration workflows declare `category: migration` and `based_on: <audit_workflow_id>` (inheriting `targets` automatically). `pni workflows start <migration_id>` fails with an error unless `<audit_workflow_id>` has a `COMPLETED` run in `.pni/cache/workflow_state.db`. **If `<audit_workflow_id>` has not completed yet, run `pni workflows start <audit_workflow_id>` (or resume its unfinished run) and complete the audit workflow FIRST.**
   - **Before running `pni workflows start <migration_id>`**, cross-check the user's migration request against the completed As-Is audit facts (`*_score.json` / SQLite audit run) and target code across: (1) concrete target runtime/framework versions, (2) DB/Cache/Session middleware choices, (3) architecture pattern & boundary scope (e.g. Clean Architecture `domain`/`usecase`/`port`/`adapter`), (4) external API compatibility (`strict` vs `versioned_v2`), (5) handling policy for legacy bug-risk quirks (`ask_human` Decision Log), and (6) rollout strategy (`phased_pr` / `strangler_fig` / `rewrite`) & explicit Non-Goals.
    - **Ask the user concise clarifying questions (with recommended defaults)** to resolve ambiguities, then **write the confirmed specification back into `.pni/workflows/<migration_id>.yaml` (`with.brief: |` or `brief_file`, plus explicit non-`auto` guardrail values)** and verify with `pni workflows show <migration_id>` before starting execution.
6. **Progress & Git Governance Plan Setup (`category: progress`)**:
   - Progress workflows (`uses: progress_assessment`) require a validated `.pni/progress/<target>.yaml` manifest (`git_policy`, `milestones`, `tasks`) before `pni workflows start`:
     ```bash
     pni progress init <target>
     # Tailor git_policy, milestones, and tasks in .pni/progress/<target>.yaml, then validate:
     pni progress validate <target>
     ```
   - Treat `.pni/progress/<target>.yaml` as **strictly Read-Only** during measurement runs (`plan_sha256` is verified on `emit_progress`). `based_on: <audit_workflow_id>` is optional and links Git-tracked `.pni/history/audit/<audit_workflow_id>.jsonl` without requiring `.pni/cache/workflow_state.db`.

## 2. Deterministic Stateful Execution Loop

Always execute workflows through the stateful pull-push cycle:

1. **Start Workflow**:
   ```bash
   pni workflows start <workflow_id>
   ```
   Obtain the generated `Workflow Run ID` (e.g., `wf-1a2b3c4d`).
2. **Pull Current Action**:
   ```bash
   pni workflows get-action <workflow_run_id>
   ```
   - PNI automatically executes programmatic analyzers (`project_inspect`, `ast_analyze`, `run_check`, `security_scan`, `web_pentest`, `migration_analyze`, `progress_analyze`) when reached, stores their results in `.pni/cache/workflow_state.db` and `.pni/cache/<workflow_id>/facts.json`, and outputs the current `Action ID` (`act-01`, `act-02`, ...), active rules, deterministic facts, prior architecture records, and required `INPUT` JSON Schema.
   - If the output status is `COMPLETED`, the workflow is finished.
3. **Perform Agent Work & Push Action Result**:
   - Never guess quantitative metrics or invent file paths—rely strictly on the deterministic AST/project/migration/progress facts (`module_inventory`, `internal_import_graph`, `detected_frameworks`, `boundary_touchpoints`, `refactoring_waves`, `branches`, `trajectory`, `task_evidence`).
   - On `record_architecture` steps (`purpose_and_stack`, `layers_and_modules`, `flows_and_state`), PNI validates every referenced file/module path against the real workspace and persists `.pni/cache/<workflow_id>/architecture.json`.
   - Submit your structured JSON output matching the action's Pydantic schema:
   ```bash
   pni workflows push-action <workflow_run_id> <action_id> '<JSON_INPUT>'
   # Or via JSON file:
   pni workflows push-action <workflow_run_id> <action_id> --file <payload.json>
   ```
   - On `emit_score`, PNI validates your `ScoreResult` JSON, writes `reports/<target>_score.json` deterministically, and appends/upserts `.pni/history/audit/<workflow_id>.jsonl`.
   - On `emit_migration_plan`, PNI validates your `MigrationPlanResult` JSON against grounded As-Is repository paths, attaches deterministic `MigrationFacts`, and writes `reports/<target>_migration_plan.json`.
   - On `emit_progress`, PNI verifies `.pni/progress/<target>.yaml` was not mutated mid-run, validates `ProgressResult`, writes `reports/<target>_progress.json`, and appends/upserts `.pni/history/progress/<workflow_id>.jsonl`.
   - On `write_drawlib_report` / `write_migration_report` / `write_progress_report` (final step):
     1. **READ Artifacts**: Load `reports/<target>_score.json` (or `*_migration_plan.json` / `*_progress.json`), `.pni/cache/<workflow_id>/facts.json`, `.pni/cache/<workflow_id>/architecture.json` (if present), and `.pni/cache/<workflow_id>/blueprint.json` (or `migration_blueprint.json` / `progress_blueprint.json`).
     2. **READ Code & Docs**: Inspect target source modules and documentation (`README.md`, design docs).
     3. **CONSULT Drawlib CLI & Rules On-Demand (Never Guess APIs)**:
        - Never guess `drawlib` constructor signatures, arguments, or coordinate anchors, and never fall back to raw `rectangle()`/`line()` primitives when a high-level component exists. Right before authoring diagrams, query Drawlib's built-in CLI help and rules (prefix with `uv run` in `uv` workspaces, e.g. `uv run drawlib ...`):
          ```bash
          drawlib -h                                # CLI overview (init, build, show, serve, rules, styles, colors, cache)
          drawlib rules list                        # List all guideline & module API rule topics
          drawlib rules show agent-instruction      # 3-stage multimodal self-review workflow & component catalog
          drawlib rules show overview               # Bottom-left (0, 0) coordinate space & canvas lifecycle
          drawlib rules show project-doc            # Single-document cover/ToC, 720pt typography & A4 PDF rules
          drawlib rules show api                    # Complete module/class signature & argument cheat sheet
          drawlib rules show lib-smartarts-overview # Panel, KpiCards, Roadmap, Table, TreeNode, CardList APIs
          drawlib rules show lib-charts-overview    # RadarChart, BarChart, HeatmapChart, LineChart APIs
          drawlib rules show lib-diagrams-overview  # ClassDiagram, HeatmapOverlay, architecture/flow/sequence APIs
          drawlib rules show lib-icons-overview     # Phosphor, FontAwesome & cloud architecture icon helpers
          ```
     4. **WRITE or UPDATE, GRID-VERIFY & COMPILE drawlib Report**:
        - Scaffold (non-destructive): `pni report init <target> --src-dir <src_dir> --lang <lang> --style <style>`
        - Author or update the blueprint files (`00_cover.md` + `01_*.md` .. `06_*.md` for audit/migration, or `01_*.md` .. `04_*.md` for progress) inside `<src_dir>/<target>_src/<lang>/` (preserving `<src_dir>/<target>_src/drawlib.toml`). **If chapters already exist, update them in-place without deleting existing documents or creating dated archive copies so `git diff` tracks changes cleanly.**
        - **Visual Grid Self-Verification (`drawlib show ... -g`)**: Export diagrams with the coordinate grid overlaid (`drawlib show <src_dir>/<target>_src/<lang>/<chapter.md> <diagram.png> -s <src_dir>/<target>_src/styles.py -u <src_dir>/<target>_src/utils.py -g -o .drawlib/scratch/<unique_name>_grid.png`) and visually inspect the rendered PNG with your image-viewing tool to fix text clipping, label overlap, margin violations, or coordinate anchor mistakes before finalizing the build.
        - Compile A4 vector PDF (default PDF-only): `pni report build <target> --src-dir <src_dir> --output-dir <output_dir>`
        - Push `ReportCompletionInput` listing `<output_dir>/<target>.pdf` in `generated_files`.
4. **Repeat Step 2 -> Step 3** until `get-action` / `push-action` reports `COMPLETED`.

## 3. Standard Commands
- `pni -h` / `pni --help`: Show CLI help and AI bootstrap instructions.
- `pni init`: Initialize `.pni/` (`rules/`, `actions/`, `workflows/`, `instructions.md`, and `.pni/cache/.gitignore`).
- `pni rules list [--all]` / `pni rules show <rule>`: Inspect engineering standards and workflow guides.
- `pni workflows list`: List project workflows in `.pni/workflows/`.
- `pni workflows show <workflow_id>`: Inspect resolved outputs, preflight readiness checks, and normalized primitive steps.
- `pni workflows run-action <workflow_id> <action> [--base-url URL] [--force-pentests]`: Execute a single step/action inside a workflow directly with zero SQLite preparation.
- `pni workflows start <workflow_id> [--supersede]`: Start a stateful run in `.pni/cache/workflow_state.db` (`--supersede` cancels older unfinished runs of `<workflow_id>`).
- `pni workflows get-action <run_id>`: Pull current action details, facts, rules, and input schema.
- `pni workflows push-action <run_id> <action_id> [INPUT] [--file <path>]`: Validate input and advance state.
- `pni workflows status [run_or_workflow] [--latest] [-w <workflow_id>] [-s <status>] [-n <limit>] [--json]`: Inspect step progress (`done/total`, current step) and history (always prefer this CLI over raw `sqlite3` queries).
- `pni workflows inspect-action <run_or_workflow> <action> [--agent-input|--deterministic|--json] [-o <path>]`: Inspect or export recorded deterministic outputs and agent inputs from current or prior runs without touching SQLite directly.
- `pni workflows cancel [<run_id> | --superseded [-w <workflow_id>]]`: Cancel an abandoned `in_progress` run or clean up superseded runs.
- `pni progress init [target] [-w <workflow_id>] [--force]`: Scaffold `.pni/progress/<target>.yaml` with milestones, tasks, and `git_policy`.
- `pni progress validate [target_or_path]`: Validate `.pni/progress/<target>.yaml` schema, dates, `git_policy`, and acyclic `depends_on` DAG.
- `pni pentests init [-w <workflow_id>] [--target-root .] [--source src] [--force]`: Materialize explicit `Python + httpx` penetration test files into `.pni/pentests/<target>/`.
- `pni pentests run [-w <workflow_id>] [--target-root .] [--base-url http://127.0.0.1:18080] [--force]`: Boot isolated loopback container (or target `--base-url`) and execute `.pni/pentests/<target>/`.
- `pni report init <target> [--src-dir reports_src] [--lang en] [--style google] [--force]`: Scaffold or refresh `reports_src/<target>_src/` (`drawlib.toml` + `<lang>/`) while preserving existing `*.md` chapters.
- `pni report build <target> [--src-dir reports_src] [--output-dir reports] [-f pdf] [--toc/--no-toc]`: Compile `reports/<target>.pdf` (default PDF-only; optional `-f html -f markdown -f images`).
- `pni validate-score <path>`: Validate a score JSON file against `ScoreResult`.
- `pni validate-migration-plan <path>`: Validate a migration plan JSON file against `MigrationPlanResult`.
- `pni validate-progress <path>`: Validate a progress assessment JSON file against `ProgressResult`.

## 4. Drawlib CLI & Rules Reference (On-Demand During Visual Report Steps)

Load Drawlib specifications dynamically only when entering `write_drawlib_report` / `write_migration_report` (keeps early analysis context lean while preventing API/layout hallucinations; run via `uv run drawlib ...` inside `uv` projects):
- `drawlib -h` / `drawlib <subcommand> -h`: Inspect CLI usage and options (`init`, `build`, `show`, `serve`, `rules`, `styles`, `colors`, `css`, `cache`).
- `drawlib rules list`: List all built-in drawing guidelines and `lib-*` module reference manuals.
- `drawlib rules show agent-instruction` / `drawlib rules show review-guide`: Read the 3-stage multimodal self-correction loop, coordinate anchor table (`Center` vs. `Bottom-Left` vs. `Top-Left`), `720pt` typography math, and `50%+` neutral color rule.
- `drawlib rules show overview` / `drawlib rules show project-doc`: Inspect bottom-left `(0, 0)` canvas geometry, `setup()`/`save()` lifecycle, and linear `doc` cover/ToC/PDF rules (`navbar.md` prohibited).
- `drawlib rules show api` / `drawlib rules show lib-<module>`: Inspect exact Python class/function signatures (`lib-smartarts-overview`, `lib-charts-overview`, `lib-diagrams-overview`, `lib-icons-overview`, `lib-styles`, `lib-shapes-overview`, `lib-lines`, `lib-text`, `lib-graph-overview`).
- `drawlib show <file.md|.py> [target] -s styles.py -u utils.py -g -o .drawlib/scratch/<unique_name>_grid.png`: Headlessly export a diagram with the 10-unit/5-unit coordinate grid overlaid for visual inspection.
- `drawlib serve <html_dir> --check`: Verify zero broken links or missing assets when HTML output (`-f html`) is built.
- `drawlib styles list` / `drawlib colors list` / `drawlib cache list`: Inspect built-in style/color catalogs and cached font/icon packages.

