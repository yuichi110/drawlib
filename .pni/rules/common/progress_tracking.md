# Project Progress & Delivery Tracking Standards (Common)

This standard governs project milestone/schedule tracking, declared-vs-verified progress scrutiny, historical trajectory evaluation, and Git-tracked JSONL history ledgers under `category: progress` workflows.

---

## Core Rules (`PRG-01` – `PRG-05`)

### `PRG-01` — Pre-Flight Schedule & Git Policy Alignment
- Every `category: progress` workflow requires a validated baseline manifest at `.pni/progress/<target>.yaml` before `pni workflows start` can execute (`pni progress init <target>` -> edit -> `pni progress validate <target>`).
- Before running the first measurement on a new project, align `.pni/progress/<target>.yaml` with the team's real milestones, task dependencies (`depends_on` DAG), expected deliverable paths (`expected_paths`), branching methodology (`git_policy.methodology`), and merge strategy (`git_policy.merge_strategy`).

### `PRG-02` — Baseline Plan Immutability During Measurement Runs
- `.pni/progress/<target>.yaml` represents the **contracted baseline** for a progress run (`plan_sha256`).
- During a measurement workflow (`pni workflows start` -> `get-action` -> `push-action`), AI agents **must treat `.pni/progress/<target>.yaml` as strictly Read-Only**. Never overwrite `planned_end`, `status`, or `declared_progress` inside `.pni/progress/*.yaml` to mask schedule slippage; PNI verifies `plan_sha256` on `emit_progress` and rejects tampered baselines.

### `PRG-03` — Declared vs. Verified Progress Scrutiny
- Never accept `declared_progress` or `status: "done"` at face value when deterministic `task_evidence` contradicts it:
  - If `missing_paths` is non-empty, cap `verified_progress` proportionally to missing deliverables and flag the gap in `evidence_summary`.
  - If matched branches are unmerged (`branch_merged == false`) or fail `git merge-tree` conflict simulation (`branch_has_conflict == true`), deduct integration work and do not classify the task as `completed`.
  - If `stub_todo_count > 0` (`TODO` / `FIXME` / `NotImplementedError`) or `has_tests == false` on core feature paths, reflect the remaining stabilization effort in `verified_progress` and `risk_note`.

### `PRG-04` — Velocity, Rework Churn & Test-to-Code Trajectory Balance
- Evaluate historical `trajectory` trends (`source_loc`, `test_loc`, `static_test_cases`, `commits_count`) and `churn_hotspots` (`rework_ratio`) rather than single-point snapshots:
  - Rapid `source_loc` expansion accompanied by stagnant `test_loc` / `static_test_cases` signals accumulating verification debt (`test_gap` action item).
  - High `rework_ratio` (> `0.50` across 3+ commits on the same module) signals unstable requirements or architectural friction (`schedule_recovery` / `branch_hygiene`).

### `PRG-05` — Lightweight Audit Linkage (`based_on` & `.pni/history/`)
- Deep code-quality, architecture, security, and container diagnostics belong to `category: audit` workflows—do **not** duplicate 7-axis deep code audits inside `category: progress`.
- When `based_on: <audit_workflow_id>` is configured, summarize the Git-tracked `.pni/history/audit/<audit_workflow_id>.jsonl` score trajectory and any blocking `critical`/`high` findings in `audit_status_note` (2–3 concise sentences) without requiring `.gitignore`'d `.pni/cache/workflow_state.db`.
