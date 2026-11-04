# Code Quality Standards (Python)

## Core Principles
1. **PEP 8 Compliance**: Follow PEP 8 style guide. Enforce formatting and linting with Ruff.
2. **Docstrings**: Provide Google-style docstrings for all public modules, functions, and classes.
3. **Naming Conventions**: Use `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants.
4. **Line Length**: Keep line lengths within 120 characters.
5. **Shared Mutable State vs. Local Legacy Idioms**: Strictly distinguish active cross-request/thread race conditions (mutable module-level globals, singleton attributes, or mutable default arguments mutated at runtime) from function-local deprecated/legacy stdlib calls or unused helpers, reporting the latter as modernization debt rather than concurrent state corruption.
