# Security Standards (Common — OWASP ASVS Baseline)

## Core Principles
1. **Zero Hardcoded or Committed Secrets**: Never hardcode passwords, API keys, or tokens in source literals (`AstFacts.hardcoded_secrets`) or commit `.env`, `*.pem`, `*.key`, or credential JSON files to version control (`ProjectFacts.committed_secret_files`).
2. **Safe Process, Deserialization & Query Execution**: Eliminate dynamic code evaluation (`eval`/`exec`), shell-interpolated subprocess calls (`shell=True`), unsafe deserializers (`pickle`, unguarded `yaml.load`), and unparameterized SQL/command string concatenation (`AstFacts.bug_risk_idioms`).
3. **Boundary Input Validation**: Validate and parse all untrusted external inputs (CLI arguments, HTTP payloads, file/YAML/JSON inputs, environment variables) through strict schema types at system boundaries.
4. **Principle of Least Privilege**: Operate processes, CI workflows, containers, and storage clients with minimal required permissions.
