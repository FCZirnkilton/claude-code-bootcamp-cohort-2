---
paths:
  - "tests/**/*.py"
---

# Test conventions

- Use `unittest` from the standard library. Do not use pytest, fixtures from plugins, or third-party mocks.
- Run with `python3 -m unittest discover -s tests -v`. Quote the raw output (including the final `Ran N tests` and `OK`/`FAILED` lines) as evidence.
- Isolate state: shipctl tests set `SHIPCTL_DB` to a file in a `tempfile.TemporaryDirectory()`; Notes API tests use `NoteRepository(":memory:")` or `create_server(host="127.0.0.1", port=0, db_path=":memory:")`.
- Never read or write the real `tasks.json`, `notes.db`, or anything outside the temp directory.
- One behavior per test method; name it after the behavior (`test_title_only_patch_keeps_body`), not the implementation.
- A bug fix starts with a regression test that fails on the unfixed code. Record the bug ID in the module or class docstring (for example `BUG-101`).
- Cover the edge cases: empty input, missing fields, unknown IDs, invalid dates, and boundary values.
- Do not weaken, skip, or delete an existing test to make a change pass. If you think a test is wrong, stop and explain why.
