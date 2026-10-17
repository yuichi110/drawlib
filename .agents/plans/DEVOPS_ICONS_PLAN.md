# Official DevOps Icons Plan (`drawlib.icons.devops` & `drawlib.icons.original_devops`)

## 1. Objective & Scope

Add 40 official DevOps, CI/CD, IaC, Testing, DevSecOps, Observability, and Collaboration product/OSS icons under a new `drawlib.icons.devops` module (`DevopsIcon`), and subsequently expand `drawlib.icons.original_devops` (`OriginalDevopsIcon`) with 40 Drawlib-stylized pastel versions of those logos (at stroke width `1.9` to match `original_data` and `original_ai`).

- **Core Separation Rule**:
  - **`drawlib.icons.devops`**: Contains ONLY real products and OSS projects with an unmistakable official logo (40 canonical icons + 17 shorthand aliases). Generic concept icons (`cicd_pipeline`, `git_repository`, `secret_vault`, etc.) do NOT belong in `devops`.
  - **`drawlib.icons.original_devops`**: Contains both the existing 20 vendor-neutral DevOps concept icons AND the 40 Drawlib-stylized pastel versions of the `devops` logos (60 canonical icons total).
  - **Zero Overlap**: Does not duplicate icons already present in `cnative` (`docker`, `kubernetes`, `helm`, `argo`, `flux`, `prometheus`, `grafana`, `jaeger`, `opentelemetry`, `fluentd`, `backstage`, `harbor`, `opa`, `falco`, `crossplane`), `data` (`elasticsearch`, `opensearch`, `airflow`, `dagster`, `dbt`), or `ai` (`n8n`, `mlflow`, `wandb`, `langfuse`).

---

## 2. The 40 Canonical `devops` Icons

| Row | Category | Canonical Names (10 per row) |
| :- | :--- | :--- |
| **1** | **Source Control & CI/CD** | `git`, `github`, `github_actions`, `gitlab`, `bitbucket`, `jenkins`, `circleci`, `buildkite`, `tekton`, `spinnaker` |
| **2** | **IaC, Config, Secrets & Artifacts** | `terraform`, `opentofu`, `pulumi`, `ansible`, `packer`, `vagrant`, `vault`, `consul`, `jfrog`, `nexus` |
| **3** | **Testing, Quality & DevSecOps** | `sonarqube`, `snyk`, `trivy`, `keycloak`, `postman`, `playwright`, `cypress`, `selenium`, `k6`, `podman` |
| **4** | **Observability, Incident & Collab** | `datadog`, `new_relic`, `dynatrace`, `splunk`, `sentry`, `kibana`, `loki`, `pagerduty`, `jira`, `slack` |

### Shorthand Aliases (`DEVOPS_ALIASES` — 17 aliases)
- `actions` -> `github_actions`
- `artifactory` -> `jfrog`
- `bb` -> `bitbucket`
- `circle` -> `circleci`
- `dd` -> `datadog`
- `gh` -> `github`
- `gha` -> `github_actions`
- `gl` -> `gitlab`
- `hashicorp_consul` -> `consul`
- `hashicorp_vault` -> `vault`
- `nr` -> `new_relic`
- `pd` -> `pagerduty`
- `pw` -> `playwright`
- `sonar` -> `sonarqube`
- `sonatype_nexus` -> `nexus`
- `tf` -> `terraform`
- `tofu` -> `opentofu`

---

## 3. Technical & Authoring Rules for `tools/icons_src/devops/`

