# Git Workflow & Branch Integration Governance Standards (Common)

This standard defines repository branching methodologies, trunk integration discipline, non-destructive conflict prevention, and commit hygiene (`GIT-01` – `GIT-05`). Quantitative thresholds and project-specific methodology choices are configured in `.pni/progress/<target>.yaml` under `git_policy`.

---

## Core Rules (`GIT-01` – `GIT-05`)

### `GIT-01` — Branching Methodology & Naming Discipline
- Follow a single explicit branching model declared in `git_policy.methodology` (`github_flow`, `trunk_based`, `git_flow`, `release_flow`, or `custom`):
  - **`github_flow` / `trunk_based`**: Keep `trunk_branch` (`main`) continuously deployable; branch directly from `main` using short-lived topic branches matching `allowed_branch_patterns` (`feat/*`, `fix/*`, `refactor/*`, `docs/*`, `chore/*`, `hotfix/*`).
  - **`git_flow`**: Coordinate feature integration through `integration_branch` (`develop`) and isolate release stabilization under `release/*` and `hotfix/*`.
- Delete merged topic branches promptly so branch inventories reflect active work in flight.

### `GIT-02` — Merge Strategy Consistency (`squash_only` | `rebase_ff` | `merge_commit`)
- Integrate topic branches into `trunk_branch` strictly according to `git_policy.merge_strategy`:
  - **`squash_only` / `rebase_ff`**: Maintain a linear `first-parent` history on `trunk_branch` (`git log --first-parent --merges` should remain `0`). Squash noisy WIP commits or rebase cleanly prior to merging.
  - **`merge_commit`**: Preserve explicit `--no-ff` merge commits for feature traceability while rebasing topic branches beforehand so each merge commit represents a clean, tested unit.

### `GIT-03` — Foxtrot Merge & Direct Trunk WIP Prevention
- **No Foxtrot Merges (`forbid_foxtrot_merges: true`)**: Never merge `main` into a topic branch and then fast-forward push that merge commit onto `main` (which flips `main` onto the second parent `HEAD^2` and corrupts `--first-parent` release history). Always rebase topic branches onto `main` or merge via Pull Request into `main`.
- **No Trunk WIP Commits (`forbid_wip_commits_on_trunk: true`)**: Never land `WIP`, `fixup!`, `squash!`, or `tmp` commits on `trunk_branch`.

### `GIT-04` — Proactive Conflict & Divergence Guardrails
- Keep unmerged branches within `git_policy.thresholds` (`stale_branch_days`, `max_behind_commits`, `max_ahead_commits`, `max_unmerged_changed_lines`, ideally < 400–800 changed lines).
- Resolve working-tree unmerged index entries, committed conflict markers (`<<<<<<<` / `=======` / `>>>>>>>`), and `git merge-tree` simulated trunk conflicts (`has_conflict == true`) **immediately as `P0` blockers** before adding further feature commits.
- When multiple active branches modify the same file (`overlapping_file_hotspots`), sequence their merges explicitly and rebase the downstream branch right after the first lands.

### `GIT-05` — Atomic Commit Scope & Message Convention
- Each commit should encapsulate one cohesive logical change with clear intent.
- When `commit_convention: "conventional_commits"` is active, format commit headers as `<type>(<scope>): <summary>` (`feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`, `revert`) and maintain `conventional_commit_ratio >= 0.80`.
