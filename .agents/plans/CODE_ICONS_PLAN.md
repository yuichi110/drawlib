# Code Icons Plan (`drawlib.icons.code` & `drawlib.icons.original_code`)

## 1. Objective & Scope

Add a dedicated programming, framework, runtime, API, and developer-tool icon suite under `drawlib.icons.code` (`CodeIcon`) for official brand/OSS logos, and `drawlib.icons.original_code` (`OriginalCodeIcon`) combining vendor-neutral software architecture / code concept icons with 2D flat pastel counterparts of the official logos.

- **Modules**:
  - `drawlib.icons.code` (`CodeIcon`) — 60 official language, runtime, framework, API, and IDE logos (+ shorthand aliases).
  - `drawlib.icons.original_code` (`OriginalCodeIcon`) — 24 vendor-neutral software/code concept icons + 60 2D flat pastel counterparts (84 canonical icons total + shorthand aliases).
- **Release Asset Packages**:
  - `icon_code` (`tools/release_assets/v0.3/icons/code/`)
  - `icon_original_code` (`tools/release_assets/v0.3/icons/original_code/`)
- **Separation & Zero-Overlap Policy**:
  - Zero overlap with `cnative` (`docker`, `kubernetes`, `helm`, `envoy`), `data` (`postgresql`, `redis`, `kafka`, `graphql` is NOT in `data`), `devops` (`git`, `github`, `postman`, `playwright`), or `ai` (`pytorch`, `tensorflow`, `jupyter`, `streamlit`).
  - If any icon script is ever shared across suites, the Python script may be reused, while output PNG asset folders (`code/`, `original_code/`) remain completely independent.

---

## 2. Canonical `code` Icons (60 Official Language, Framework, API & IDE Logos)

| Category | # | Canonical Name | Language / Framework / Tool | Shorthand Aliases |
| :--- | :- | :--- | :--- | :--- |
| **1. Core & Systems Languages** | 1 | `python` | Python | `py` |
| | 2 | `javascript` | JavaScript (ES6+) | `js` |
| | 3 | `typescript` | TypeScript | `ts` |
| | 4 | `go` | Go (Golang) | `golang` |
| | 5 | `rust` | Rust | `rs` |
| | 6 | `java` | Java | — |
| | 7 | `c` | C Language | `c_lang` |
| | 8 | `cpp` | C++ | `cplusplus` |
| | 9 | `csharp` | C# | `cs` |
| | 10 | `zig` | Zig | — |
| **2. App, Scripting & Functional** | 11 | `kotlin` | Kotlin | `kt` |
| | 12 | `swift` | Swift | — |
| | 13 | `dart` | Dart | — |
| | 14 | `php` | PHP | — |
| | 15 | `ruby` | Ruby | `rb` |
| | 16 | `scala` | Scala | — |
| | 17 | `elixir` | Elixir | `ex` |
| | 18 | `lua` | Lua | — |
| | 19 | `r_lang` | R Project | `r` |
| | 20 | `bash` | GNU Bash / Shell | `sh`, `shell` |
| **3. Runtimes, Web & Compilers** | 21 | `nodejs` | Node.js | `node` |
| | 22 | `deno` | Deno | — |
| | 23 | `bun` | Bun | — |
| | 24 | `webassembly` | WebAssembly (Wasm) | `wasm` |
| | 25 | `html5` | HTML5 | `html` |
| | 26 | `css3` | CSS3 | `css` |
| | 27 | `markdown` | Markdown | `md` |
| | 28 | `llvm` | LLVM Compiler Infrastructure | — |
| | 29 | `openjdk` | OpenJDK / JVM | `jvm` |
| | 30 | `dotnet` | Microsoft .NET | `net` |
| **4. Frontend & UI Frameworks** | 31 | `react` | React | `reactjs` |
| | 32 | `nextjs` | Next.js | `next` |
| | 33 | `vuejs` | Vue.js | `vue` |
| | 34 | `nuxt` | Nuxt | `nuxtjs` |
| | 35 | `angular` | Angular | — |
| | 36 | `svelte` | Svelte | — |
| | 37 | `solidjs` | SolidJS | `solid` |
| | 38 | `astro` | Astro | — |
| | 39 | `tailwind_css` | Tailwind CSS | `tailwind` |
| | 40 | `vite` | Vite | `vitejs` |
| **5. Backend & Mobile Frameworks** | 41 | `fastapi` | FastAPI | — |
| | 42 | `django` | Django | — |
| | 43 | `flask` | Flask | — |
| | 44 | `spring` | Spring / Spring Boot | `spring_boot` |
| | 45 | `nestjs` | NestJS | `nest` |
| | 46 | `express` | Express.js | `expressjs` |
| | 47 | `rails` | Ruby on Rails | `ruby_on_rails` |
| | 48 | `laravel` | Laravel | — |
| | 49 | `flutter` | Flutter | — |
| | 50 | `react_native` | React Native | `rn` |
| **6. APIs, Package Tools & IDEs** | 51 | `graphql` | GraphQL | `gql` |
| | 52 | `grpc` | gRPC | — |
| | 53 | `openapi` | OpenAPI / Swagger | `swagger` |
| | 54 | `npm` | npm | — |
| | 55 | `pnpm` | pnpm | — |
| | 56 | `yarn` | Yarn | — |
| | 57 | `uv` | Astral uv | — |
| | 58 | `vscode` | Visual Studio Code | `vs_code` |
| | 59 | `intellij` | JetBrains IntelliJ IDEA | `jetbrains` |
| | 60 | `neovim` | Neovim | `nvim`, `vim` |

---

## 3. Canonical `original_code` Icons (24 Concept Icons + 60 Pastel Logos = 84 Icons)

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

### Part B: 2D Flat Pastel Logos (60 Icons)
- Every icon in `code` (1–60) has a matching 2D flat pastel counterpart in `original_code`.
- **Mandatory Brand Color Rule**: Each `original_code` logo preserves its official brand color palette softened into Drawlib pastel tones with `DARK = "#323A48"` outlines (`w = 1.9`).

---

## 4. Implementation & Verification Workflow

1. **Phase 1 — Official Reference Collection & Provider Wiring**:
   - Download official SVG/PNG brand logos for all 60 `code` icons into `tools/original_assets/code/` and rasterize `.drawlib/scratch/code_ref/<name>_ref.png`.
   - Wire `code` (`CodeIcon`) and `original_code` (`OriginalCodeIcon`) in `src/drawlib/_icons/png_icons/`, `src/drawlib/icons.py`, `src/drawlib/diagrams/architecture.py`, `src/drawlib/diagrams/sequence.py`, and `tools/dcli/codegen/`.
2. **Phase 2 — `code` Official Logos (6 Parallel Batches of 10)**:
   - Author `tools/icons_src/code/<name>_default.py` using pure Drawlib vector primitives (no `image()`, no `text()`).
   - Verify each with `-g` grid inspection against `_ref.png` and render the 60-icon `code_icons_contact_sheet.png`.
3. **Phase 3 — `original_code` Concepts (24) & Pastel Logos (60)**:
   - Author the 24 concept icons first, verify on a 24-icon concept sheet, then author the 60 2D flat pastel vendor logos.
   - Run `./dcli codegen icon-code` and `./dcli codegen icon-original-code`, sync `_cached_assets` and `_release_assets.py`, run `./dcli code-check all` and `./dcli test target icons diagrams`.
