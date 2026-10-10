---
paths:
  - "notes_api/**/*.py"
---

# Notes API conventions

- Keep the layers: `server.py` handles HTTP routing and JSON translation only. `service.py` holds validation and business rules. `repository.py` holds SQL only. Do not put SQL in the service or validation in the server.
- Only use parameterized `sqlite3` queries with `?` placeholders. Never build SQL with f-strings, `%`, or `.format()`.
- Validate every client field in `service.py` (type, length, required or optional). Raise `ValidationError` for HTTP 400 and `NotFound` for HTTP 404.
- PATCH is a partial update. A field missing from the request body keeps its stored value. An empty string is an explicit value.
- Send client errors as JSON `{"error": "<human-readable message>"}`. Never put tracebacks, `repr(exc)`, SQL, or file paths in a response.
- Every response has a correct `Content-Type` and `Content-Length`.
- Do not add authentication, CORS, or new endpoints unless the brief asks for them. If one seems needed, propose it and stop.
- Python 3 standard library only.
- Every endpoint change needs an end-to-end test in `tests/` that drives a real server on an ephemeral port.
