# Original Security Concept Icons Design Plan (`drawlib.icons.original_security`)

## 1. Design Goal & Consistency Strategy

Author 24 vendor-neutral security concept icons in `drawlib.icons.original_security` (`OriginalSecurityIcon`) with strict visual consistency across 5 domains.
Unlike networking (where Cisco's router/switch stencils are universal), security spans diverse concepts (IAM, firewalls, crypto, SIEM, threat intel). To prevent icons from either looking like "24 identical shields" or "24 unrelated clip-art drawings", every icon follows a **2-Layer Visual Grammar**:

- **Layer 1 — Distinct Structural Base (`PASTEL_BLUE` / `PASTEL_BLUE_LIGHT` / `WHITE`)**: Each icon starts with a unique, immediately recognizable container or asset silhouette (ID card, smartphone, fortress, pyramid tree, brick wall, globe, tunnel, laptop, database, cloud, envelope, certificate, microchip, safe door, radar scope, console, honeycomb).
- **Layer 2 — Security Action Accent (`PASTEL_GREEN`)**: Every icon highlights its active security mechanism (shield, padlock, key, inspection eye, seal, rotary dial, magnifying lens, or radar target) in `PASTEL_GREEN`.

---

## 2. Shared Color & Stroke Specification (`original_cloud` / `original_network` Parity)

- **Canvas**: `100x100` (`setup_icon()`), origin `(0, 0)` at bottom-left, center `(50.0, 50.0)`. All geometry inside `[9.0, 91.0]`.
- **Colors (`tools/icons_src/utils.py`)**:
  - `PASTEL_BLUE = "#86A4F7"` — Primary container / appliance / structural surface.
  - `PASTEL_BLUE_LIGHT = "#ACC2FA"` — Secondary split-half / highlight brick / flap.
  - `PASTEL_GREEN = "#7AD69E"` — Security focal element (shield, lock, key, lens, target blip).
  - `WHITE = "#FFFFFF"` — Inner contrast card, screen panel, or badge backing.
  - `DARK = "#323A48"` — All structural outlines and line details.
- **Stroke Widths**:
  - Outer / primary structural border: `ORIG_STROKE = 2.7` (`w = 2.7`).
  - Secondary / inner panel border: `2.0`–`2.4`.
- **Shield Discipline**:
  - Use the heraldic shield (`build_shield_half_points`) ONLY on the 7 perimeter/filter/defense icons (`firewall`, `waf`, `ddos_protection`, `zero_trust`, `ids_ips`, `edr_xdr`, `email_security`), always paired with a unique base silhouette so none look repetitive.

---

## 3. The 24 Concept Icons — 5-Family Design Matrix

### Family 1: Identity & Access Management (4 Icons)

| # | Name | Base Silhouette (`PASTEL_BLUE` / `WHITE`) | Security Accent (`PASTEL_GREEN`) | Design Decision vs. Existing |
| :- | :--- | :--- | :--- | :--- |
| 1 | `iam_sso` | Horizontal ID badge card (`WHITE`) + left `PASTEL_BLUE` user avatar | Top lanyard clip + bottom-right `PASTEL_GREEN` key badge | **Improved** from `identity_auth` (adds key badge so it reads as Auth/SSO, not just a profile card) |
| 2 | `mfa_auth` | Vertical smartphone bezel (`PASTEL_BLUE` body, `WHITE` screen, top speaker, 3 PIN dots) | Bottom-right `PASTEL_GREEN` shield with checkmark | **New** |
| 3 | `pam_bastion` | Castle fortress with top battlements (`PASTEL_BLUE` crown, `WHITE` wall) | Inner `PASTEL_GREEN` SSH terminal screen (`>_`) | **Adopted** from `bastion_host` (clear fortress + privileged terminal motif) |
| 4 | `directory_service` | Clean orthogonal T-branch hierarchy (`PASTEL_BLUE` middle OU squares, `WHITE` user circles) | Top `PASTEL_GREEN` root node | **Improved** from `directory_service` (replaces triangular truss lines with clean orthogonal tree branches) |

### Family 2: Network & Perimeter Defense (5 Icons)

| # | Name | Base Silhouette (`PASTEL_BLUE` / `WHITE`) | Security Accent (`PASTEL_GREEN`) | Design Decision vs. Existing |
| :- | :--- | :--- | :--- | :--- |
| 5 | `firewall` | Staggered brick wall (`PASTEL_BLUE` & `PASTEL_BLUE_LIGHT` bricks) | Bottom-right `PASTEL_GREEN` shield + `WHITE` checkmark circle | **Adopted** from `original_network/firewall` |
| 6 | `waf` | Web browser window (`WHITE` body, `PASTEL_BLUE` top bar with dots, `</>` inside) | Bottom-right `PASTEL_GREEN` shield with checkmark | **Improved** from `original_cloud/waf` (uses browser window + `</>` instead of generic globe) |
| 7 | `ddos_protection` | Right-side large shield (`PASTEL_BLUE` / `PASTEL_BLUE_LIGHT`) deflecting 3 bouncing arrows | Center `PASTEL_GREEN` + `WHITE` shield core | **Refined** from `ddos_protection` (keeps bouncing arrows, sharpens shield contrast) |
| 8 | `vpn_gateway` | Horizontal rounded tunnel pipe (`PASTEL_BLUE` outer, `WHITE` channel) + left/right arrows | Central `PASTEL_GREEN` padlock | **Adopted** from `original_network/vpn_gateway` |
| 9 | `zero_trust` | Circular continuous verification loop (2 curved `DARK` arrows) around center | Center `PASTEL_GREEN` shield with lock/check inside | **Improved** from `zero_trust_proxy` (replaces abstract H-bars with continuous verification loop) |

### Family 3: Endpoint, Cloud & Data Protection (5 Icons)

| # | Name | Base Silhouette (`PASTEL_BLUE` / `WHITE`) | Security Accent (`PASTEL_GREEN`) | Design Decision vs. Existing |
| :- | :--- | :--- | :--- | :--- |
| 10 | `edr_xdr` | Laptop monitor & keyboard base (`PASTEL_BLUE` bezel, `WHITE` screen) | Heartbeat pulse line on screen + bottom-right `PASTEL_GREEN` shield | **New** |
| 11 | `ids_ips` | 1U rack appliance (`PASTEL_BLUE` outer, `WHITE` panel) + bidirectional arrows | Center `PASTEL_GREEN` shield with `WHITE` inspection eye | **Adopted** from `original_network/ids_ips` |
| 12 | `dlp` | Stacked database cylinder / document card (`PASTEL_BLUE` & `WHITE`) | Outbound arrow blocked by a bottom-right `PASTEL_GREEN` padlock | **New** |
| 13 | `casb` | Fluffy `PASTEL_BLUE` cloud silhouette with `WHITE` inner gate frame | Central `PASTEL_GREEN` policy padlock & checkpoint bars | **New** |
| 14 | `email_security` | Mail envelope (`WHITE` body, `PASTEL_BLUE_LIGHT` top V-flap) | Bottom-right `PASTEL_GREEN` shield with checkmark | **New** |

### Family 4: Cryptography, Keys & Secrets (4 Icons)

| # | Name | Base Silhouette (`PASTEL_BLUE` / `WHITE`) | Security Accent (`PASTEL_GREEN`) | Design Decision vs. Existing |
| :- | :--- | :--- | :--- | :--- |
| 15 | `pki_ca` | Horizontal `WHITE` certificate card with text lines + `PASTEL_BLUE` ribbon tails | Circular `PASTEL_GREEN` medal seal with `WHITE` center | **Adopted** from `original_cloud/certificate_tls` |
| 16 | `hsm_kms` | Square hardware security microchip (`PASTEL_BLUE` package, `WHITE` inner die, 3 pins per side) | Central `PASTEL_GREEN` cryptographic key | **Improved** from `key_management` (replaces plain hexagon with physical HSM microchip + pins) |
| 17 | `secret_vault` | Heavy square bank safe door (`PASTEL_BLUE` frame, `WHITE` door panel, 2 left hinges) | Central `PASTEL_GREEN` 4-spoke rotary combination dial wheel | **Improved** from `secret_vault` (replaces generic padlock with unmistakable bank vault door + dial) |
| 18 | `encryption` | Left `WHITE` plaintext card + right `PASTEL_BLUE` ciphertext/binary card | Central `PASTEL_GREEN` padlock over the left-to-right transform arrow | **New** |

### Family 5: SecOps, SOC & Threat Management (6 Icons)

| # | Name | Base Silhouette (`PASTEL_BLUE` / `WHITE`) | Security Accent (`PASTEL_GREEN`) | Design Decision vs. Existing |
| :- | :--- | :--- | :--- | :--- |
| 19 | `siem` | Top 3 log source dots feeding a `PASTEL_BLUE` funnel into a lower `WHITE` dashboard | `PASTEL_GREEN` alert pulse badge inside the dashboard | **New** |
| 20 | `soar` | Left `PASTEL_BLUE` shield linked to 3 right-side `WHITE` workflow playbook nodes | Central interlocking `PASTEL_GREEN` automation gear | **New** |
| 21 | `soc_center` | Wide multi-screen operations monitor (`PASTEL_BLUE` bezel, `WHITE` split screens + stand) | Left radar circle + right `PASTEL_GREEN` bar chart / status dot | **New** |
| 22 | `threat_intel` | Circular radar scope (`PASTEL_BLUE` outer ring, `WHITE` face, concentric rings & crosshairs) | Diagonal sweep line + glowing `PASTEL_GREEN` target blip dot | **New** |
| 23 | `vulnerability_scan` | Code/server window (`WHITE` body, `PASTEL_BLUE` header bar with dots) | Overlapping bottom-right magnifying glass with `PASTEL_GREEN` lens & bug icon | **Improved** from `security_scan` (scans a system/code window to reveal a bug, instead of scanning a shield) |
| 24 | `honeypot` | Cluster of 3 flat-top hexagons (`PASTEL_BLUE` & `PASTEL_BLUE_LIGHT` outer cells) | Center `PASTEL_GREEN` decoy hexagon + concentric radar trap arcs | **New** |

---

## 4. Implementation & Review Steps

1. **Phase 1 — Provider Scaffolding**:
   - Create `src/drawlib/_icons/png_icons/original_security/` (`__init__.py`, `_base.py`) and wire `original_security` (`OriginalSecurityIcon`) in `src/drawlib/icons.py`, `src/drawlib/_diagrams/`, and `tools/dcli/codegen/`.
2. **Phase 2 — Authoring the 24 Concept Icons (4 Parallel Batches of 6)**:
   - Reuse/copy the 8 existing proven scripts (`pam_bastion`, `directory_service`, `firewall`, `waf`, `ddos_protection`, `vpn_gateway`, `zero_trust`, `ids_ips`, `pki_ca`) and author the 15 new/adapted scripts in `tools/icons_src/original_security/`.
   - Each subagent runs Stage 1 & Stage 2 grid inspection (`-g`) to verify margins (`[9.0, 91.0]`), stroke weights (`w = 2.7`), and clean silhouettes.
3. **Phase 3 — Unified 24-Icon Contact Sheet Review**:
   - Render all 24 icons to `512x512` PNGs, generate a 24-icon contact sheet (`original_security_concepts_sheet.png`), inspect visual balance across all 5 families, and present to the user for approval before proceeding to the 60 vendor logos.
