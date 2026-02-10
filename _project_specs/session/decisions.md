<!--
LOG DECISIONS WHEN:
- Choosing between architectural approaches
- Selecting libraries or tools
- Making security-related choices
- Deviating from standard patterns

This is append-only. Never delete entries.
-->

# Decision Log

Track key architectural and implementation decisions.

## Format
```
## [YYYY-MM-DD] Decision Title

**Decision**: What was decided
**Context**: Why this decision was needed
**Options Considered**: What alternatives existed
**Choice**: Which option was chosen
**Reasoning**: Why this choice was made
**Trade-offs**: What we gave up
**References**: Related code/docs
```

---

## [2026-02-10] Ruff for linting and formatting

**Decision**: Use Ruff as the linter and formatter
**Context**: No linting or formatting tools were configured
**Options Considered**: Ruff, Black + flake8, pylint
**Choice**: Ruff
**Reasoning**: Fast, covers both linting and formatting, replaces multiple tools
**Trade-offs**: Less mature than pylint for deep analysis
**References**: `ruff.toml`, `.pre-commit-config.yaml`

## [2026-02-10] Conventional commits enforcement

**Decision**: Use conventional-pre-commit hook for commit message validation
**Context**: No commit message standards existed
**Options Considered**: commitlint (Node.js), conventional-pre-commit (Python)
**Choice**: conventional-pre-commit
**Reasoning**: Python-native, no Node.js dependency needed for a Python project
**Trade-offs**: Fewer config options than commitlint
**References**: `.pre-commit-config.yaml`
