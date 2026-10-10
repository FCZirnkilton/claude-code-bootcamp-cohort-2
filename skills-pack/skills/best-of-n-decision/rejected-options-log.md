# Rejected Options Log

Record one entry for **every** rejected option. All five fields are required.
An entry with a missing field is incomplete.

## Entry template

```markdown
### Rejected: Option <letter>: <name>

- **Summary of the approach:** <2-3 sentences describing the design>
- **Main advantages:** <bullets: what it does better than the selected option>
- **Main disadvantages:** <bullets: concrete costs or risks>
- **Primary reason for rejection:** <one sentence; the deciding factor>
- **Conditions under which the approach may become appropriate later:** <measurable triggers, e.g. "more than 10k notes", "multiple concurrent writers", "team adopts an ORM">
```

## Field guidance

| Field | Good | Weak |
|-------|------|------|
| Summary of the approach | "Notes stored in SQLite through `sqlite3`; repository translates rows to `Note` objects." | "Use a database." |
| Main advantages | "Transactions and indexed search for free." | "It's better." |
| Main disadvantages | "Schema migrations add a step to every model change." | "Complex." |
| Primary reason for rejection | "Adds migration overhead with no benefit at workshop data size." | "Didn't like it." |
| Conditions to reconsider | "Note count above ~10k or two processes writing at once." | "Maybe later." |

## Example (Shipyard Notes API)

```markdown
### Rejected: Option B: SQLite repository

- **Summary of the approach:** Persist notes in a local SQLite file through the
  standard-library `sqlite3` module. The repository layer owns SQL; the service
  and HTTP layers are unchanged.
- **Main advantages:** ACID writes; indexed search for tags; still stdlib-only.
- **Main disadvantages:** Schema migration code; tests need a temp database file
  or `:memory:` setup; harder to inspect data by hand during the workshop.
- **Primary reason for rejection:** Its strengths (concurrency, large data) do not
  matter at workshop scale, and it costs more setup than the JSON repository.
- **Conditions under which the approach may become appropriate later:** more than
  ~10k notes, more than one writer process, or a requirement for full-text search.
```
