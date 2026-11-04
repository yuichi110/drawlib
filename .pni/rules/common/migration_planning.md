# Migration Planning, Pre-Flight Clarification & Phased Execution Guide (Common)

This standard governs how AI agents author, refine, and execute PNI migration planning workflows (`migration_proposal` and `write_migration_report`).

---

## 1. Workflow Category, Prerequisite Audit (`based_on`), and Pre-Execution Clarification Protocol

Every PNI workflow declares a top-level `category`:
- `category: audit` (default): Evaluates As-Is codebase health, architecture, runtime, security, and emits `ScoreResult` + audit report.
- `category: migration`: Synthesizes a To-Be Migration Execution Plan (`MigrationPlanResult` + 7-chapter Drawlib report) and **MUST declare `based_on: <audit_workflow_id>`** at the top level of `.pni/workflows/<migration_id>.yaml`.
  - **Automatic Target & Fact Inheritance**: `targets` (`root`, `source`, `tests`, `docs`) are automatically inherited from `based_on` (do not duplicate `targets` unless intentionally overriding a path). When started, PNI automatically inherits the completed audit run's `ProjectFacts`, `AstFacts`, `RuntimeFacts`, `SecurityFacts`, `ArchitectureRecord`, and `ScoreResult` directly from `.pni/cache/workflow_state.db`.
  - **Mandatory SQLite Audit Prerequisite**: `pni workflows start <migration_id>` fails with an explicit `WorkflowPrerequisiteError` unless `<audit_workflow_id>` has a `completed` run in `.pni/cache/workflow_state.db`. **If `pni workflows show` or `pni workflows start` reports a missing or unfinished prerequisite audit run, execute `pni workflows start <audit_workflow_id>` (or resume the unfinished audit run) and complete the audit workflow FIRST before starting the migration workflow.**

Because `pni workflows start <workflow_id>` freezes step parameters into `.pni/cache/workflow_state.db`, **the workflow YAML in `.pni/workflows/*.yaml` must serve as the deterministic Single Source of Truth (SSOT)**. Never launch a migration workflow on a vague or underspecified prompt.

Before running `pni workflows start <migration_id>`, execute this 4-step pre-flight protocol:

### Step 1: Ensure Prerequisite Audit Is Completed & Cross-Check As-Is Facts
- Run `pni workflows show <migration_id>` (or check `pni workflows status`) to verify `based_on: <audit_workflow_id>` has a `COMPLETED` run in `.pni/cache/workflow_state.db`. If not yet completed, run and complete `<audit_workflow_id>` first so full As-Is diagnostics exist.
- Inspect the completed audit artifacts (`reports/<lang>/<target>_score.json`, `.pni/cache/<audit_wf>/facts.json`) and target manifests/code (`pom.xml`, `composer.json`, `pyproject.toml`, session/cache globals, SQL queries, HTTP clients).

### Step 2: Scrutinize the 6 Ambiguity Dimensions
Check whether any of the following 6 architectural decisions are missing, contradictory, or phrased vaguely (e.g., `"latest"`, `"最新"`, `"いい感じ"`, `"TBD"`, `"未定"`):