- **Canvas**: `100x100` (`setup_icon()`), origin `(0,0)` at bottom-left, center `(50,50)`. Keep all geometry inside `[9.0, 91.0]` (`82x82` inner box).
- **Pure Drawlib Primitives Only**: Never call `image()` or `text()`. Use `polygon()`, `circle()`, `rectangle()`, `draw_compound_polygon()`, `fill_style()`, `no_border_fill()`, and `stroke_style()`.
- **Reference Assets**: Stored in `tools/original_assets/devops/<name>/<name>.svg` (full-color official brand marks), with rasterized `512x512` reference PNGs in `.drawlib/scratch/devops_ref/<name>_ref.png`.
- **Transparent Background Cutout Holes**: Any negative-space hole in the official SVG (e.g. `circleci` center aperture, `vault` keyhole, `github_actions` node holes, `trivy` triskelion gaps) must use `draw_compound_polygon()` or open contours so the background shows through cleanly on colored cards (`Colors.Blue2`), never filled with `WHITE`. Foreground white marks on solid badges (`ansible` white "A" on dark circle, `pagerduty` white "P" on green badge, `postman` white astronaut on orange circle) stay `WHITE`.

---

## 4. Wiring & Packaging Checklist (`drawlib.icons.devops`)

1. **Provider Module**:
   - `src/drawlib/_icons/png_icons/devops/__init__.py`
   - `src/drawlib/_icons/png_icons/devops/_base.py` (`DEVOPS_ALIASES`, `DEVOPS_PROVIDER`)
   - `src/drawlib/_icons/png_icons/devops/_generated.py` (generated via `./dcli codegen icon-devops`)
2. **Facade & Package Exports**:
   - `src/drawlib/_icons/png_icons/__init__.py` (`devops`)
   - `src/drawlib/_icons/__init__.py` (`devops`)
   - `src/drawlib/icons.py` (`devops`, `sys.modules["drawlib.icons.devops"] = devops`)
3. **Architecture & Sequence Diagram Enums**:
   - `src/drawlib/_diagrams/architecture/_icons.py` (`DevopsIcon`)
   - `src/drawlib/_diagrams/architecture/__init__.py` (`DevopsIcon`)
   - `src/drawlib/_diagrams/architecture/_types.py` (`DevopsIcon` in `IconType`)
   - `src/drawlib/_diagrams/_common.py` (`DevopsIcon` -> `devops_gen` in `_ENUM_ICON_MODULES`)
   - `src/drawlib/_diagrams/sequence/_types.py` & `_render_elements.py` (`DevopsIcon`)
   - `src/drawlib/diagrams/architecture.py` & `sequence.py` (`DevopsIcon`)
4. **DCLI Codegen & Release Assets**:
   - `tools/dcli/codegen/icons_build.py` (`"devops": DEVOPS_ALIASES` in `PROVIDER_ALIASES`)
   - `tools/dcli/codegen/original_cloud_codegen.py` (`"devops": "DevOps"` in `PROVIDER_LABELS`, `"devops": "DevopsIcon"` in `PROVIDER_ENUM_NAMES`)
   - `tools/dcli/codegen/cli.py` (`icon-devops` command)
   - `./dcli release-assets build icon_devops` and `./dcli release-assets sync`
5. **Tests & Rules**:
   - `tests/drawlib/icons/test_devops.py`
   - `src/drawlib/_rules/api.md`, `lib_icons.md`, `lib_diagrams.md`

---

## 5. Verification Steps

1. Collect all 40 official color SVGs into `tools/original_assets/devops/<name>/<name>.svg` and rasterize `.drawlib/scratch/devops_ref/<name>_ref.png` (`512x512`). Inspect a 40-icon reference contact sheet to verify every logo is authentic and full-color.
2. Author `tools/icons_src/devops/<name>_default.py` in 4 parallel subagent batches (10 icons per batch). Each subagent renders `-g --no-cache` grid previews and compares against `_ref.png` via `view_file`.
3. Render `512x512` PNGs into `tools/release_assets/v0.3/icons/devops/` and `src/drawlib/_cached_assets/icons/devops/`.
4. Run `./dcli codegen icon-devops`, `./dcli release-assets build icon_devops`, and `./dcli release-assets sync`.
5. Build a 40-icon `devops_icons_contact_sheet.png` (and blue-card hole check), run `./dcli code-check all` and `./dcli test target icons --no-cov`, and present the result to the user before Phase 2 (`original_devops`).
