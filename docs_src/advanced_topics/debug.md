# Debugging & Error Handling

By default, Drawlib suppresses deep internal tracebacks and prints concise, actionable error messages pointing directly to the user's script file and line number:

- The script file and line where invalid parameters or drawing issues occurred.
- A descriptive error message explaining what failed.

For development, troubleshooting, or reporting bugs, you can enable verbose logging and disable error suppression to inspect full Python stack traces.

---

## 1. Enabling Debug Modes via the CLI

The `drawlib` CLI provides multiple flags to control logging verbosity and error display:

```bash
# 1. Verbose debug logging (shows detailed steps, asset loading, font resolution):
drawlib build html docs_src/ -o docs_html/ --verbose

# 2. Developer mode (disables error suppression and prints full Python tracebacks):
drawlib build html docs_src/ -o docs_html/ --developer
```

| Flag | Logging Level | Error Behavior |
| :--- | :--- | :--- |
| *(default)* | `INFO` | Concise user-facing error message with file and line. |
| `--verbose` / `--debug` | `DEBUG` | Detailed logging for cache hits, font downloads, and compiler passes. |
| `--quiet` | `ERROR` | Silent execution, showing only fatal errors. |
| `--developer` | `DEBUG` | Disables `@error_handler` wrappers, displaying complete raw tracebacks. |

---

## 2. Interactive Block Debugging

When a specific drawing block in a document fails during compilation, extract and inspect that single block with coordinate grid lines:

```bash
# Overlay coordinate grid and center axes:
drawlib show docs_src/diagrams/sequence.md 1 --grid --developer
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
