# Trace Analysis Report

## Metadata
| Field | Value |
|-------|-------|
| File | `demo-trace__android__1.0.0__user-1___.pbf.gz` |
| User ID | `user-1` |
| Session ID | `session-9` |
| Vehicle | DEMOCAR01 |
| Project | com.mapbox.porsche |
| Platform | android |
| Nav Native | 324.26.0-demo |

## Q1 — Route Changes & Deviations

Route recalculated **3** times (2 distinct routes). Off-route events: 1.
- ⚠️ Instability cluster: 2 changes near 2026-09-09 04:55:49 UTC

> ℹ️ Off-route events in first 3 min excluded (parking lot buffer). Silent reroutes (SDK rerouted while `route_state` stayed `tracking`) counted in summary only.
> Reason values: `Reroute` = SDK auto-rerouted · `NewRoute` = user/destination change · `Alternative` = user picked alternate · `FastestRoute` = background swap

| # | Time (UTC) | Type | Reason | ETA impact | Context |
|---|------------|------|--------|------------|---------|
| 1 | 2026-09-09 04:55:49 UTC | ⚠️ Off-route → no reroute | Reroute | +4m 10s ⚠️ | Q4 GPS divergence 10m |
| 2 | 2026-09-09 04:57:29 UTC | Route change | NewRoute | +12s | — |

**Net ETA impact from all route changes: +4m 22s ⚠️**
_(1 change added time, 0 saved time)_

Route stabilized after: 2026-09-09 04:57:29 UTC

## Q2 — Route Completion

**Route completed: ❌ NO (canceled by driver)**
- Remaining distance at trace end: 1.2 km
- Remaining ETA at trace end: 3m 10s
- ⚠️ Driver stopped 516m from destination — check destination location for data issues (non-routable access, incorrect placement, access restriction)

- Drive start: 2026-09-09 04:55:49 UTC
- Drive end:   2026-09-09 05:32:22 UTC
- Actual drive time (trace recording span): 36m 33s
- Initial ETA (original route): 11s
- ETA delta: +36m 22s ⚠️ too optimistic

## Q3 — Traffic

**Alternatives offered: 2**

**Slowdowns (< 5 km/h for > 30s): 1**

| # | Start (UTC) | Duration |
|---|------------|----------|
| 1 | 2026-09-09 05:01:08 UTC | 52s |

**Actionable congestion signals (over-pred or missed, duration ≥ 30s): 2**
_(annotation (no speed data): congestion detected but no expected speed available (nav native ≤ 3.18). ⚠️ FN-risk: driver < 50% of model free-flow while annotation says clear — possible missed congestion.)_

| # | Signal | Worst moment (UTC) | Duration | Severity | congestion_numeric | Expected (km/h) | Actual (km/h) | Location (lon,lat) |
|---|--------|-------------------|----------|----------|--------------------|----------------|--------------|-------------------|
| 1 | ⚠️ FN-risk (stopped) 🚦 signal? | 2026-09-09 05:00:16 UTC | 1m 54s | — | 0 | 30 | 0 | (9.18984,48.88913;9.18391,48.89026) |
| 2 | annotation ⚠️ over-pred | 2026-09-09 05:06:32 UTC | 1m 29s | moderate | 15 | 37 | 80 | (9.14609,48.88566;9.14396,48.88451) |

## Q4 — GPS / Map-matched Divergence ⚠️ Experimental

**Total divergence episodes (≥ 8.7m IQR threshold, clustered in 30s windows): 2**

**Top 2 worst moments:**

> ℹ️ Large divergences on divided highways may reflect map matching to the opposite carriageway (~30m apart) rather than a gross positioning error.

| # | Time (UTC) | Worst dist | Duration |
|---|-----------|-----------|---------|
| 1 | 2026-09-09 04:57:27 UTC | 14m | 1s |
| 2 | 2026-09-09 05:29:43 UTC | 31m | 12s |

**Navigator fallback to raw GPS: ⚠️ 1**
**Map-matcher teleports: ⚠️ 4**

## Q5 — Search Destination

**Search attempts: 2** | **Selections: 1**

| # | Time (UTC) | Query | Chars | Results | Selected |
|---|-----------|-------|-------|---------|---------|
| 1 | 2026-09-09 05:32:22 UTC | "Ikea" | 4 | 5 | ✅ IKEA Sindelfingen (pos 1) |
| 2 | 2026-09-09 05:32:22 UTC | "parking_lot" | 11 | ⚠️ 0 | — |

**Selected destinations:**

| # | Name | Address | Dist to trip end |
|---|------|---------|----------------|
| 1 | IKEA Sindelfingen | Hanns-Martin-Schleyer-Straße 2 | 25.1km ⚠️ |

## Q_feedback — User Feedback

