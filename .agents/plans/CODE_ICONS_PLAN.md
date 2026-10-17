# Code Icons Plan (`drawlib.icons.code` & `drawlib.icons.original_code`)

## 1. Objective & Scope

Add a dedicated programming, framework, runtime, API, and IDE icon suite under `drawlib.icons.code` (`CodeIcon`) for official brand/OSS logos, and `drawlib.icons.original_code` (`OriginalCodeIcon`) combining vendor-neutral software architecture / code concept icons with 2D flat pastel counterparts of the official logos.

- **Modules**:
  - `drawlib.icons.code` (`CodeIcon`) — 72 official language, runtime, framework, API, Google platform, and IDE logos (+ shorthand aliases).
  - `drawlib.icons.original_code` (`OriginalCodeIcon`) — 24 vendor-neutral software/code concept icons + 72 2D flat pastel counterparts (96 canonical icons total + shorthand aliases).
- **Tiered Priority Design**:
  - **Tier 1 (Heavily Weighted)**: **Python** (14 icons + Colab) and **JavaScript / TypeScript** (21 icons) cover languages, runtimes, major frontend/backend frameworks (`react`, `fastapi`, `htmx`, `jquery`, etc.), ORMs, validation, testing, and package tools.
  - **Tier 2 (Priority 5 Ecosystems)**: **Go**, **Java / Kotlin**, **Rust**, **C# / .NET**, and **PHP / Ruby** (17 icons) include both the language logos and their flagship frameworks/build tools.
  - **Tier 3 (Systems, Mobile, Web, APIs & Google/IDEs)**: Covers C/C++, Swift/Dart/Flutter, HTML/CSS/Wasm, GraphQL/gRPC/Protobuf, Google developer stack (`firebase`, `colab`, `android_studio`, `antigravity`), and IDEs (`vscode`, `intellij`).
- **Release Asset Packages**:
  - `icon_code` (`tools/release_assets/v0.3/icons/code/`)
  - `icon_original_code` (`tools/release_assets/v0.3/icons/original_code/`)
- **Separation & Zero-Overlap Policy**:
  - Zero overlap with `cnative` (`docker`, `kubernetes`, `helm`, `envoy`), `data` (`postgresql`, `redis`, `kafka`), `devops` (`git`, `github`, `postman`, `playwright`), or `ai` (`pytorch`, `tensorflow`, `jupyter`, `streamlit`).
  - If any icon script is ever shared across suites, the Python script may be reused, while output PNG asset folders (`code/`, `original_code/`) remain completely independent.

---

## 2. Canonical `code` Icons (72 Official Logos — 6 Rows × 12 Columns)

### Tier 1A: Python Ecosystem (14 Icons)

| # | Canonical Name | Library / Tool | Shorthand Aliases | Role |
| :- | :--- | :--- | :--- | :--- |
| 1 | `python` | Python | `py` | Core Language |
| 2 | `fastapi` | FastAPI | — | Modern Async API Framework |
| 3 | `django` | Django | — | Full-Stack Web Framework |
| 4 | `flask` | Flask | — | Lightweight Web Framework |
| 5 | `uvicorn` | Uvicorn | — | ASGI Web Server |
| 6 | `uv` | Astral uv | — | Fast Python Package & Project Manager |
| 7 | `poetry` | Poetry | — | Python Dependency Manager |
| 8 | `pypi` | PyPI | — | Python Package Index |
| 9 | `pydantic` | Pydantic | — | Data Validation & Settings |
| 10 | `sqlalchemy` | SQLAlchemy | — | Python SQL Toolkit & ORM |
| 11 | `celery` | Celery | — | Distributed Task Queue |
| 12 | `pytest` | pytest | — | Python Testing Framework |
| 13 | `numpy` | NumPy | — | Scientific Array Computing |
| 14 | `pandas` | pandas | — | DataFrame & Data Analysis |

### Tier 1B: JavaScript & TypeScript Ecosystem (21 Icons)

