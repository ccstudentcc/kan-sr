# Git Commit Message Convention

## 1. Format
Commit messages follow this structure:

```text
<type>(<scope>): <subject>

<body>

<footer>
```

`Header` is required. `Body` and `Footer` are optional.

## 2. Header Rules

### 2.1 Type (Required)
Allowed types:

- `feat`: introduce a new feature
- `fix`: fully fix a bug
- `to`: partial bug-fix step (used before final `fix`)
- `docs`: documentation-only changes
- `style`: formatting changes with no behavior change
- `refactor`: code restructuring with no feature/bug behavior change
- `perf`: performance and experience improvements
- `test`: add or update tests
- `chore`: tooling/build/process maintenance
- `revert`: revert previous commit(s)
- `merge`: branch merge commits
- `sync`: sync bug-fix changes from mainline or another branch

### 2.2 Scope (Optional)
Scope describes the impacted area, for example:

- `controller`
- `data-access`
- `experiment`
- `scripts`
- `spec`

If multiple scopes are impacted and one scope is not enough, use `*`.

### 2.3 Subject (Required)
Subject rules:

- Start with a verb in present tense (`add`, `fix`, `update`, `remove`)
- Use lowercase first letter
- Keep within 50 characters when possible
- Do not end with a period

Examples:

- `feat(controller): add user login flow`
- `fix(data-access): correct query filter logic`
- `to(experiment): align summary schema checks`

## 3. Body Rules (Optional)
Body should explain:

- Why the change is needed (motivation)
- What changed compared with previous behavior
- Important tradeoffs or constraints

Use present tense and keep statements specific.

## 4. Footer Rules (Optional)
Footer is used for:

### 4.1 Breaking Changes
Use:

```text
BREAKING CHANGE: <what changed, why, and how to migrate>
```

### 4.2 Issue Closing
Use:

```text
Closes #234
```

Or multiple issues:

```text
Closes #123, #245, #992
```

## 5. Repository-Specific Notes
- Commit messages must be in English.
- Include impact scope and risk when changes affect protocol, schema, or workflow checks.
- Prefer small incremental commits over large mixed commits.