**Total feedback events: 1**

| # | Time (UTC) | Type | Description | Lat | Lon |
|---|-----------|------|-------------|-----|-----|
| 1 | 2026-09-09 05:10:00 UTC | false_negative_traffic_issue | missed congestion | 48.89000 | 9.18000 |

**By type:** false_negative_traffic_issue: 1

## Q7 — Tunnel Positioning

**Tunnel sections: 2 | Degraded: 1**

| # | Start (UTC) | Duration | Degraded? | Worst divergence | Worst at (UTC) |
|---|------------|----------|-----------|-----------------|----------------|
| 1 | 2026-09-09 04:59:13 UTC | 7s | ✅ Clean | 4m *(minor)* | 2026-09-09 04:59:19 UTC |
| 2 | 2026-09-09 05:17:25 UTC | 2m 20s | ⚠️ Yes | 17m | 2026-09-09 05:19:32 UTC |

## Q10 — Route Incidents

**Route incidents: 2**

| # | First seen (UTC) | Source | Type | Impact | Road | Length | Location | Driver passed? | Deviation? |
|---|-----------------|--------|------|--------|------|--------|----------|----------------|-----------|
| 1 | 2026-09-09 04:55:49 UTC | getRoute | construction | major | A 81/E 41 | 3.3 km | 48.80787,9.04640 → 48.78595,9.01575 [idx] | ✅ Yes | ⚠️ GPS divergence 10m |
| 2 | 2026-09-09 04:56:17 UTC | refreshRoute | construction | — | B 10 | 730 m | 48.83864,9.10129 → 48.83387,9.09042 [idx] | ❌ No | — |

> ⚠️ Non-routable incident traversed — `road_closure` on Heilbronner Straße (routing error signal)

> ℹ️ 1 passable incident not traversed (construction/lane_restriction)

**Route closures: 1**

> ⚠️ Route was planned through a closed road segment. Likely a routing error.

| # | Route set (UTC) | Geometry indices | Location | Driver traversed? | Note |
|---|----------------|-----------------|----------|-------------------|------|
| 1 | 2026-09-09 05:07:09 UTC | 31–40 | 48.81551,9.17792 → 48.81649,9.17722 | ✅ Yes | ⚠️ Closure starts at route origin |

## Q_EV — EV Data

**ChargingStateEvent count: 0**

**CS waypoint SOC comparison (setRoute → route_refresh → actual):**

| # | CS | setRoute pred | Refresh pred (last before arrival) | Actual SOC | CS used? |
|---|---|--------------|-----------------------------------|------------|---------|
| 1 | EnBW Test | 46.03 kWh | N/A | 40.00 kWh ⚠️ (setRoute +6.03 kWh) | ⚡ Used |

- Mean prediction error: **+1.50 kWh** ⚠️ (positive = over-predicted)
- **Arrival prediction error (last EvData): +2.10 kWh** ⚠️

## Q_lane — Lane Guidance & Maneuver Quality

Findings grouped by **RICO bucket**; the **Detector** column names the producing signal.

### `G:lanes:wrong` — Wrong lane guidance

| Step | Time (UTC) | Location | Maneuver | Detector | Detail | Outcome | B3 lane | Route coords (lon,lat) |
|---|---|---|---|---|---|---|---|---|
| 2 | 2026-09-09 14:52:48 UTC | 48.83255, 9.15785 | turn right | A2 | active idx 1 / 1 lanes | ⚠️ Likely impactful | ⚠️ in off-route lane | 9.157976,48.832606; 9.157845,48.832546 |

_1 finding(s) — A2: 1._

<details><summary>C detail — banner-vs-route lane breakdown</summary>

| Lane | Banner dir | Banner active | Route ind | Route active | Route valid |
|---|---|---|---|---|---|
| 0 | right ⚠️ | ● | straight |  | false |

</details>

### `G:lanes:missing` — Missing lane guidance

_No findings._

### `G:active_mnvr:missing` — Missing maneuver

_No findings._

### `G:active_mnvr:unneeded` — Unneeded maneuver

_No findings._

### `G:banner:wrong` — Wrong banner text

_No findings._

## H1 — Missing HD lanes

| # | Time (UTC) | Location (start → end) | Distance | Duration | Road class | Type | Off-road reason | Maneuver? | Outcome |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-09-09 05:00:00 UTC | 48.81000,9.05000 → 48.81100,9.05100 | 120 m | 8s | motorway | ⚠️ genuine | — | ⚠️ turn right | ⚠️ Likely impactful |
| 2 | 2026-09-09 05:05:00 UTC | 48.82000,9.06000 → 48.82100,9.06100 | 2500 m | 2m | link | 🛈 transition (expected) | — | — | 🛈 Context-only |
