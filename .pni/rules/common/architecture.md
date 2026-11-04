# Architecture Standards (Common)

## Core Principles
1. **Separation of Concerns (SoC)**: Separate presentation, business logic, and data access.
2. **Layer Hierarchy**: Modules must depend downward on lower layers. Never create cyclic dependencies.
3. **Loose Coupling & High Cohesion**: Design modules with minimal dependencies and clear, focused responsibilities.
4. **Single Source of Truth**: Define models and core domain constants in a single canonical location.
