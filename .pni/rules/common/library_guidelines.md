# Library & SDK Packaging Guidelines (Common — SemVer & API Purity)

Apply this standard to reusable packages, SDKs, and internal shared libraries (`"library"` in `runtime_types`).

## Core Principles
1. **Explicit Public API Surface**: Define clear public vs. internal module boundaries (`__all__`, `_`-prefixed internal packages in Python; `public` vs. package-private/module exports in Java) and ship complete type metadata (`py.typed` marker, `ProjectFacts.has_type_marker`).
2. **Zero Import-Time Side Effects**: Importing a library module must never perform network I/O, mutate global state, configure root loggers, or read required environment variables at module top level.
3. **Never Terminate the Host Process**: Library code outside explicit CLI entrypoints must raise typed domain exceptions rather than calling `sys.exit()`, `os._exit()`, or `System.exit()`, or writing unstructured `print()` output (`AstFacts.unstructured_logging`).
4. **SemVer-Friendly Dependency Bounds**: Declare flexible lower bounds (`>=`) on runtime `dependencies` and avoid strict `==` pins (`ProjectFacts.tooling_modernization_issues`) that cause version-resolver deadlocks for downstream consumers; reserve exact pins for application lockfiles.
