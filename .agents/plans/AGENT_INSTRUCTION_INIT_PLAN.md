# AI Agent Instruction Initialization (`drawlib init agent`) Plan

## 1. Overview & Motivation

AI coding agents (Google Antigravity, Claude Code, Cursor, GitHub Copilot, Windsurf, Cline, Roo Code, OpenAI Codex CLI, Gemini CLI) use different directory structures, file extensions (`.md`, `.mdc`, `.instructions.md`), YAML frontmatter schemas, and character limits. Previously, users had to manually copy-paste a static prompt snippet and hand-craft tool-specific frontmatter.

This feature adds **`drawlib init agent`** to the CLI and corresponding programmatic helpers to **`drawlib.tools`**, generating ready-to-use, tool-idiomatic Drawlib instruction files directly in a project repository or user global configuration directory.

---

## 2. CLI Specification (`drawlib init agent`)

Integrated under the `drawlib init` sub-application (`src/drawlib/_cli/commands/init.py`, with hidden plural alias `drawlib init agents`):

```bash
# Generate rule file(s) for one or more specific agents (default mode: auto)
drawlib init agent antigravity
drawlib init agent claude cursor copilot

# Unconditional ("always on") loading mode for dedicated diagram/doc repositories
drawlib init agent antigravity --mode always

# Generate all modular per-agent rule files in one command
drawlib init agent all

# Auto-detect existing agent directories/files in the workspace and initialize them
drawlib init agent --detect

# Install into user-level global configuration directory (~/.gemini/..., ~/.claude/..., etc.)
drawlib init agent antigravity --global

# List supported AI agent targets, output paths, and frontmatter formats
drawlib init agent --list          # (also supports positional `drawlib init agent list`)

# Custom target workspace directory, explicit file path, and force update
drawlib init agent antigravity -d ./my-repo -f
drawlib init agent cursor -o custom/drawlib.mdc
```

### Options Summary

| Argument / Option | Shorthand | Default | Description |
| :--- | :--- | :--- | :--- |
| `[AGENTS...]` | — | `None` | One or more agent names (space- or comma-separated), `all`, or `list`. |
| `--mode` | `-m` | `auto` | Activation mode: `auto` (on-demand / task-relevant loading) or `always` (unconditional). |
| `--global` | `-g` | `False` | Install into user home global agent rules path instead of project workspace. |
| `--detect` | — | `False` | Detect existing agent config directories/files in `--dir` and generate rules for them. |
| `--list` | — | `False` | Print table of supported agents, paths, and formats, then exit. |
| `--dir` | `-d` | `.` | Workspace root directory for project-scoped output and `--detect`. |
| `--output` | `-o` | `None` | Explicit destination file path (valid only when a single agent is specified). |
| `--force` | `-f` | `False` | Overwrite existing dedicated rule files or update existing marker blocks in shared files. |

---

## 3. Supported AI Agent Matrix & File Semantics

Modular per-agent rule files (`rules/drawlib.*`) are prioritized so existing root files (`CLAUDE.md`, `.github/copilot-instructions.md`) are never clobbered. Shared single-file targets (`AGENTS.md`, `GEMINI.md`, Windsurf `global_rules.md`) use non-destructive HTML comment marker blocks (`<!-- drawlib-agent-instruction:start -->` ... `<!-- drawlib-agent-instruction:end -->`).

| Target (`<agent>`) | Aliases | Project Path | Global Path (`-g`) | Format & Frontmatter (`auto` vs `always`) | Merge Mode |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`antigravity`** | `jetski` | `.agents/rules/drawlib.md` *(auto-selects `.agent/rules/drawlib.md` if `.agent/` exists and `.agents/` does not)* | `~/.gemini/config/rules/drawlib.md` | YAML frontmatter required:<br>• `auto`: `trigger: model_decision` + `description`<br>• `always`: `trigger: always_on` | Dedicated |
| **`claude`** | `claude-code` | `.claude/rules/drawlib.md` | `~/.claude/rules/drawlib.md` | Standard Markdown (modular `.claude/rules/` avoids modifying root `CLAUDE.md`) | Dedicated |
| **`cursor`** | — | `.cursor/rules/drawlib.mdc` | *(Unsupported — IDE UI setting)* | MDC YAML frontmatter:<br>• `auto`: `description` + `alwaysApply: false`<br>• `always`: `description` + `alwaysApply: true` | Dedicated |
| **`copilot`** | `github-copilot` | `.github/instructions/drawlib.instructions.md` | *(Unsupported — repo/IDE setting)* | YAML frontmatter:<br>• `auto`: `description` + `applyTo: "**/*_src/**, **/*.md, **/*.py, **/drawlib.toml"`<br>• `always`: `description` + `applyTo: "**"` | Dedicated |
| **`windsurf`** | `cascade` | `.windsurf/rules/drawlib.md` | `~/.codeium/windsurf/memories/global_rules.md` *(marker merge, plain MD)* | Project YAML frontmatter:<br>• `auto`: `trigger: model_decision` + `description`<br>• `always`: `trigger: always_on` | Dedicated (Project) / Marker (Global) |
| **`cline`** | — | `.clinerules/drawlib.md` | `~/Documents/Cline/Rules/drawlib.md` | Standard Markdown (errors cleanly if legacy `.clinerules` regular file blocks directory creation) | Dedicated |
| **`roo`** | `roo-code`, `roocode` | `.roo/rules/drawlib.md` | `~/.roo/rules/drawlib.md` | Standard Markdown | Dedicated |
| **`codex`** | `agents-md`, `agents` | `AGENTS.md` | `~/.codex/AGENTS.md` | Plain Markdown wrapped in `<!-- drawlib-agent-instruction:start/end -->` markers | Marker Merge |
| **`gemini`** | `gemini-cli`, `gemini-md` | `GEMINI.md` | `~/.gemini/GEMINI.md` | Plain Markdown wrapped in `<!-- drawlib-agent-instruction:start/end -->` markers | Marker Merge |

