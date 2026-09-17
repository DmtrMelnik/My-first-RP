# Broken report

This file is intentionally malformed.

## Metadata
| Field | Value
User ID is missing a proper table

## Q1 — Route Changes & Deviations

| # | Time (UTC) | Type | Reason | ETA impact | Context |
| 1 | not a valid table because the separator is missing | x | y | z | w |

## Q3 — Traffic

**Actionable congestion signals (over-pred or missed, duration ≥ 30s): 1**

| # | Signal | Worst moment (UTC) | Duration | Severity | congestion_numeric | Expected (km/h) | Actual (km/h) | Location (lon,lat) |
|---|--------|-------------------|----------|----------|--------------------|----------------|--------------|-------------------|
| 1 | ⚠️ FN-risk | 2026-01-01 00:00:00 UTC | 30s | — | 0 | 30 | 0

| leftover | garbage |
this row is not a table

## Q4 — GPS / Map-matched Divergence ⚠️ Experimental

**Navigator fallback to raw GPS: not-a-number**
**Map-matcher teleports: ⚠️ 2**

| # | Time (UTC) | Worst dist | Duration |
|---|-----------|-----------|---------|
| 1 | 2026-01-01 00:01:00 UTC | potato | 1s |
| extra | columns | 12m | 2s | oops |

## Q10 — Route Incidents

| # | First seen (UTC) | Source | Type | Impact | Road | Length | Location | Driver passed? | Deviation? |
|---|-----------------|--------|------|--------|------|--------|----------|----------------|-----------|
| 1 | 2026-01-01 00:02:00 UTC | getRoute | construction | major | Road | 10 m | not-a-coord | ✅ Yes | — |

## Not a Q section

| a | b |
|---|---|
| 1 | 2 |
