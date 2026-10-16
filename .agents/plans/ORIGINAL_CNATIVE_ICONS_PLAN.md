# Original Cloud Native Icons Plan (`drawlib.icons.original_cnative`)

## 1. Objective & Design Principle (30% Original + 70% Drawlib Unity)

Add 48 vendor-neutral Drawlib Original Cloud Native icons under `drawlib.icons.original_cnative` (`OriginalCnativeIcon`), plus 72 shorthand aliases.

- **Core Design Rule**: **30% Original Essence + 70% Drawlib Visual Unity**.
  - **30% Original Essence**: Retain the recognizable silhouette, mascot, or core geometric motif of each official icon (e.g., Argo's friendly octopus in a space helmet, Kubernetes' rounded 7-sided heptagon, Istio's sailboat, Prometheus' flame, Jaeger's gopher, Crossplane's popsicle, Rook's castle tower).
  - **70% Drawlib Visual Unity**: Replace multi-stop vendor gradients and tiny complex paths with Drawlib's clean flat pastel surfaces, bold dark structural borders, and generous spacing.

---

## 2. Mandatory Technical & Style Rules

- **Canvas**: `100x100` (`setup_icon()`), origin `(0,0)` at bottom-left, center `(50,50)`. Keep all geometry inside `[8.0, 92.0]`.
- **Imports**: Always use `from drawlib.utils import ...` (NEVER `from utils import ...` so `ty` static type checks pass).
- **Color Palette** (strictly from `drawlib.utils`):
  - `PASTEL_BLUE = "#86A4F7"` (Primary pastel cornflower blue fill)
  - `PASTEL_BLUE_LIGHT = "#ACC2FA"` (Lighter pastel blue companion fill)
  - `PASTEL_GREEN = "#7AD69E"` (Soft mint/sage green accent fill)
  - `WHITE = "#FFFFFF"` (Crisp white base / inner card / cutout fill)
  - `DARK = "#323A48"` (Deep slate structural border and line color)
- **Color Balance**: Use 2 or 3 fill colors (`WHITE` + `PASTEL_BLUE`, or `WHITE` + `PASTEL_BLUE` + `PASTEL_GREEN` / `PASTEL_BLUE_LIGHT`) as needed for clear visual hierarchy. Avoid visual noise.
- **Stroke Width**: Primary outer borders use `w = ORIG_STROKE` (`2.7` units). Inner details use `2.0–2.4` units.
- **No `text()` or `image()`**: Every icon must be pure geometric primitives (`circle`, `rectangle`, `polygon`, `arc`, `ellipse`, `draw_iso_cube`, `draw_round_polyline`, `draw_round_segment`, `draw_original_k8s_heptagon`, `build_shield_half_points`, `draw_cisco_arrow`).

---

## 3. Canonical Icon Specifications (48 Icons)

### Batch 1: Kubernetes Control Plane & Workloads (`k8s_*` 1–12)

All 20 `k8s_*` icons call `draw_original_k8s_heptagon()` first (which draws the rounded 7-sided heptagon in `PASTEL_BLUE` with a `DARK` `2.7` border). Place the clean Drawlib inner motif centered around `(50, 48)`:

| # | Filename | 30% Original + 70% Drawlib Motif |
| :- | :--- | :--- |
| 1 | `k8s_api_server_default.py` | `draw_original_k8s_heptagon()` + `WHITE` rounded API gateway card (`(50, 48)`, `w=44, h=34, r=6`) + `PASTEL_GREEN` central routing circle (`r=6.5`) with left/right horizontal `DARK` bidirectional arrows |
| 2 | `k8s_configmap_default.py` | `draw_original_k8s_heptagon()` + `WHITE` rounded card (`(50, 48)`, `w=44, h=38, r=6`) containing 3 horizontal `DARK` slider tracks with alternating `PASTEL_GREEN` & `PASTEL_BLUE_LIGHT` circular knobs |
| 3 | `k8s_control_plane_default.py` | `draw_original_k8s_heptagon()` + `WHITE` ship's wheel ring (`(50, 48)`, outer `r=18`, inner `r=11`, `DARK` borders) + 7 radial `DARK` spokes with rounded tips (`r_tip=24`) + `PASTEL_GREEN` center hub (`r=6`) |
| 4 | `k8s_crd_default.py` | `draw_original_k8s_heptagon()` + `WHITE` rounded square (`(44, 46)`, `w=30, h=30, r=5`) + interlocking top-right `PASTEL_GREEN` extension square (`(60, 56)`, `w=20, h=20, r=4`) with a crisp `DARK` plus `+` inside |
| 5 | `k8s_cronjob_default.py` | `draw_original_k8s_heptagon()` + `WHITE` circular clock face (`(50, 46)`, `r=21`, `DARK` border) + top `PASTEL_GREEN` alarm/schedule tab (`(50, 70)`, `w=14, h=6, r=2`) + `DARK` L-shaped clock hands & `PASTEL_GREEN` center dot |
| 6 | `k8s_daemonset_default.py` | `draw_original_k8s_heptagon()` + bottom `PASTEL_GREEN` horizontal node bar (`(50, 29)`, `w=46, h=8, r=3`) + 2 side-by-side `WHITE` pod squares above (`(38, 49)` and `(62, 49)`, `w=19, h=19, r=4`) with `PASTEL_BLUE_LIGHT` inner dots |
| 7 | `k8s_deployment_default.py` | `draw_original_k8s_heptagon()` + central `draw_iso_cube(50, 46, radius=14, top_color=WHITE, left_color=PASTEL_BLUE_LIGHT, right_color=PASTEL_GREEN, border_color=DARK, border_units=2.2)` + upper curved `DARK` / `WHITE` circular rollout arrow arc (`r=23`) |
| 8 | `k8s_endpoint_default.py` | `draw_original_k8s_heptagon()` + left `WHITE` source circle (`(31, 48)`, `r=7`) connected by `DARK` lines to 2 right `PASTEL_GREEN` target circles (`(64, 58)` and `(64, 38)`, `r=7.5`) |
| 9 | `k8s_hpa_default.py` | `draw_original_k8s_heptagon()` + central `WHITE` pod square (`(50, 48)`, `w=22, h=22, r=4`) with `PASTEL_GREEN` inner square (`w=10, h=10, r=2`) + left & right outward `DARK` horizontal scaling arrows (`x=23..35` and `x=65..77`) |
| 10 | `k8s_ingress_default.py` | `draw_original_k8s_heptagon()` + right `WHITE` gateway frame (`(56, 48)`, `w=32, h=36, r=6`) + left `PASTEL_GREEN` entry circle (`(28, 48)`, `r=6.5`) with a `DARK` arrow entering the card and branching to 2 `PASTEL_BLUE_LIGHT` dots |
| 11 | `k8s_job_default.py` | `draw_original_k8s_heptagon()` + `WHITE` task card (`(47, 48)`, `w=36, h=38, r=6`) with 2 `DARK` horizontal lines + bottom-right overlapping `PASTEL_GREEN` circle (`(62, 36)`, `r=12`) with crisp `DARK` checkmark |
| 12 | `k8s_namespace_default.py` | `draw_original_k8s_heptagon()` + `WHITE` inner workspace card (`(50, 48)`, `w=44, h=34, r=6`, `DARK` border) + 4 `PASTEL_GREEN` corner bracket L-accents or inner dashed `DARK` frame |

### Batch 2: Kubernetes Networking/Storage (`k8s_*` 13–20) + 4 Projects

| # | Filename | 30% Original + 70% Drawlib Motif |
| :- | :--- | :--- |
| 13 | `k8s_network_policy_default.py` | `draw_original_k8s_heptagon()` + `PASTEL_GREEN` shield (`build_shield_half_points(50, 25, 69, 19)`, `DARK` border) + `WHITE` center circle (`r=8`) with `DARK` checkmark or node link |
| 14 | `k8s_node_default.py` | `draw_original_k8s_heptagon()` + `WHITE` horizontal rack host (`(50, 48)`, `w=48, h=30, r=5`) divided into upper CPU bay (`PASTEL_BLUE_LIGHT` square chip at `(38, 54)`) and lower slot bar with `PASTEL_GREEN` LED dot at `(64, 39)` |
| 15 | `k8s_pod_default.py` | `draw_original_k8s_heptagon()` + single large crisp isometric container cube: `draw_iso_cube(50.0, 47.0, radius=21.0, top_color=WHITE, left_color=PASTEL_BLUE_LIGHT, right_color=PASTEL_GREEN, border_color=DARK, border_units=2.4)` |
| 16 | `k8s_pv_default.py` | `draw_original_k8s_heptagon()` + 2-tier 2D storage cylinder (`x=30..70`): lower body in `WHITE`, upper body in `PASTEL_BLUE_LIGHT`, top ellipse cap in `PASTEL_GREEN`, all with `DARK` `2.3` borders |
| 17 | `k8s_pvc_default.py` | `draw_original_k8s_heptagon()` + `WHITE` storage cylinder (`x=29..65, y=31..63`) + bottom-right overlapping `PASTEL_GREEN` circular badge (`(64, 36)`, `r=11`) with `DARK` inward claim arrow/link |
| 18 | `k8s_secret_default.py` | `draw_original_k8s_heptagon()` + `WHITE` padlock shackle arch (`(50, 56)`, `r_outer=12, r_inner=6.5`) + `PASTEL_GREEN` rounded padlock body (`(50, 41)`, `w=32, h=24, r=4`) + `WHITE` keyhole circle (`(50, 41)`, `r=4.5`) |
| 19 | `k8s_service_default.py` | `draw_original_k8s_heptagon()` + top `PASTEL_GREEN` service hub circle (`(50, 64)`, `r=8`) branching via orthogonal `DARK` lines (`y=50` crossbar) to 3 bottom `WHITE` pod circles (`(33, 33)`, `(50, 33)`, `(67, 33)`, `r=6.5`) |
| 20 | `k8s_statefulset_default.py` | `draw_original_k8s_heptagon()` + back stacked `PASTEL_BLUE_LIGHT` card (`(55, 53)`, `w=36, h=30, r=4`) + front `WHITE` card (`(46, 44)`, `w=36, h=30, r=4`) containing a small `PASTEL_GREEN` cylinder (`(46, 44)`, `w=20, h=16`) |
| 21 | `argo_default.py` | Cute simplified Argo CD space-octopus: `WHITE` circular space helmet (`(50, 58)`, `r=31`, `DARK` border) with `PASTEL_BLUE_LIGHT` inner visor ring (`r=25`) + `PASTEL_BLUE` rounded octopus head/body (`x=34..66, y=26..72`) + 4 clean rounded tentacles at bottom (`y=12..28`) + 2 big `WHITE` circular eyes (`(41, 56)` & `(59, 56)`, `r=8.5`) with `DARK` pupils (`r=3.5`) + `PASTEL_GREEN` collar band or smile |
| 22 | `backstage_default.py` | Rounded square portal (`(50, 50)`, `w=76, h=76, r=14`, `PASTEL_BLUE` fill, `DARK` border `2.7`) + stylized geometric `B` made of 2 stacked left-aligned `WHITE` & `PASTEL_GREEN` isometric/angled stage blocks (`DARK` borders `2.3`) |
| 23 | `cert_manager_default.py` | `draw_original_k8s_heptagon()` (or `PASTEL_BLUE` shield/heptagon) + `WHITE` certificate card (`(48, 52)`, `w=36, h=32, r=4`, `DARK` border) with 2 `DARK` text lines + bottom-right `PASTEL_GREEN` circular seal (`(62, 34)`, `r=11`) & `WHITE`/`DARK` ribbon tails |
| 24 | `cilium_default.py` | Clean 7-hexagon honeycomb cluster centered at `(50, 50)` (each flat-top or pointy-top hex `r=13.5`, `DARK` border `2.4`): center hexagon in `PASTEL_GREEN`, 3 alternating outer hexagons in `PASTEL_BLUE`, 3 alternating outer hexagons in `WHITE` / `PASTEL_BLUE_LIGHT` |

### Batch 3: Cloud Native Projects 25–36

| # | Filename | 30% Original + 70% Drawlib Motif |
| :- | :--- | :--- |
| 25 | `containerd_default.py` | Rounded square (`(50, 50)`, `w=74, h=74, r=12`, `PASTEL_BLUE` fill, `DARK` border `2.7`) + bold geometric `WHITE` block-letter `d` (`x=31..69, y=22..78`, `DARK` border `2.3`) + `PASTEL_GREEN` inner square cutout (`(47, 39)`, `w=14, h=14, r=2`, `DARK` border `2.0`) |
| 26 | `coredns_default.py` | Two overlapping 45°-tilted rounded squares: back tilted square at `(56, 56)` in `PASTEL_BLUE_LIGHT`, main tilted square at `(46, 46)` in `PASTEL_BLUE` (`DARK` border `2.7`) + central 45°-tilted `WHITE` & `PASTEL_GREEN` capsule chain-link ring (`DARK` border `2.4`) |
| 27 | `crossplane_default.py` | Cute upright/slightly-tilted rounded popsicle (`x=28..72, y=30..88`, `DARK` border `2.7`) divided into 3 diagonal stripes (`WHITE` top, `PASTEL_BLUE` middle, `PASTEL_GREEN` bottom, `DARK` `2.3` dividers) + bottom rounded popsicle stick (`(50, 19)`, `w=14, h=22, r=6`, `PASTEL_BLUE_LIGHT` fill, `DARK` border `2.5`) |
| 28 | `dapr_default.py` | Friendly simplified bowler/top hat: wide curved brim (`(50, 32)`, `w=78, h=16, r=7`, `PASTEL_BLUE`, `DARK` border `2.7`) + rounded crown (`(50, 56)`, `w=52, h=42, r=14`, `PASTEL_BLUE`, `DARK` border `2.7`) + horizontal `PASTEL_GREEN` hat ribbon band (`(50, 42)`, `w=52, h=10`, `DARK` border `2.3`) + small `WHITE` highlight pill on left crown |
| 29 | `docker_default.py` | Cute flat 2D whale (`PASTEL_BLUE` whale body `x=12..82, y=18..48` with raised tail fluke on right `x=76..90, y=44..62`, `WHITE` lower belly curve, `DARK` eye dot at `(26, 34)`, `DARK` border `2.7`) + 5 container squares stacked on back (`y=48..76`, 3 bottom + 2 top in `WHITE`, `PASTEL_GREEN`, `PASTEL_BLUE_LIGHT` with `DARK` `2.2` borders) |
| 30 | `envoy_default.py` | Clean geometric hexagon badge centered at `(50, 50)` (`r=40`, `DARK` border `2.7`): 3 outer ribbon facets alternating `PASTEL_BLUE`, `PASTEL_BLUE_LIGHT`, `PASTEL_GREEN` (`DARK` `2.3` seam lines) surrounding a crisp center `WHITE` hexagon (`r=17`, `DARK` border `2.4`) |
| 31 | `etcd_default.py` | 8-tooth rounded gear wheel centered at `(50, 50)` (`r_outer=40, r_base=31`, `PASTEL_BLUE` fill, `DARK` border `2.7`) + inner `WHITE` circular face (`r=21`, `DARK` border `2.4`) + two `PASTEL_GREEN` circular eyes/nodes (`(42, 50)` & `(58, 50)`, `r=5.0`, `DARK` border `2.0`) |
| 32 | `falco_default.py` | Circular medallion (`(50, 50)`, `r=40`, `WHITE` fill, `DARK` border `2.7`) + swooping `PASTEL_BLUE` & `PASTEL_BLUE_LIGHT` layered falcon wing bars on left/top + crisp `PASTEL_GREEN` hooked falcon beak & head profile on right (`DARK` borders `2.4`) |
| 33 | `fluentd_default.py` | Clean simplified flying bird silhouette (`x=12..88, y=18..82`, `DARK` border `2.7`): `PASTEL_BLUE` body, neck, and pointed beak on right (`WHITE` eye circle at `(74, 58)`, `r=3.5`), `PASTEL_BLUE_LIGHT` raised upper wing on top-left, and `PASTEL_GREEN` lower wing/tail facet at bottom-left (`DARK` `2.3` facet seams) |
| 34 | `flux_default.py` | Clean geometric upward weave: top `PASTEL_GREEN` diamond (`(58, 76)`, `r=10`, `DARK` border `2.5`) + right `PASTEL_BLUE` upward chevron arrow + 3 left diagonal parallel wave bars (`WHITE`, `PASTEL_BLUE_LIGHT`, `PASTEL_BLUE` with `DARK` borders `2.4`) |
| 35 | `grafana_default.py` | Simplified 7-fin spiral sun-gear (`(50, 50)`, `r_outer=41`, `PASTEL_BLUE` outer gear silhouette with 7 rounded fins, `DARK` border `2.7`) + inner `WHITE` circular cutout (`r=26`) containing a clean `PASTEL_GREEN` spiral coil (`DARK` border `2.4`) |
| 36 | `harbor_default.py` | Circular badge (`(50, 50)`, `r=40`, `WHITE` fill, `PASTEL_BLUE` outer ring thickness `7`, `DARK` border `2.7`) + left `PASTEL_BLUE` & `WHITE` lighthouse tower (`x=34..46, y=20..70`, `DARK` border `2.3`) + right `PASTEL_GREEN` triangular light beam fan (`(46, 58)` fanning to `x=82, y=44..72`, `DARK` border `2.2`) |

### Batch 4: Cloud Native Projects 37–48

| # | Filename | 30% Original + 70% Drawlib Motif |
| :- | :--- | :--- |
| 37 | `helm_default.py` | Standalone nautical ship's helm wheel centered at `(50, 50)`: `PASTEL_BLUE` wheel ring (`r_outer=28, r_inner=18`, `DARK` border `2.7`), 8 radial spokes (`DARK` / `PASTEL_BLUE` with rounded outer handles extending to `r=41`, `DARK` border `2.4`), `WHITE` inner ring, and `PASTEL_GREEN` center hub circle (`r=8`, `DARK` border `2.4`) |
| 38 | `istio_default.py` | Crisp geometric sailboat (`x=18..82, y=12..88`, all `DARK` borders `2.7`): large right main triangle sail (`(46, 30), (46, 86), (80, 30)` in `PASTEL_BLUE`), left jib triangle sail (`(20, 30), (41, 70), (41, 30)` in `WHITE`), and bottom tapered hull polygon (`y=12..25` in `PASTEL_GREEN`) |
| 39 | `jaeger_default.py` | Cute simplified gopher mascot (`x=20..80, y=14..86`, `DARK` borders `2.6`): `PASTEL_BLUE` rounded body (`x=24..76, y=14..68`), `PASTEL_GREEN` explorer hat on top (`x=18..82, y=62..84`) with `WHITE` hat band, 2 big `WHITE` circular eyes (`(39, 48)` & `(61, 48)`, `r=9.5`) with `DARK` pupils (`r=3.8`), `WHITE` oval snout (`(50, 31)`, `w=22, h=11`) with `DARK` nose oval, and 2 small `WHITE` buck teeth below |
| 40 | `keda_default.py` | Heptagonal node ring centered at `(50, 50)` (`r=34`): 7 straight `PASTEL_BLUE_LIGHT` ring segments (`w=6`, `DARK` borders `2.2`), 7 `PASTEL_BLUE` vertex circles (`r=6.5`, `DARK` border `2.3`), and a bold central `PASTEL_GREEN` lightning bolt (`y=28..72`, `DARK` border `2.5`) |
| 41 | `knative_default.py` | Pointy-top rounded hexagon (`(50, 50)`, `r=40`, `PASTEL_BLUE` fill, `DARK` border `2.7`) + bold central `WHITE` letter `K` / wing block (`x=32..68, y=28..72`, `DARK` border `2.4`) with `PASTEL_GREEN` right arrow-wing accent |
| 42 | `kubernetes_default.py` | `draw_original_k8s_heptagon()` (`PASTEL_BLUE` fill, `DARK` border `2.7`) + full crisp 7-spoke `WHITE` ship's wheel (`r_ring_outer=22, r_ring_inner=15, r_handle=32`, `DARK` border `2.2`) + `PASTEL_GREEN` center hub circle (`(50, 48)`, `r=6.5`, `DARK` border `2.2`) |
| 43 | `kyverno_default.py` | Protective policy shield (`build_shield_half_points(50, 12, 86, 34)`, `PASTEL_BLUE` outer shield with `DARK` border `2.7`, `WHITE` inner shield `build_shield_half_points(50, 20, 78, 25)` with `DARK` border `2.2`) + central `PASTEL_GREEN` diamond/scale checkmark badge (`(50, 52)`, `r=12`, `DARK` border `2.3`) |
| 44 | `linkerd_default.py` | Clean isometric woven lattice cube (`x=16..84, y=14..86`, `DARK` borders `2.3`): 3 top diagonal bars tilted at +30°/-30° in `PASTEL_GREEN` & `WHITE` weaving neatly into 4 vertical front pillars in `PASTEL_BLUE` (outer) and `PASTEL_BLUE_LIGHT` (inner) |
| 45 | `opa_default.py` | Clean simplified policy/Viking helmet (`x=12..88, y=16..84`, `DARK` borders `2.6`): `WHITE` left & right curved wing/horn shapes (`x=12..34` and `x=66..88`), `PASTEL_BLUE` rounded center helmet dome (`(50, 52)`, `w=44, h=46`), and `PASTEL_GREEN` horizontal brow band + center vertical nose guard (`x=46..54, y=22..50`) |
| 46 | `opentelemetry_default.py` | Clean 35°-tilted 2-stage telescope (`x=18..82, y=18..82`, `DARK` borders `2.6`): lower-left narrower tube in `PASTEL_BLUE_LIGHT`, middle tube in `PASTEL_BLUE`, upper-right wide lens hood in `PASTEL_GREEN` with `WHITE` glass ellipse, plus 2 small `WHITE` / `PASTEL_GREEN` star/signal dots at top-right |
| 47 | `prometheus_default.py` | Circular medallion (`(50, 50)`, `r=40`, `PASTEL_BLUE` outer ring, `WHITE` inner circle `r=31`, `DARK` borders `2.7` & `2.3`) + bold stylized 3-tip `PASTEL_GREEN` flame (`y=38..74`, `DARK` border `2.4`) + horizontal `PASTEL_BLUE` torch base bar & `PASTEL_BLUE_LIGHT` lower dish (`y=22..34`, `DARK` border `2.2`) |
| 48 | `rook_default.py` | Clean chess castle rook tower (`x=26..74, y=14..86`, `DARK` borders `2.7`): wide `PASTEL_BLUE` stepped base (`y=14..26`), tapered `PASTEL_BLUE` tower shaft (`y=26..66`), `WHITE` arched window cutout at `(50, 46)` (`w=14, h=20, r=6`, `DARK` border `2.3`), and 3 `PASTEL_GREEN` top crenellations/battlements (`y=66..84`) |

---

## 4. Verification Checklist for Each Subagent

1. **Stage 1 (Static Check)**:
   - Run `uv run ruff check` and `uv run ruff format --check` on assigned files in `tools/icons_src/original_cnative/`.
   - Confirm zero `image()` or `text()` calls, and all imports use `from drawlib.utils import ...`.
2. **Stage 2 (Visual Grid Review)**:
   - Render each icon with `-g` into `.drawlib/scratch/original_cnative_preview/<stem>_grid.png` (using `-s /usr/local/google/home/yuichiito/git_github/drawlib/tools/icons_src/styles.py -u /usr/local/google/home/yuichiito/git_github/drawlib/tools/icons_src/utils.py --no-cache`).
   - View every rendered preview via `view_file` alongside its `tools/release_assets/v0.3/icons/cnative/<stem>.png` reference to verify:
     - 30% original motif recognition + 70% Drawlib flat pastel unity (`PASTEL_BLUE`, `PASTEL_BLUE_LIGHT`, `PASTEL_GREEN`, `WHITE`, `DARK` borders).
     - Clean centering, balanced margins (`>= 8` units), and zero overlapping or clipped lines.
