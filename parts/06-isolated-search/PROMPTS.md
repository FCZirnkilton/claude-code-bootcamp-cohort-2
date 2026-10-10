# Part 06 prompts

Copy each block into Claude Code in order. Read the output before sending the next one.

## 1. Build inside the worktree (`claude --worktree search-tags`)

```text
Read briefs/search-and-tags.md. Implement search and tags exactly as specified, keeping the layering (SQL only in repository.py, rules only in service.py). Add tests in tests/test_search_tags.py, including literal % and _ in search. Run the full suite and show the raw output. Then show git diff --stat against main. Do not commit and do not touch files outside notes_api/ and tests/.
```
