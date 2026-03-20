# Logging Guidelines

## 1. Logging Goal
- Make the full experiment flow traceable, from input configuration to output results.

## 2. Output Levels
- `INFO`: stage start/end, plan count, output path
- `WARN`: compatibility fallback, non-blocking exceptions
- `ERROR`: task failure, invalid config, missing critical dependencies

## 3. Format Recommendation
- Unified structure: `[LEVEL] [task=<name>] [method=<name>] [seed=<n>] message`
- Scripts must output at least:
  - final run count
  - artifact path
  - failure count

## 4. Notebook and Script Consistency
- Key experimental conclusions in notebooks should retain corresponding script run records or parameter snapshots, to avoid "plots without process".
