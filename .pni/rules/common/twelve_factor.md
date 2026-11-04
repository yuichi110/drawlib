# Twelve-Factor & Cloud-Native App Standards (Common — `web_api` / `worker`)

Apply this standard to network services, APIs, and background workers (`"web_api"` or `"worker"` in `runtime_types`). Do **not** penalize pure libraries or standalone offline CLIs for lacking service ports or daemons.

## Core Principles
1. **Centralized, Typed Configuration (Factor III)**: Read environment configuration once in a dedicated, schema-validated config/settings layer (`pydantic-settings`, `@ConfigurationProperties`) rather than scattering raw `os.environ` / `System.getenv` lookups across domain and service modules (`AstFacts.scattered_env_access`).
2. **Swappable Backing Services (Factor IV)**: Treat databases, queues, caches, and external HTTP APIs as attached resources injected via configuration/interfaces without hardcoded hostnames or credentials.
3. **Stateless, Share-Nothing Processes (Factor VI)**: Never rely on mutable in-memory global state (`AstFacts.global_state_usages`) or local sticky filesystem state across requests/jobs.
4. **Disposability & Graceful Shutdown (Factor IX)**: Start fast, handle `SIGTERM` cleanly, finish or roll back in-flight requests/tasks, and close connection pools deterministically.
5. **Structured Event-Stream Logs (Factor XI)**: Emit structured logs via a standard logging framework (`logging`/`structlog`/`SLF4J`) rather than raw `print()` or `System.out.println()` (`AstFacts.unstructured_logging`).