1. **Concrete Target Stack & Versions**: Exact language/runtime and framework versions (e.g., `Java 21 LTS + Spring Boot 3.4`, `PHP 8.3 + Laravel 11`, `Python 3.12 + FastAPI`) rather than generic "upgrade to latest".
2. **Stateful Middleware (Database / Cache / Session / Queue)**: When As-Is code holds process-local state (`static HashMap`, singleton mutable fields, `$_SESSION`, cookie `unserialize`) or raw SQL, confirm target backing stores (e.g., `PostgreSQL 16 + Spring Data JPA + Flyway`, `Redis 7` with TTL, or stateless refactoring).
3. **Architecture Philosophy & Boundary Scope**: When architectural modernization (e.g., Clean Architecture, Hexagonal / Port & Adapter, Modular Monolith) is requested, clarify the target ring/package layout (`domain` / `usecase` / `port` / `adapter`) and whether strict framework-free `domain` isolation applies across all modules or only around external I/O boundaries.
4. **External Contract Compatibility (`api_compatibility`)**: Confirm whether public URLs, HTTP methods, JSON request/response field names, and auth headers must remain 100% backward-compatible (`strict`) or whether a versioned contract (`versioned_v2` / `flexible`) is permitted.
5. **Ambiguous Legacy Behavior Policy (`bug_handling_policy`)**: When As-Is diagnosis reveals bug-risk idioms or legacy crypto/comparison quirks (Hyrum's Law, e.g., Java `currency == "USD"` reference equality, MD5 password hashes), confirm whether to preserve behavior during infrastructure phases and isolate them into the Stakeholder Decision Log (`ask_human` [Recommended]) or fix them immediately.
6. **Rollout Strategy & Explicit Non-Goals (`migration_strategy`)**: Confirm single-repo incremental PRs (`phased_pr`), proxy-routed coexistence (`strangler_fig`), or clean-slate replacement (`rewrite`), plus explicit **Non-Goals** (e.g., "OAuth2 IdP migration is out of scope for this phase").

### Step 3: Ask Concise Clarifying Questions to the User
- Whenever high-impact ambiguities remain, **stop before `pni workflows start`** and ask the user concise, structured questions grounded in the real As-Is codebase, always proposing a `(Recommended)` option for each question.
- Only skip interactive questioning if the user has already provided concrete answers or explicitly instructed `"推奨案でお任せ"` / `"proceed with recommended defaults"` (in which case, document those chosen defaults in `confirmed_assumptions`).

### Step 4: Materialize Confirmed Decisions into `.pni/workflows/*.yaml`
- Persist `category: migration`, `based_on: <audit_workflow_id>`, and all confirmed requirements, constraints, and non-goals into `.pni/workflows/<migration_id>.yaml` under `with.brief: |` (or `with.brief_file`) and replace `"auto"` guardrails with explicit pinned values (`migration_strategy`, `api_compatibility`, `bug_handling_policy`, `codemod_tool`).
- Run `pni workflows show <migration_id>` and verify both `✓ Prerequisite Audit Ready` and `✓ Migration Preflight Check` before invoking `pni workflows start <migration_id>`.

---

## 2. Multi-Axis & Target Architecture Design Rules

1. **Dynamic Multi-Axis Coverage (`target_axes`)**:
   - Represent every requested change dimension (`language_runtime`, `framework`, `architecture_pattern`, `database_persistence`, `cache_state`, `auth_security`, `container_cicd`) with grounded As-Is evidence (`affected_files`) and concrete To-Be targets.
2. **Clean Architecture / Port & Adapter Isolation (`target_architecture`)**:
   - **Dependency Inversion**: Inner layers (`domain`, `usecase`) MUST NOT import web frameworks (`org.springframework.web.*`, `Illuminate\Http\*`, `fastapi`), ORM annotations (`jakarta.persistence.*`), cache clients, or HTTP libraries.
   - **Boundary Touchpoint Mapping**: Every `BoundaryTouchpoint` (`in_memory_state`, `persistence_db`, `external_http_rpc`) extracted by `migration_analyze` MUST map to an explicit Port interface and Outbound Adapter in `component_mappings` (including explicit connect/read timeouts for HTTP adapters and TTL/serialization rules for Redis/cache adapters).
3. **Strict External Compatibility Mapping**:
   - When `api_compatibility == "strict"`, keep external HTTP routes and JSON keys intact inside Inbound Web Adapter DTOs, translating at the boundary into clean Domain/UseCase types.

---

## 3. 5-Phase Gated Execution & PR WBS Rules

Structure every migration execution plan across **5 sequential phase gates** (`Phase 0`..`Phase 4`) and decompose work into atomic, reviewable PRs (`pr_wbs`):

- **Phase 0 — Minimal Green Build & Characterization (Golden Master) Tests**:
  - Fix build/toolchain blockers (`manual_blockers`) with minimal code edits and lock existing endpoint/script contracts (`implicit_contracts`) with snapshot/integration tests before structural changes.
- **Phase 1 — Cycle Cuts & Domain / Port Extraction (Behavior-Preserving)**:
  - Follow `refactoring_waves` (`Wave 1` leaves -> `Wave 3` cycle cuts). Break circular dependencies (`cycle_cuts`) and extract Domain entities, UseCases, and Port interfaces wrapped initially by lightweight legacy/in-memory adapters.
- **Phase 2 — Runtime/Framework Upgrade (Codemods) & New Infrastructure Adapters**:
  - Apply deterministic codemods (`mechanical_codemods`: OpenRewrite, Rector, Ruff) Separate mechanical codemod PRs from manual logic edits so diffs stay reviewable. Implement target DB (PostgreSQL/JPA/PDO/SQLAlchemy) and Cache (Redis) Outbound Adapters verified by integration/contract tests.
- **Phase 3 — Typed Inbound DTOs, Security Hardening & Approved Decision Log Fixes**:
  - Replace untyped `Map` / `$_POST` / `dict` payloads with validated Request/Response DTOs, remediate SQLi/XSS/command-injection/loose-auth sinks, and apply stakeholder-approved `decision_log` fixes.
- **Phase 4 — Container / CI Hardening, Cutover & Final Verification**:
  - Externalize remaining secrets (`env_contracts`), enforce non-root multi-stage `Dockerfile` and pinned CI permissions, execute Strangler Fig traffic cutover (if applicable), and re-run PNI audit + security scan as final acceptance gates.
