# Specification Change Management

## 1. Status Definitions
- `Adopted`: implemented and enforced in repository practice
- `Draft`: defined but not fully implemented
- `Deprecated`: no longer recommended, kept for historical reference

## 2. When Specifications Must Be Updated
- A new task type or method type is introduced
- Result fields or output structure are modified
- Experiment fairness strategy changes (budget, split, repeat count)
- A new execution entry point is introduced or repository layout is refactored

## 3. Change Submission Workflow
1. Update status and notes in the corresponding `spec/*/index.md`
2. Update all impacted specification files
3. Include "impact scope + rollback cost + risk" in the commit message

## 4. Versioning Recommendations
- For major spec updates, maintain a "Last Updated" date at the end of the file
- For breaking changes, add migration notes
