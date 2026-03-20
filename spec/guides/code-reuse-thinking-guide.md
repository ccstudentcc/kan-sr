# Code Reuse Thinking Guide

## 1. Reuse Priority
- Highest priority for reuse: configuration structure, evaluation fields, result writing logic
- Secondary reuse: plotting templates, data generation utilities
- Last reuse: experiment-specific temporary analysis

## 2. When to Extract Shared Code
- When the same logic appears for the third time, it must be extracted into a script or module.
- Logic shared across tasks should not remain in a single notebook.

## 3. Preventing "Forked Implementations"
- Keep only one authoritative config file per task (`configs/tasks/<task>.yaml`)
- Keep only one authoritative definition per result field (`EXPERIMENT_PROTOCOL.md` + `spec/experiment/result-governance.md`)

## 4. Practical Checklist
- Are there copy-pasted code blocks where only constants changed?
- Is the same metric named differently across files?
- Does one change require edits in more than three places? If yes, consider abstracting a shared layer.
