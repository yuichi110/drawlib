# Software Maintainability Standards (Common — SIG / ISO 25010)

## Core Principles
1. **Unit Size (`<= 50` LOC)**: Keep functions, methods, and constructors concise and focused on a single responsibility (`AstFacts.complex_functions`).
2. **Unit Complexity (`Cognitive <= 15`, `McCabe <= 7`)**: Minimize deeply nested conditionals, loops, and exception handlers; prefer early guard clauses and small helper functions (`AstFacts.complex_functions`).
3. **Unit Interfacing (`<= 6` Parameters)**: Avoid long parameter lists (`AstFacts.excessive_parameters`); group cohesive arguments into typed DTOs, value objects, or configuration dataclasses/records.
4. **Module Coupling & Acyclic Boundaries**: Keep `AstFacts.circular_dependencies` and `AstFacts.boundary_violations` at zero, and avoid mutable global or non-final static state (`AstFacts.global_state_usages`).
