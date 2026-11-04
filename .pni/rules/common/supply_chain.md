# Supply Chain & Repository Governance Standards (Common — OpenSSF Scorecard)

## Core Principles
1. **Reproducible Locked Dependencies**: Every repository declaring third-party dependencies (`ProjectFacts.dependencies`) must commit a deterministic lockfile or wrapper (`uv.lock`, `poetry.lock`, `gradle.lockfile`, `package-lock.json`, `go.sum`) and avoid unpinned dependency specs (`ProjectFacts.unpinned_dependencies`).
2. **Least-Privilege CI Tokens (`Token-Permissions`)**: Every GitHub Actions workflow (`.github/workflows/*.yml`) must declare an explicit `permissions:` block (`contents: read` by default) at workflow or job level, and avoid unsafe `pull_request_target` execution of untrusted PR code (`ProjectFacts.ci_supply_chain_issues`).
3. **Immutable CI Actions (`Pinned-Dependencies`)**: Never reference mutable branches (`@main`, `@master`, `@HEAD`) in `uses:` steps; pin third-party actions to full commit SHAs or immutable release tags.
4. **Automated Vulnerability & Dependency Updates**: Configure `.github/dependabot.yml` or `renovate.json` (`ProjectFacts.has_dependency_automation`) and publish a vulnerability reporting policy in `SECURITY.md` (`ProjectFacts.has_security_policy`) alongside an explicit `LICENSE` (`ProjectFacts.has_license`).
5. **Container Build Hygiene**: When a `Dockerfile` is present (`ProjectFacts.has_dockerfile`), pin base image versions (never `:latest`), run the final stage as a non-root `USER`, and maintain a `.dockerignore` file (`ProjectFacts.container_hygiene_issues`).
