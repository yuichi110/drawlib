# Command Line Interface Guidelines (Common — `clig.dev`)

Apply this standard to command-line tools and developer CLIs (`"cli"` in `runtime_types`).

## Core Principles
1. **Discoverable Help & Version**: Support `-h` / `--help` and `version` / `--version` cleanly with concise command summaries, concrete examples, and clear argument descriptions.
2. **Stdout vs. Stderr Separation**: Write primary command results and machine-consumable payloads (JSON/YAML/Markdown) to `stdout`, and route error diagnostics, warnings, and progress messages to `stderr` so Unix pipelines (`|`, `>`) remain clean.
3. **Meaningful Exit Codes**: Return `0` on success and non-zero exit codes on validation, runtime, or usage errors (`typer.Exit(code=1)`, `sys.exit(1)` at CLI boundary only).
4. **Automation & Non-Interactive Friendliness**: Never block indefinitely on interactive prompts without a flag bypass (`--force`, `--yes`, `--file`, stdin); provide structured output modes or deterministic plain output for scripts and AI agents.
5. **Actionable Error Messages**: State what went wrong and suggest the exact recovery command (e.g., `"Run 'pni init' first..."`) rather than dumping raw unhandled tracebacks for expected user errors.