| # | Canonical Name | Library / Tool | Shorthand Aliases | Role |
| :- | :--- | :--- | :--- | :--- |
| 15 | `javascript` | JavaScript | `js` | Core Web Language |
| 16 | `typescript` | TypeScript | `ts` | Typed JavaScript |
| 17 | `nodejs` | Node.js | `node` | JS Server Runtime |
| 18 | `deno` | Deno | — | Secure TS/JS Runtime |
| 19 | `bun` | Bun | — | All-in-One JS Runtime & Bundler |
| 20 | `react` | React | `reactjs` | Component UI Library |
| 21 | `nextjs` | Next.js | `next` | React Full-Stack Framework |
| 22 | `vuejs` | Vue.js | `vue` | Progressive UI Framework |
| 23 | `nuxt` | Nuxt | `nuxtjs` | Vue Full-Stack Framework |
| 24 | `angular` | Angular | — | Google Enterprise Web Framework |
| 25 | `svelte` | Svelte | — | Compiler-Based UI Framework |
| 26 | `astro` | Astro | — | Content-Driven Web Framework |
| 27 | `htmx` | htmx | — | Hypermedia-Driven HTML Extensions |
| 28 | `jquery` | jQuery | — | Classic DOM & Utility Library |
| 29 | `tailwind_css` | Tailwind CSS | `tailwind` | Utility-First CSS Framework |
| 30 | `vite` | Vite | `vitejs` | Next-Gen Frontend Build Tool |
| 31 | `nestjs` | NestJS | `nest` | Enterprise Node.js Framework |
| 32 | `express` | Express | `expressjs` | Classic Node.js Web Framework |
| 33 | `hono` | Hono | — | Ultrafast Edge / Web Standard Framework |
| 34 | `prisma` | Prisma | — | TypeScript / Node.js ORM |
| 35 | `npm` | npm | — | Node Package Manager |

### Tier 2: Priority 5 Backend Ecosystems (17 Icons)

| Ecosystem | # | Canonical Name | Language / Framework / Tool | Shorthand Aliases |
| :--- | :- | :--- | :--- | :--- |
| **Go** | 36 | `go` | Go (Golang) | `golang` |
| | 37 | `gin` | Gin Web Framework | `gin_gonic` |
| | 38 | `echo` | Echo Go Framework | `echo_go` |
| **Java / Kotlin** | 39 | `java` | Java | `openjdk`, `jvm` |
| | 40 | `kotlin` | Kotlin | `kt` |
| | 41 | `spring` | Spring / Spring Boot | `spring_boot` |
| | 42 | `gradle` | Gradle Build Tool | — |
| **Rust** | 43 | `rust` | Rust | `rs` |
| | 44 | `cargo` | Cargo | — |
| | 45 | `tokio` | Tokio Async Runtime | — |
| **C# / .NET** | 46 | `csharp` | C# | `cs` |
| | 47 | `dotnet` | Microsoft .NET | `net`, `aspnet` |
| | 48 | `blazor` | Blazor | — |
| **PHP / Ruby** | 49 | `php` | PHP | — |
| | 50 | `laravel` | Laravel | — |
| | 51 | `ruby` | Ruby | `rb` |
| | 52 | `rails` | Ruby on Rails | `ruby_on_rails` |

### Tier 3A: Systems, Mobile & Web Standards (10 Icons)

| # | Canonical Name | Language / Standard | Shorthand Aliases | Role |
| :- | :--- | :--- | :--- | :--- |
| 53 | `c` | C Language | `c_lang` | Systems Programming |
| 54 | `cpp` | C++ | `cplusplus` | High-Performance Systems |
| 55 | `bash` | GNU Bash / Shell | `sh`, `shell` | Shell Scripting |
| 56 | `swift` | Swift | — | Apple iOS / macOS Language |
| 57 | `dart` | Dart | — | Google Client-Optimized Language |
| 58 | `flutter` | Flutter | — | Google Cross-Platform UI SDK |
| 59 | `react_native` | React Native | `rn` | Cross-Platform Mobile Framework |
| 60 | `html5` | HTML5 | `html` | Web Markup Standard |
| 61 | `css3` | CSS3 | `css` | Web Styling Standard |
| 62 | `webassembly` | WebAssembly | `wasm` | Portable Binary Instruction Format |