- **`all` Target Scope**: Expands to the 7 isolated modular targets (`antigravity`, `claude`, `cursor`, `copilot`, `windsurf`, `cline`, `roo`). Root shared files (`codex` -> `AGENTS.md`, `gemini` -> `GEMINI.md`) are excluded from `all` so tools that read both `.agents/rules/` (or `.cursor/rules/`) and root `AGENTS.md` do not double-load Drawlib instructions.
- **Marker Merge Idempotency**:
  1. File does not exist -> creates file with marker-wrapped Drawlib block.
  2. File exists without Drawlib markers -> appends marker-wrapped Drawlib block to the end of the file, preserving all existing user content without requiring `--force`.
  3. File exists and already contains Drawlib markers -> raises `FileExistsError` unless `force=True`, in which case replaces *only* the marker-delimited section in-place.

---

## 4. Source Rule Size Optimization (`< 10,000` chars)

- `src/drawlib/_rules/agent_instruction.md` is condensed from ~15,000 characters down to ~9,000–9,500 characters while preserving 100% of core principles, project-first scaffolding commands, component routing table, code-fence typography math (`720pt`, `text_size >= 10.0`), 3-stage multimodal review loop, parallel subagent protocol, and the `drawlib rules show` topic catalog.
- Ensures full compliance with Windsurf's 12,000-character per-file cap (including frontmatter) and reduces token overhead across all AI coding agents.
- `.agents/rules/drawlib.md` in this repository is synchronized directly via `drawlib init agent antigravity --mode always --force`.

---

## 5. Architecture & Public Python API (`drawlib.tools`)

1. **`src/drawlib/_templates/_agent.py`**:
   - `AGENT_TARGETS` / `ALL_MODULAR_AGENTS` metadata definitions.
   - `list_agent_targets() -> list[dict[str, str]]`
   - `detect_agent_targets(destination: str | Path = ".") -> list[str]`
   - `get_agent_instruction(agent: str, mode: Literal["auto", "always"] = "auto", global_scope: bool = False) -> str`
   - `init_agent_instruction(agent: str | Sequence[str], destination: str | Path = ".", mode: Literal["auto", "always"] = "auto", global_scope: bool = False, output_path: str | Path | None = None, force: bool = False) -> list[Path]`
2. **Re-exports**:
   - `src/drawlib/_templates/__init__.py`
   - `src/drawlib/tools.py` (`_LAZY_ATTRS`, `TYPE_CHECKING`, `__all__`)
3. **CLI Wiring (`drawlib init project` & `drawlib init agent`)**:
   - `src/drawlib/_cli/commands/init.py`: Symmetrical two-subcommand design under `drawlib init`:
     - `drawlib init project <doc|site|slide|images|list>` (`project_app` Typer sub-application; legacy top-level `drawlib init <doc|site|slide|images|list>` removed).
     - `drawlib init agent <target...>` (`cmd_init_agent` and hidden plural alias `cmd_init_agents_alias`).
4. **Tests & Dogfooding Docs**:
   - `tests/drawlib/cli/test_cli_init_agent.py`: Unit & CLI tests covering all 9 agents, aliases, `auto` vs `always` frontmatter, `.agents/` vs `.agent/` smart selection, marker-block append & `--force` in-place replacement, `--detect`, `--global` (with `HOME` monkeypatched), `-o`, `all`, error handling (`.clinerules` file conflict, unsupported `--global` on Cursor/Copilot, duplicate overwrite guard), and character-count assertion (`< 10_600` chars).
   - `tests/drawlib/cli/test_cli_init.py`: Updated all project scaffolding tests to `drawlib init project <type>` and added explicit verification that legacy root `drawlib init <doc|site|slide|images|list>` commands are rejected.
   - Rules & Documentation updates: `src/drawlib/_rules/*.md`, `.agents/rules/drawlib.md`, `README.md`, `docs/README_PYPI.md`, and `docs/*_src/`.
