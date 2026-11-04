# Containerized Runtime Verification Standards (Common — Build, Offline Tests, Coverage & Boot)

Apply this standard whenever `RuntimeFacts` (`run_check` / `container_runtime_audit`) is executed in a workflow. If `RuntimeFacts.status == "skipped"` because no container daemon (`docker` / `podman`) is available on the host, mark `common/runtime_verification` as `not_applicable` and cite `RuntimeFacts.skip_reason`.

## Core Verification Gates

1. **RV-01 — Deterministic Clean Build & Dependency Resolution**:
   - The target codebase must build cleanly from scratch inside an isolated container (`RuntimeFacts.harness_build.status == "passed"`).
   - If the repository defines its own `Dockerfile` / `Containerfile`, `RuntimeFacts.project_dockerfile_build.status` must also equal `"passed"`; otherwise flag broken build steps, undeclared OS libraries, or unpinned transitive breaks (`HIGH` / `CRITICAL`).
   - If custom native packages were required, note the harness file under `.pni/dockerfiles/.../Dockerfile`.

2. **RV-02 — Hermetic Offline Unit Test Execution (`--network=none`)**:
   - Unit tests must execute deterministically with network access disabled (`RuntimeFacts.test_execution.status == "passed"`, `failed_tests == 0`, `error_tests == 0`).
   - Flag any failing test case (`RuntimeFacts.test_execution.failures`), timeout, or live-network dependency exposed by `--network=none` (`HIGH` / `CRITICAL`).

3. **RV-03 — Measured Line & Branch Test Coverage**:
   - Evaluate measured execution coverage (`RuntimeFacts.coverage.line_coverage_pct` and `branch_coverage_pct`) rather than relying solely on static test-file ratios:
     - **`>= 80%` line coverage** (`>= 70%` branch): Healthy (`PASS`).
     - **`60% – 79.9%` line coverage**: Moderate gap (`WARN`); prioritize `lowest_covered_modules`.
     - **`< 60%` line coverage** (or `measured == false` when tests exist): High regression risk (`FAIL`); cite exact files and `missing_lines_preview` from `RuntimeFacts.coverage.lowest_covered_modules`.

4. **RV-04 — Archetype Startup Smoke & DI Wiring Health**:
   - The software must boot or initialize cleanly for its archetype (`RuntimeFacts.smoke_check.status == "passed"`):
     - `library`: Clean top-level package import without import-time side effects or missing runtime dependencies.
     - `cli`: Entry-point `--help` exits `0` without stack traces.
     - `web_api` / `worker`: ASGI/WSGI lifespan or Spring `ApplicationContext` initializes cleanly without circular DI errors (`import_or_di_error`), unguarded startup connections (`external_service_unreachable`), or crashes.