### Tier 3B: APIs, Google Platforms & IDEs (10 Icons)

| # | Canonical Name | Platform / Tool | Shorthand Aliases | Role |
| :- | :--- | :--- | :--- | :--- |
| 63 | `graphql` | GraphQL | `gql` | Query Language for APIs |
| 64 | `grpc` | gRPC | — | High-Performance RPC (Google-originated) |
| 65 | `openapi` | OpenAPI / Swagger | `swagger` | REST API Specification |
| 66 | `protobuf` | Protocol Buffers | `proto` | Binary Serialization (Google) |
| 67 | `firebase` | Firebase | — | Google App Development Platform & SDK |
| 68 | `colab` | Google Colaboratory | `google_colab` | Hosted Python Notebook Environment |
| 69 | `antigravity` | Antigravity | — | Agentic AI Coding IDE (Google DeepMind) |
| 70 | `android_studio` | Android Studio | — | Official Android & Kotlin/Flutter IDE |
| 71 | `vscode` | Visual Studio Code | `vs_code` | Lightweight Extensible Code Editor |
| 72 | `intellij` | JetBrains IntelliJ IDEA | `jetbrains` | JVM & Polyglot IDE |

---

## 3. Canonical `original_code` Icons (24 Concept Icons + 72 Pastel Logos = 96 Icons)

### Part A: Vendor-Neutral Software & Code Concept Icons (24 Icons)

| Category | # | Canonical Name | Shorthand Aliases | 2D Pastel Motif (`PASTEL_BLUE` / `PASTEL_GREEN` / `WHITE`) |
| :--- | :- | :--- | :--- | :--- |
| **1. Source & Modules** | 1 | `source_code` | `code_file`, `script` | Document sheet (`WHITE`) with top corner fold + central `PASTEL_BLUE` / `PASTEL_GREEN` `</>` brackets |
| | 2 | `sdk_library` | `sdk`, `library` | Open modular book / layer stack + `PASTEL_GREEN` puzzle connector piece |
| | 3 | `package_module` | `package`, `module`, `dependency` | Isometric 3D parcel cube (`PASTEL_BLUE` / `WHITE`) with `PASTEL_GREEN` code tag |
| | 4 | `cli_tool` | `cli`, `terminal`, `command_line` | Terminal window frame (`PASTEL_BLUE` header, `WHITE` body) + `PASTEL_GREEN` `>_` prompt |
| | 5 | `ide_editor` | `ide`, `code_editor` | Split-pane editor window (`WHITE` + `PASTEL_BLUE` sidebar) with colored syntax bars |
| **2. APIs & Protocols** | 6 | `rest_api` | `http_api`, `endpoint` | Service window + central `{}` JSON badge & bidirectional `PASTEL_GREEN` HTTP arrows |
| | 7 | `graphql_api` | `query_api` | Hexagon query graph (`PASTEL_BLUE`) with `PASTEL_GREEN` & `WHITE` vertex nodes |
| | 8 | `rpc_call` | `remote_procedure`, `binary_rpc` | Left & right service blocks linked by a fast `PASTEL_GREEN` lightning call arrow |
| | 9 | `websocket` | `realtime_stream`, `socket` | Open persistent pipe (`PASTEL_BLUE`) with simultaneous two-way `PASTEL_GREEN` arrows |
| | 10 | `webhook` | `callback_hook`, `event_hook` | Event trigger node firing into a curved interlocking `PASTEL_GREEN` hook |
| **3. App Architecture** | 11 | `microservice` | `service_node` | Hexagonal service cell (`PASTEL_BLUE`) with 3 `PASTEL_GREEN` external port connectors |
| | 12 | `monolith` | `monolithic_app` | Solid unified 3-tier block (`PASTEL_BLUE` / `PASTEL_BLUE_LIGHT` / `PASTEL_GREEN`) inside one frame |
| | 13 | `serverless_func` | `faas`, `lambda_func` | Rounded card with `f(x)` / `{}` brackets + `PASTEL_GREEN` lightning bolt |
| | 14 | `background_worker` | `async_worker`, `job_worker` | Task card stack (`WHITE`) + interlocking `PASTEL_GREEN` processing gear |
| | 15 | `cron_job` | `scheduled_task`, `timer_job` | Clock face (`WHITE` / `PASTEL_BLUE`) + bottom-right `PASTEL_GREEN` play/code badge |
| **4. Build, Run & Test** | 16 | `compiler_build` | `compiler`, `bundler`, `transpiler` | Code sheet entering a `PASTEL_BLUE` funnel/gear and outputting a `PASTEL_GREEN` binary cube |
| | 17 | `runtime_vm` | `runtime`, `interpreter`, `bytecode_vm` | Engine frame (`PASTEL_BLUE`) executing stacked `WHITE` & `PASTEL_GREEN` instruction bars |
| | 18 | `unit_test` | `test_suite`, `assertion` | Code checklist / lab flask (`WHITE` / `PASTEL_BLUE`) + `PASTEL_GREEN` pass checkmark |
| | 19 | `debugger` | `breakpoint`, `bug_fix` | Magnifying lens / crosshair (`PASTEL_BLUE`) inspecting a `PASTEL_GREEN` bug silhouette |
| | 20 | `linter_formatter` | `linter`, `formatter`, `static_analysis` | Aligned code bars (`WHITE` / `PASTEL_BLUE`) + `PASTEL_GREEN` alignment wand/check |
| **5. Data & Formats** | 21 | `json_schema` | `json_data`, `serialized_payload` | Rounded card (`WHITE`) with bold `PASTEL_BLUE` `{` `}` braces & `PASTEL_GREEN` key-value dots |
| | 22 | `xml_markup` | `markup_doc`, `dom_tree` | Document card (`WHITE`) with `PASTEL_BLUE` `< />` tag & `PASTEL_GREEN` hierarchy node |
| | 23 | `binary_executable` | `binary`, `executable`, `bytecode` | Chip/module frame (`PASTEL_BLUE`) containing crisp `0 1 / 1 0` geometric shapes |
| | 24 | `regex_parser` | `regex`, `lexer`, `parser` | Filter lens (`PASTEL_GREEN`) over text lines highlighting a matched pattern segment |

