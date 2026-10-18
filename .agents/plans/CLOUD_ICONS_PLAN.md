# Cloud Icons Plan (`drawlib.icons.cloud` & `drawlib.icons.original_cloud`)

## 1. Objective & Scope

Add a dedicated cloud provider, parent cloud company, and major hosting/PaaS icon suite under `drawlib.icons.cloud` (`CloudIcon`) for official brand logos, and expand `drawlib.icons.original_cloud` (`OriginalCloudIcon`) with 5 pure cloud concept icons and 40 medium-tone (`Tone 3`) vendor counterparts.

- **Modules**:
  - `drawlib.icons.cloud` (`CloudIcon`) — 40 official cloud service, parent tech company, global hosting/VPS/edge, modern PaaS/BaaS, and Japanese cloud/hosting logos (+ shorthand aliases).
  - `drawlib.icons.original_cloud` (`OriginalCloudIcon`) — 102 vendor-neutral cloud & architecture concept icons (97 existing + 5 pure cloud concepts) + 40 2D flat medium-tone vendor counterparts (142 canonical icons total + shorthand aliases).
- **Release Asset Packages**:
  - `icon_cloud` (`tools/release_assets/v0.3/icons/cloud/`)
  - `icon_original_cloud` (`tools/release_assets/v0.3/icons/original_cloud/`)
- **Code Reuse & Independent PNG Folders**:
  - Overlapping icons (`microsoft`, `ibm`, `cloudflare`, `fastly`, `akamai`, `firebase`, `supabase`) reuse the Python drawing scripts from `client`, `server`, `network`, `code`, and `data`.
  - Rendered PNG files and manifests remain completely independent inside `cloud/` and `original_cloud/`.

---

## 2. Canonical `cloud` Icons (40 Official Cloud, Company & Hosting Logos)

| Category | # | Canonical Name | Service / Company / Brand | Shorthand Aliases / Overlap |
| :--- | :- | :--- | :--- | :--- |
| **1. Hyperscale Cloud Platforms** | 1 | `aws` | Amazon Web Services | `amazon_web_services` |
| | 2 | `google_cloud` | Google Cloud (GCP) | `gcp` |
| | 3 | `azure` | Microsoft Azure | `ms_azure`, `microsoft_azure` |
| | 4 | `oracle_cloud` | Oracle Cloud Infrastructure (OCI) | `oci` |
| | 5 | `ibm_cloud` | IBM Cloud | — |
| | 6 | `alibaba_cloud` | Alibaba Cloud (Aliyun) | `aliyun` |
| | 7 | `tencent_cloud` | Tencent Cloud | — |
| | 8 | `huawei_cloud` | Huawei Cloud | — |
| **2. Cloud Parent Companies** | 9 | `amazon` | Amazon.com | `amazon_corp` |
| | 10 | `google` | Google | `alphabet` |
| | 11 | `microsoft` | Microsoft | Reuses `client/microsoft` |
| | 12 | `oracle` | Oracle Corporation | `oracle_corp` |
| | 13 | `ibm` | IBM Corporation | Reuses `server/ibm` |
| | 14 | `alibaba` | Alibaba Group | `alibaba_group` |
| | 15 | `tencent` | Tencent | `tencent_corp` |
| | 16 | `huawei` | Huawei | `huawei_corp` |
| **3. Global Hosting, VPS & Edge** | 17 | `cloudflare` | Cloudflare | Reuses `network/cloudflare` (`cf`) |
| | 18 | `fastly` | Fastly | Reuses `network/fastly` |
| | 19 | `akamai` | Akamai Connected Cloud | Reuses `network/akamai` |
| | 20 | `digitalocean` | DigitalOcean | `do` |
| | 21 | `linode` | Linode (Akamai) | — |
| | 22 | `vultr` | Vultr | — |
| | 23 | `hetzner` | Hetzner Online | — |
| | 24 | `ovhcloud` | OVHcloud | `ovh` |
| | 25 | `scaleway` | Scaleway | — |
| | 26 | `ionos` | 1&1 IONOS | — |
| **4. Modern PaaS, Serverless & BaaS** | 27 | `vercel` | Vercel | — |
| | 28 | `netlify` | Netlify | — |
| | 29 | `heroku` | Heroku | — |
| | 30 | `render` | Render | `render_cloud` |
| | 31 | `fly_io` | Fly.io | `flyio` |
| | 32 | `railway` | Railway | `railway_app` |
| | 33 | `firebase` | Google Firebase | Reuses `code/firebase` |
| | 34 | `supabase` | Supabase | Reuses `data/supabase` |
| **5. Japan Cloud & Hosting** | 35 | `sakura` | Sakura Internet / Sakura Cloud (さくらインターネット) | `sakura_cloud`, `sakura_internet` |
| | 36 | `conoha` | GMO ConoHa | `gmo_conoha` |
| | 37 | `xserver` | Xserver (エックスサーバー) | — |
| | 38 | `nifcloud` | NIFCLOUD / FJcloud-V (ニフクラ) | `fjcloud` |
| | 39 | `idcf` | IDC Frontier (IDCフロンティア) | `idcf_cloud` |
| | 40 | `kagoya` | KAGOYA JAPAN (カゴヤ・ジャパン) | `kagoya_cloud` |

