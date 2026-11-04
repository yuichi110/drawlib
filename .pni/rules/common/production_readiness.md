# Production Readiness Review Standards (Common — Google SRE PRR)

Apply this standard primarily to deployed services, APIs, and workers (`"web_api"` or `"worker"` in `runtime_types`), and apply timeout/error-handling rules to any codebase performing external I/O.

## Core Principles
1. **Mandatory External I/O Timeouts**: Every outbound HTTP, RPC, database, or subprocess call must specify explicit connection and read timeouts so a stalled dependency cannot exhaust worker pools (`AstFacts.missing_io_timeouts` = 0).
2. **Bounded Retries & Cascading-Failure Prevention**: Pair transient-error retries with exponential backoff + jitter and idempotency guarantees; avoid unbounded retry loops.
3. **Actionable Error Propagation**: Never swallow exceptions silently (`try-except-pass` or empty `catch`, `AstFacts.bug_risk_idioms`); preserve causal context (`raise ... from err` or wrapped cause) and avoid leaking internal stack traces to external clients.
4. **Health, Readiness & Observability**: Expose lightweight liveness/readiness probes for services, correlate request/job IDs in structured logs, and instrument critical latency/error paths.
