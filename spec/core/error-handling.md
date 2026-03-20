# Error Handling Guidelines

## 1. Core Principles
- Fail Fast: missing config, unsupported method, or wrong field types must raise exceptions immediately.
- Fail Visible: runtime failures must be written to result artifacts; silent swallowing is not allowed.

## 2. Constraints
- `except: pass` is forbidden.
- `except Exception` must log context: task name, method name, seed, and stage.
- Error messages should directly locate the relevant config field or function entry point.

## 3. Recommended Practices
- Perform structural validation during config loading (see `validate_config`).
- During batch runs, convert exceptions into structured output fields: `status` + `error_message`.