### Part B: 2D Flat Pastel Logos (72 Icons)
- Every icon in `code` (1–72) has a matching 2D flat pastel counterpart in `original_code`.
- **Mandatory Brand Color Rule**: Each `original_code` logo preserves its official brand color palette softened into Drawlib pastel tones with `DARK = "#323A48"` outlines (`w = 1.9`).

---

## 4. Implementation & Verification Workflow

1. **Phase 1 — Official Reference Collection & Provider Wiring**:
   - Download official SVG/PNG brand logos for all 72 `code` icons into `tools/original_assets/code/` and rasterize `.drawlib/scratch/code_ref/<name>_ref.png`.
   - Wire `code` (`CodeIcon`) and `original_code` (`OriginalCodeIcon`) in `src/drawlib/_icons/png_icons/`, `src/drawlib/icons.py`, `src/drawlib/diagrams/architecture.py`, `src/drawlib/diagrams/sequence.py`, and `tools/dcli/codegen/`.
2. **Phase 2 — `code` Official Logos (6 Parallel Batches of 12)**:
   - Author `tools/icons_src/code/<name>_default.py` using pure Drawlib vector primitives (no `image()`, no `text()`).
   - Verify each with `-g` grid inspection against `_ref.png` and render the 72-icon (6×12) `code_icons_contact_sheet.png`.
3. **Phase 3 — `original_code` Concepts (24) & Pastel Logos (72)**:
   - Author the 24 concept icons first, verify on a 24-icon (2×12) concept sheet, then author the 72 2D flat pastel vendor logos.
   - Run `./dcli codegen icon-code` and `./dcli codegen icon-original-code`, sync `_cached_assets` and `_release_assets.py`, run `./dcli code-check all` and `./dcli test target icons diagrams`.
