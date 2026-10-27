# Drawlib Code Icons Guidelines (`lib-icons-code`)

API specification and complete catalog for `drawlib.icons.code` (`CodeIcon`, **97** official programming language, web/backend framework, runtime, API protocol, and IDE logos) and `drawlib.icons.original_code` (`OriginalCodeIcon`, **121** flat 2D pastel icons: **97** brand twins + **24** vendor-neutral software engineering and API concept icons). See `lib-icons-overview` for cross-tier icon rules.

---

## 1. API Signature & Twin Module Structure

Every icon function is **Center-Anchored at `xy = (cx, cy)`** with a `1:1` square aspect ratio and requires `*, style: Style` as a mandatory keyword-only argument:

```python
from drawlib.diagrams.architecture import CodeIcon, Node, OriginalCodeIcon
from drawlib.icons import code, code_icon, original_code, original_code_icon
from drawlib.styles import Styles

# 1. Direct module function calls (center-anchored at (cx, cy); style is required)
code.python((30, 25), width=9.0, style=Styles.Primary)
original_code.python((55, 25), width=9.0, style=Styles.Primary)
original_code.rest_api((80, 25), width=9.0, style=Styles.Primary)

# 2. Dynamic string/Enum dispatchers
code_icon((30, 10), width=9.0, name="fastapi", style=Styles.Primary)
original_code_icon((55, 10), width=9.0, name="microservice", style=Styles.Primary)

# 3. High-level ArchitectureDiagram Node integration via Enum
ui_node = Node("Next.js App", width=24, height=18, icon=CodeIcon.NEXTJS, icon_size=7.5)
worker_node = Node("Async Worker", width=24, height=18, icon=OriginalCodeIcon.BACKGROUND_WORKER, icon_size=7.5)
```

| Module | Diagram Enum | Canonical Count | Asset Archive | Visual Purpose |
| :--- | :--- | :---: | :--- | :--- |
| `drawlib.icons.code` | `CodeIcon` | **97** | `icon_code` | Official logos for programming languages, frontend/backend frameworks, build toolchains, API protocols, and IDEs. |
| `drawlib.icons.original_code` | `OriginalCodeIcon` | **121** (`97` + `24`) | `icon_original_code` | Flat 2D pastel twins for all 97 brands plus **24 vendor-neutral software & API concept icons**. |

---

## 2. Complete 97 Shared Brand Icons (`code.*` & `original_code.*`)

| Category | Count | Canonical Function Names (`code.*` & `original_code.*`) |
| :--- | :---: | :--- |
| **Programming & Markup Languages** | 25 | `bash`, `c`, `cpp`, `csharp`, `css3`, `dart`, `elixir`, `go`, `html5`, `java`, `javascript`, `julia`, `kotlin`, `lua`, `php`, `python`, `r`, `ruby`, `rust`, `scala`, `solidity`, `sql`, `swift`, `typescript`, `zig` |
| **Frontend, Mobile & Desktop UI Frameworks** | 18 | `angular`, `astro`, `blazor`, `electron`, `expo`, `flutter`, `htmx`, `jquery`, `nextjs`, `nuxt`, `react`, `react_native`, `remix`, `storybook`, `svelte`, `tailwind_css`, `tauri`, `vuejs` |
| **Backend, Web & Systems Frameworks** | 21 | `appwrite`, `axum`, `celery`, `convex`, `django`, `dotnet`, `echo`, `express`, `fastapi`, `firebase`, `flask`, `gin`, `hono`, `laravel`, `nestjs`, `pocketbase`, `quarkus`, `rails`, `spring`, `tokio`, `uvicorn` |
| **Runtimes, Package Managers & Build Toolchains** | 14 | `biome`, `bun`, `cargo`, `deno`, `gradle`, `nodejs`, `npm`, `pnpm`, `poetry`, `pypi`, `uv`, `vite`, `webassembly`, `yarn` |
| **APIs, Data Access, Scientific & Testing Libraries** | 14 | `apollo`, `graphql`, `grpc`, `hasura`, `numpy`, `openapi`, `pandas`, `prisma`, `protobuf`, `pydantic`, `pytest`, `sqlalchemy`, `trpc`, `vitest` |
| **IDEs, Editors & Cloud Notebooks** | 5 | `android_studio`, `antigravity`, `colab`, `intellij`, `vscode` |

---

## 3. Complete 24 Vendor-Neutral Software & API Concept Icons (`original_code.*` Only)

| Category | Count | Canonical Function Names (`original_code.*` / `OriginalCodeIcon.*`) |
| :--- | :---: | :--- |
| **API Protocols, Schemas & Streaming** | 7 | `graphql_api`, `json_schema`, `rest_api`, `rpc_call`, `webhook`, `websocket`, `xml_markup` |
| **Service Archetypes & Execution Models** | 5 | `background_worker`, `cron_job`, `microservice`, `monolith`, `serverless_func` |
| **Runtimes, Binaries, SDKs & Tooling** | 12 | `binary_executable`, `cli_tool`, `compiler_build`, `debugger`, `ide_editor`, `linter_formatter`, `package_module`, `regex_parser`, `runtime_vm`, `sdk_library`, `source_code`, `unit_test` |

```drawlib code=fold align=center file=icons_code_rules_arch.png caption="Polyglot Full-Stack & Microservice Topology Using CodeIcon and OriginalCodeIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    CodeIcon,
    Node,
    NodeGroup,
    OriginalCodeIcon,
)
from drawlib.styles import Styles

setup(width=136, height=58)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

web = d.add(
    Node("Next.js\nFrontend", width=24, height=18, icon=CodeIcon.NEXTJS, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
backend = d.add(NodeGroup(title="Polyglot Backend Services", padding=4.5), xy=(42, 4))
api = backend.add(Node("FastAPI\nGateway", width=24, height=18, icon=CodeIcon.FASTAPI, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(14, 14))
worker = backend.add(Node("Rust Async\nWorker", width=24, height=18, icon=OriginalCodeIcon.BACKGROUND_WORKER, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(54, 14))

d.connect(web, api, label="REST", padding=1.5)
d.connect(api, worker, label="gRPC", padding=1.5)
d.draw(xy=(4, 4))
save()
```
