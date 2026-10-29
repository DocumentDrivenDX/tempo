---
ddx:
  id: ADR-005
  authoring:
    home: repo
  links:
    - prd
---

# ADR-005: Store every entry with its time zone and split at local midnight

## Problem

The PRD requires each entry to record its time zone so Tempo can show local working hours (FR-23), split entries that cross local midnight (FR-24), and keep day and month totals exact (FR-19, FR-26, FR-27).

## Decision

Each time entry stores: `started_at_utc` and `ended_at_utc` (nullable for manual entries with no start time), `duration_minutes` (integer, at least 1), `tz_id` (IANA name in force when logged), `utc_offset_minutes` at the start, and `local_date` (the entry's date in `tz_id`). Start and end are truncated to whole minutes before use, so durations are exact integers. An entry whose local span crosses midnight in `tz_id` is split into one entry per local day at the exact local midnight, using IANA rules (so a daylight-saving day has 23 or 25 hours); the segments' durations sum to the original. `local_date` is fixed at write time and never recomputed when the profile zone changes. Day, week, and month grouping uses `local_date` by default; grouping by a chosen reporting zone converts `started_at_utc` and falls back to `local_date` for entries with no start time.

## Why We Chose This

### Over storing UTC only
Day and month totals would shift with the viewer's zone, and month-end entries would land in the wrong month.

### Over storing local time only
The instant is lost, so cross-zone time-of-day and reporting-zone views are impossible.

## Consequences

**Good**: Exact, stable month totals; correct local working-hour analysis; period close can use `local_date`.

**Trade-offs**: Redundant columns to keep consistent (enforced by a domain function and database check constraints); manual entries without a start time cannot appear in time-of-day views or reporting-zone conversion.

**Drift signals to watch**: Recomputing `local_date` from UTC at query time; floating-point durations; splits done in the UI.

## Concern Impact

- **No concern impact**.