---

## 3. Canonical `original_cloud` Additions (5 Pure Cloud Concepts + 40 Medium-Tone Logos)

### Part A: Pure Cloud Concept Icons (5 New Icons added to existing 97)

| # | Canonical Name | Shorthand Aliases | 2D Medium-Tone Motif (`PASTEL_BLUE` / `PASTEL_GREEN` / `WHITE`) |
| :- | :--- | :--- | :--- |
| 1 | `cloud` | `generic_cloud`, `cloud_computing` | Clean classic cloud silhouette (`PASTEL_BLUE`) with subtle `WHITE` inner highlight and `DARK` border |
| 2 | `public_cloud` | — | Open `PASTEL_BLUE` cloud with `WHITE` / `PASTEL_GREEN` globe/network access nodes |
| 3 | `private_cloud` | `vpc_cloud` | `PASTEL_BLUE` cloud protected by a `PASTEL_GREEN` / `WHITE` security shield & lock |
| 4 | `hybrid_cloud` | — | `PASTEL_BLUE` cloud connected bidirectionally to an on-premises `WHITE` / `PASTEL_GREEN` server rack |
| 5 | `multi_cloud` | `multicloud` | Overlapping dual/triple clouds (`PASTEL_BLUE`, `PASTEL_GREEN`, `WHITE`) representing multi-provider topology |

### Part B: 2D Medium-Tone Brand Logos (40 Icons)
- Every icon in `cloud` (1–40) has a matching 2D flat medium-tone (`Tone 3`) counterpart in `original_cloud`.
- **Mandatory Style Rule**: Each `original_cloud` brand icon preserves its official brand color hue adjusted to Medium Tone (`L ≈ 59%–66%`, `S ≈ 50%–65%`) with `DARK = "#323A48"` outlines (`w = 2.0`).

---

## 4. Implementation Steps (3-Step Workflow)

1. **Step 1 — Reference Image Collection**:
   - Collect official SVG/PNG brand logos for all 40 `cloud` icons into `tools/original_assets/cloud/<name>/`.
   - Rasterize reference previews into `.drawlib/scratch/cloud_ref/<name>_ref.png` and build a 40-icon reference contact sheet.
2. **Step 2 — Official `cloud` Icons**:
   - Reuse the 7 existing overlapping scripts and author the 33 new scripts in `tools/icons_src/cloud/<name>_default.py`.
   - Render `tools/release_assets/v0.3/icons/cloud/<name>_default.png`, normalize to `512 × 512`, and compare side-by-side against `_ref.png`.
3. **Step 3 — `original_cloud` Medium-Tone Icons & Wiring**:
   - Author the 5 pure cloud concept icons and 33 new medium-tone brand scripts in `tools/icons_src/original_cloud/` (reusing the 7 overlapping `original_*` scripts).
   - Wire `drawlib.icons.cloud` (`CloudIcon`) and `drawlib.icons.original_cloud` (`OriginalCloudIcon`) across `src/drawlib/`, `tools/dcli/`, `tests/`, and docs.
   - Build `icon_cloud.zip` and `icon_original_cloud.zip`, sync `_release_assets.py`, and run `./dcli code-check all` and `./dcli test target icons diagrams`.
