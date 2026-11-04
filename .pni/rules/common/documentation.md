# Documentation Standards (Common — Standard Readme & Diátaxis)

## Core Principles
1. **README First (Standard Readme)**: Every project must provide a clear `README` (`ProjectFacts.has_readme`, `ProjectFacts.readme_headings`) covering Purpose/Overview, Installation/Prerequisites, Quickstart/Usage Example, and Development/Testing commands.
2. **Diátaxis Structure Appropriate to Scale**: Organize non-trivial documentation (`ProjectFacts.docs_inventory`) along the four Diátaxis quadrants rather than mixing them into a single wall of text:
   - **Tutorials** (learning-oriented onboarding)
   - **How-To Guides** (task-oriented recipes)
   - **Reference** (accurate CLI/API specifications and docstrings, `AstFacts.docstring_coverage_pct`)
   - **Explanation** (architecture rationale and design trade-offs)
3. **Up-to-Date & Truthful Docs**: Keep documented signatures, flags, and examples synchronized with code (`AstFacts.doc_signature_mismatches` = 0, `AstFacts.empty_docstrings` = 0), and delete dead commented-out code.
