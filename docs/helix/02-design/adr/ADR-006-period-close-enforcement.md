---
ddx:
  id: ADR-006
  authoring:
    home: repo
  links:
    - ADR-002
    - ADR-005
---

# ADR-006: Enforce period close in the service and in the database

## Problem

FR-27 says no role may create, edit, delete, approve, reject, or reopen an entry whose local date is on or before the close-through date. A check only in the API could be bypassed by a bug or a future code path.

## Decision

The close-through date lives in a single `settings` row. Every write use case reads it inside its transaction (with an update lock) and refuses closed dates. As defense in depth, a trigger on `time_entries` rejects any insert, update, or delete touching a row whose `local_date` (old or new) is on or before the close-through date. Closing and reopening only change `settings.closed_through` and write an audit row in the same transaction. Only Accountants and Admins may change it.

## Why We Chose This

### Over service-level checks only
One missed code path would silently break accounting guarantees.

### Over per-entry lock flags
Closing a period would touch every entry in it, and new entries would need special handling.

## Consequences

**Good**: The guarantee holds even for buggy or future code; closing is a one-row change.

**Trade-offs**: A trigger is logic outside TypeScript (covered by migration tests); bulk data fixes in closed periods require reopening first.

**Drift signals to watch**: Disabling the trigger in migrations; writes that skip the settings read.

## Concern Impact

- **No concern impact**.
