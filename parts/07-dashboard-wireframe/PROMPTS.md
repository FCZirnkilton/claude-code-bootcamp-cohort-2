# Part 07 prompts

Copy each block into Claude Code in order. Read the output before sending the next one.

## 1. Build from the wireframe

```text
Look at wireframes/release-dashboard.png and read briefs/release-dashboard.md. First list the components, states and interactions you extracted from the image and its annotations. Then build the dashboard in dashboard/ and add the read-only GET /api/tasks route and static serving to the existing server, with node --test tests for the pure logic. Run both test suites and show the raw output. Do not commit.
```

## 2. Verify in Chrome (`claude --chrome`)

```text
Start the server with seeded data (python3 seed.py && python3 -m notes_api.server). Open http://localhost:8000/ in Chrome. Exercise the owner filter, status filter, both combined, search, and tag toggle on/off. Read the console. Resize to 390px wide. Record every issue in docs/browser-issue-log.md with evidence, fix them one by one, and re-verify each fix.
```
