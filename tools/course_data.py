"""Single source of truth for the 14 workshop parts: timing, goals, prompts, evidence, discussion.

Used by tools/gen_parts.py (part READMEs and PROMPTS.md) and deck/build_deck.py (slides and notes).
"""

START = "09:00"  # brief table; shift every time if the cohort starts at 10:00 ET

BREAKS = {
    3: ("Break", 10),
    6: ("Break", 10),
    7: ("Lunch", 40),
    11: ("Break", 10),
}

PARTS = [
    {
        "n": 1, "slug": "01-workspace", "minutes": 20, "project": "Project 1: AI-Ready Engineering Workspace",
        "title": "Welcome, setup, AI-first mindset and safe delegation",
        "goals": [
            "Map what Claude Code can do across CLI, IDE, desktop, web and mobile",
            "Run the lifecycle: plan → implement → verify → review → commit",
            "Choose model, context and effort for a task",
            "Pick a permission mode and accept workspace trust deliberately",
            "Separate reversible from irreversible actions; create a recovery point first",
        ],
        "outputs": ["Working Claude Code environment", "Trusted starter repository",
                    "Written permission and safety boundary (SAFETY.md + .claude/settings.json)",
                    "Baseline Git commit and recovery point"],
        "prompts": [
            ("Safety boundary (Manual mode)",
             "Read README.md. Draft SAFETY.md for this repository: the permission mode we use and when, "
             "actions allowed without asking, actions that must ask first, blocked actions, which actions are "
             "reversible versus irreversible, and how we recover (baseline commit). Then show me a matching "
             ".claude/settings.json permissions block (allow / ask / deny) in your reply, but do not create that "
             "file: I will review it and save it myself. Do not commit."),
        ],
        "evidence": ["`claude --version` and `/status`", "`git log --oneline -1` → baseline commit",
                     "SAFETY.md reviewed by a human", "`/permissions` shows the saved rules"],
        "discussion": [
            "Which of your daily tasks are reversible, and which are not?",
            "Rewrite \"Update every dependency, fix whatever breaks, and deploy\" as a safe delegation.",
            "When would you choose plan mode over auto mode?",
        ],
        "lab": "Stage part 01, start Claude Code, accept trust only after reading the folder, choose Manual mode, draft SAFETY.md with the prompt, save the settings yourself, commit the baseline.",
        "video": "Claude drafts the safety boundary from the README; the human saves the settings and commits the baseline.",
    },
    {
        "n": 2, "slug": "02-task-manager", "minutes": 25, "project": "Project 2: CLI Release Task Manager",
        "title": "Prompting Claude Code like a tech lead",
        "goals": [
            "Replace small prompts with a complete engineering brief",
            "State outcome, context, constraints, protected areas and acceptance criteria",
            "Require proof instead of accepting completion claims",
            "Ask for a plan first; review and challenge it; intervene only at decision points",
        ],
        "outputs": ["Working CLI application (`shipctl.py`)", "Structured engineering brief", "Test suite",
                    "Acceptance evidence table", "README with usage examples"],
        "prompts": [
            ("Plan first (plan mode)",
             "Read briefs/cli-release-task-manager.md and SAFETY.md. Propose an implementation plan for shipctl: "
             "files, functions, storage format, how each acceptance criterion will be tested, and the risks. "
             "Do not write code yet."),
            ("Implement after approval",
             "Plan approved. Implement shipctl.py, tests/test_shipctl.py and the README section exactly as planned. "
             "Run python3 -m unittest discover -s tests -v and show the raw output. Then give me a table mapping "
             "every acceptance criterion (AC1-AC8) to the test that proves it, and a short terminal session with "
             "real CLI output for AC1, AC4 and AC5 using SHIPCTL_DB=./demo-tasks.json. Do not commit."),
        ],
        "evidence": ["The approved plan", "Raw `unittest -v` output", "AC → test table",
                     "Real CLI session for AC1, AC4, AC5"],
        "discussion": [
            "Which acceptance criterion was the hardest to prove, and why?",
            "What would you have challenged in the plan?",
            "What is the difference between \"tests pass\" and \"here is the command and its output\"?",
        ],
        "lab": "Run the two prompts. Reject the first plan once with a concrete objection (for example: atomic writes). Check the evidence table against the brief yourself.",
        "video": "Plan mode proposal, approval, implementation, 15 passing tests and the AC evidence table.",
    },
    {
        "n": 3, "slug": "03-project-brain", "minutes": 25, "project": "Project 3: Project Brain",
        "title": "CLAUDE.md, scoped rules and auto memory",
        "goals": [
            "Decide what belongs in CLAUDE.md, and what does not",
            "Record build/test commands, conventions, security rules and do-not-touch areas concisely",
            "Use .claude/rules with `paths:` for directory- or language-specific instructions",
            "Move occasional reference material into Skills",
            "Review, correct and remove stale auto memory",
        ],
        "outputs": ["Reusable CLAUDE.md (under 60 lines)", "Path-scoped rules (`tests/**`, `shipctl.py`)",
                    "Documented conventions", "Reviewed auto-memory entry",
                    "Evidence that Claude followed the context (`shipctl stats`)"],
        "prompts": [
            ("Write the project brain",
             "Create a concise CLAUDE.md for this repository (under 60 lines): stack, exact build and test "
             "commands, conventions you can infer from shipctl.py and tests/, the exit-code contract, protected "
             "files (SAFETY.md, .claude/settings.json, briefs/), and do-not rules. Then create two path-scoped "
             "rules with `paths:` frontmatter: .claude/rules/tests.md for tests/**/*.py and .claude/rules/cli.md "
             "for shipctl.py. Keep anything occasional out of CLAUDE.md. Do not commit."),
            ("Prove the context is applied",
             "Add a `shipctl stats` command that prints pending, done and overdue counts per owner. Follow "
             "CLAUDE.md and the rules in .claude/rules. When done, list which specific rules you applied and "
             "where, run the full test suite and show the raw output. Do not commit."),
        ],
        "evidence": ["`/memory` shows CLAUDE.md, rules and auto memory", "`/context` shows what loaded",
                     "Diff of `stats` follows `cmd_` naming, README table, test class conventions",
                     "Reviewed memory entries in docs/memory-review.md"],
        "discussion": [
            "What did you delete from your first CLAUDE.md draft, and why?",
            "When is a path-scoped rule better than a line in CLAUDE.md?",
            "Which auto-memory entries would you never keep?",
        ],
        "lab": "Write CLAUDE.md and the rules (Claude Code asks you to approve edits under .claude/: read them, then approve), start a fresh session, request the `stats` change, and check the diff against the rules. Open `/memory` and remove one stale entry.",
        "video": "Claude writes CLAUDE.md and two scoped rules, then implements `stats` and cites the rules it applied.",
    },
    {
        "n": 4, "slug": "04-notes-tournament", "minutes": 30, "project": "Project 4: Notes API Design Tournament",
        "title": "Best-of-N and better engineering decisions",
        "goals": [
            "Ask for genuinely different approaches, not cosmetic variants",
            "Score them on a fixed matrix: simplicity, testability, security, scalability, maintenance",
            "Avoid the first-answer-wins trap and incoherent hybrids",
            "Record the chosen and rejected approaches",
        ],
        "outputs": ["Working Notes API", "Three-option decision matrix", "Selected architecture with reasoning",
                    "Rejected Options Log"],
        "prompts": [
            ("Tournament (no code)",
             "Read briefs/notes-api.md. Follow the tournament rules exactly: write three genuinely different "
             "designs to designs/option-a-*.md, option-b-*.md and option-c-*.md, score them in "
             "decision/decision-matrix.md with the fixed weighted criteria, recommend a winner, and write "
             "decision/rejected-options-log.md with every required field. Do not write any implementation code. "
             "Stop and wait for my approval."),
            ("Implement the approved design",
             "I approve your recommended design. Implement it in notes_api/ with end-to-end tests in "
             "tests/test_notes_api.py that run a real server on an ephemeral port. Run the full test suite and "
             "show the raw output. Do not commit."),
        ],
        "evidence": ["Three design files that differ in shape", "Filled matrix with totals",
                     "Rejected Options Log with 'could become appropriate if'", "Raw test output"],
        "discussion": [
            "Were the three designs genuinely different? How can you tell?",
            "Which criterion weight would you change for your team?",
            "Under what conditions would the rejected option win?",
        ],
        "lab": "Run the tournament prompt. Before approving, push back once: ask Claude to defend the scores of the loser it ranked second.",
        "video": "Three designs, the weighted matrix, the Rejected Options Log, then the approved implementation with tests.",
    },
    {
        "n": 5, "slug": "05-resilient-notes", "minutes": 30, "project": "Project 5: Resilient Notes API",
        "title": "Testing, debugging, checkpoints and /goal",
        "goals": [
            "Generate meaningful tests and find missing edge cases",
            "Use a failing test as the debugging contract; investigate before editing",
            "Use checkpoints: /rewind → restore code without losing the conversation",
            "Use /goal for a measurable completion condition",
            "Separate test evidence from Claude's own completion claim",
        ],
        "outputs": ["Expanded test suite", "Documented diagnosis", "Verified bug fix", "Successful checkpoint restore",
                    "Completed Review Before Merge checklist"],
        "prompts": [
            ("Investigate before editing",
             "Read BUG-REPORT.md. Do not change any code yet. Reproduce BUG-101 with a failing regression test in "
             "tests/test_partial_update.py (title-only PATCH must keep the body; also cover body-only, explicit "
             "empty body and empty patch). Run it and show the failure. Then explain the most likely cause with "
             "file and line."),
            ("Measurable completion with /goal",
             "/goal BUG-101 is fixed with the smallest change in notes_api/service.py, "
             "python3 -m unittest discover -s tests -q exits 0 with the raw output shown, docs/diagnosis-bug-101.md "
             "records reproduce/cause/fix/evidence, and reviews/review-before-merge-bug-101.md completes all seven "
             "points of templates/review-before-merge-checklist.md with evidence. Do not commit."),
        ],
        "evidence": ["Failing test output before the fix", "One-line diff in service.py",
                     "Passing full suite", "/rewind restore of the deliberately bad attempt",
                     "Seven-point checklist with evidence"],
        "discussion": [
            "Why write the failing test before reading the code?",
            "What does /rewind restore, and what does it not restore?",
            "What makes a /goal condition checkable from the transcript?",
        ],
        "lab": "Try the deliberately heavy approach first (rewrite the repository update), then /rewind → Restore code, and apply the bounded fix.",
        "video": "Failing regression test, diagnosis to the exact line, /goal-driven fix, green suite and the completed checklist.",
    },
    {
        "n": 6, "slug": "06-isolated-search", "minutes": 25, "project": "Project 6: Isolated Search Feature",
        "title": "Git workflows, worktrees, permissions and sandboxing",
        "goals": [
            "Use feature branches and focused commits; review Claude-generated diffs",
            "Isolate experiments with `claude --worktree`",
            "Run parallel sessions without contaminating the main checkout",
            "Set filesystem and network boundaries with /sandbox",
            "Match autonomy to consequence and reversibility",
        ],
        "outputs": ["Isolated worktree", "Feature branch", "Search and tagging functionality", "Reviewed diff",
                    "Passing test suite", "Clean merge and commit history"],
        "prompts": [
            ("Build inside the worktree (`claude --worktree search-tags`)",
             "Read briefs/search-and-tags.md. Implement search and tags exactly as specified, keeping the layering "
             "(SQL only in repository.py, rules only in service.py). Add tests in tests/test_search_tags.py, "
             "including literal % and _ in search. Run the full suite and show the raw output. Then show "
             "git diff --stat against main. Do not commit and do not touch files outside notes_api/ and tests/."),
        ],
        "evidence": ["`git worktree list` shows `.claude/worktrees/search-tags`", "`git diff --stat main...`",
                     "Full suite green inside the worktree", "main untouched while the feature was built",
                     "Merge commit + worktree removed"],
        "discussion": [
            "What would have happened without the worktree?",
            "Which commands would you allow in a sandbox, and which network domains?",
            "When is a branch enough, and when do you want a worktree?",
        ],
        "lab": "Start `claude --worktree search-tags`, run the prompt, review the diff from main, run the tests yourself in the worktree, then merge and remove the worktree.",
        "video": "A real worktree session builds search and tags; review the diff from main, then merge.",
    },
    {
        "n": 7, "slug": "07-dashboard-wireframe", "minutes": 25, "project": "Project 7: Dashboard from a Wireframe",
        "title": "Multimodal building and Chrome verification",
        "goals": [
            "Turn a wireframe into components, states and interaction requirements",
            "Improve the prompt before patching generated UI by hand",
            "Connect Claude Code to Chrome (`claude --chrome`, /chrome)",
            "Test navigation and forms, inspect the console, check responsive layouts, capture evidence",
            "Convert findings into focused fixes",
        ],
        "outputs": ["Working dashboard", "Componentized frontend", "Browser verification evidence",
                    "Console and interaction issue log", "Before-and-after status for identified issues"],
        "prompts": [
            ("Build from the wireframe",
             "Look at wireframes/release-dashboard.png and read briefs/release-dashboard.md. First list the "
             "components, states and interactions you extracted from the image and its annotations. Then build "
             "the dashboard in dashboard/ and add the read-only GET /api/tasks route and static serving to the "
             "existing server, with node --test tests for the pure logic. Run both test suites and show the raw "
             "output. Do not commit."),
            ("Verify in Chrome (`claude --chrome`)",
             "Start the server with seeded data (python3 seed.py && python3 -m notes_api.server). Open "
             "http://localhost:8000/ in Chrome. Exercise the owner filter, status filter, both combined, search, "
             "and tag toggle on/off. Read the console. Resize to 390px wide. Record every issue in "
             "docs/browser-issue-log.md with evidence, fix them one by one, and re-verify each fix."),
        ],
        "evidence": ["Component/state list extracted from the image", "Desktop and 390 px screenshots",
                     "Console: no errors", "Issue log with before/after"],
        "discussion": [
            "What did Claude extract from the annotations that you would have missed?",
            "Which issues can only be found in a real browser?",
            "When do you fix the prompt instead of patching the UI?",
        ],
        "lab": "Build from the wireframe, then verify with `claude --chrome`. No Chrome? Use the browser verification checklist and the captured evidence in parts/07/evidence.",
        "video": "Claude reads the wireframe, builds the dashboard and verifies it; real screenshots at 1280 and 390 px.",
    },
    {
        "n": 8, "slug": "08-maintainer-dashboard", "minutes": 20, "project": "Project 8: Maintainer-Ready Dashboard",
        "title": "Refactor, document and create a maintainer handoff",
        "goals": [
            "Refactor with behaviour-preserving constraints",
            "Find duplication and unclear responsibilities; improve naming and structure",
            "Keep tests and browser checks as refactor guardrails",
            "Generate architecture notes, onboarding docs, known limitations and a handoff",
        ],
        "outputs": ["Refactored project structure", "Passing tests", "Updated README", "Architecture note",
                    "Maintainer handoff", "Known limitations and next steps"],
        "prompts": [
            ("Bounded refactoring plan (plan mode)",
             "Read REFACTOR-REQUEST.md. Propose a bounded refactoring plan for dashboard/app.js: target modules "
             "and their single responsibility, what will not change (HTML ids, API calls, rendering, behaviour), "
             "and how the existing tests and a browser check prove behaviour is preserved. Do not edit yet."),
            ("Implement, re-verify, hand off",
             "Plan approved. Implement it. Keep the existing test assertions (only import paths may change), run "
             "both test suites and show the raw output. Then write docs/ARCHITECTURE.md (one page), "
             "docs/HANDOFF.md (start here, how to change things safely, known limitations, ownership) and update "
             "README.md. Do not commit."),
        ],
        "evidence": ["Plan approved before edits", "Tests green with unchanged assertions",
                     "Screenshot diff before/after: only the timestamp differs", "ARCHITECTURE.md and HANDOFF.md"],
        "discussion": [
            "How do you prove a refactor changed nothing?",
            "What belongs in a handoff that a README never says?",
            "Which known limitation should block the next release?",
        ],
        "lab": "Run the plan prompt, cut one module from the plan, approve, implement, and compare screenshots before and after.",
        "video": "Plan, refactor into four modules, tests unchanged and green, pixel-identical screenshots, handoff docs.",
    },
    {
        "n": 9, "slug": "09-quality-pack", "minutes": 35, "project": "Project 9A: Engineering Quality Skills Pack",
        "title": "Skills, hooks and specialist subagents",
        "goals": [
            "Choose between CLAUDE.md, rules, Skills, hooks, MCP, subagents and Agent Teams",
            "Read SKILL.md structure: description, discovery, arguments, supporting files, forked context",
            "Use hooks as deterministic controls: post-edit tests, blocking unsafe commands",
            "Create specialist subagents with restricted tools",
        ],
        "outputs": ["Customized SKILL.md", "Working post-edit validation hook", "Specialist subagent definition",
                    "Structured review output"],
        "prompts": [
            ("Specialist review",
             "Use the security-reviewer subagent to review notes_api/ and dashboard/js/. It must cite file:line "
             "and quoted evidence for every finding and rank them by severity. Save its report to "
             "reviews/security-review-dashboard.md. Do not change any code."),
            ("Hook in action",
             "Make the release target date in dashboard/index.html read 2026-11-12 instead of 2026-11-10 and tell me "
             "what the post-edit validation hook reported. Then test our PreToolUse guardrail: the block-unsafe-commands "
             "hook is expected to stop secret reads before they run. Attempt exactly `cat .env` once (the file may not "
             "even exist) and report the hook's message word for word. Do not try any workaround."),
        ],
        "evidence": ["`/hooks` lists PreToolUse and PostToolUse", "Post-edit tests run automatically",
                     "`cat .env` blocked by the hook, although permissions allow cat", "Severity-ranked review with file:line"],
        "discussion": [
            "Which rule in your team should be a hook, not an instruction?",
            "Why does the security reviewer get only Read, Grep and Glob?",
            "What would make a skill trigger automatically, and when should it not?",
        ],
        "lab": "Customize the description and add a Shipyard section to change-review/SKILL.md, wire the hooks in settings.json, then run the two prompts.",
        "video": "Read-only security reviewer finds the stored XSS with file:line; the hook blocks a force push.",
    },
    {
        "n": 10, "slug": "10-plugin", "minutes": 25, "project": "Project 9B: Package the Engineering Quality Plugin",
        "title": "Plugins and marketplace distribution",
        "goals": [
            "Package Skills, hooks, subagents and MCP configuration as one plugin",
            "Write the manifest; understand namespacing",
            "Validate (`claude plugin validate --strict`), install and test locally",
            "Distribute through a marketplace; version, trust and maintain",
        ],
        "outputs": ["Validated Claude Code plugin", "Local plugin installation", "Successful namespaced invocation",
                    "Distribution README"],
        "prompts": [
            ("Package",
             "Read briefs/package-plugin.md. Package our .claude/ change-review skill, a security-review skill, "
             "the security-reviewer agent and both hooks into plugins/engineering-quality/ with a valid "
             ".claude-plugin/plugin.json and hooks/hooks.json using ${CLAUDE_PLUGIN_ROOT}. Add the marketplace "
             "file .claude-plugin/marketplace.json named shipyard-tools. Run claude plugin validate on both with "
             "--strict and show the output. Do not commit."),
            ("Namespaced invocation (`claude --plugin-dir ./plugins/engineering-quality`)",
             "/engineering-quality:change-review briefs/package-plugin.md"),
        ],
        "evidence": ["`claude plugin validate … --strict` → Validation passed",
                     "`claude plugin install engineering-quality@shipyard-tools`",
                     "`claude plugin details` inventory and token cost", "Namespaced skill output"],
        "discussion": [
            "What would you put in a plugin, and what stays in CLAUDE.md?",
            "How do you trust a plugin from another team?",
            "When do you bump the version?",
        ],
        "lab": "Package, validate with --strict, install from the local marketplace, run `/engineering-quality:change-review`.",
        "video": "Plugin packaged and validated, installed from a local marketplace, invoked by its namespaced name.",
    },
    {
        "n": 11, "slug": "11-agent-team", "minutes": 30, "project": "Project 9C: Parallel Feature Sprint",
        "title": "Agent Teams: ship a feature in parallel",
        "goals": [
            "Choose between subagents and Agent Teams; background sessions and agent view",
            "Lead and teammate roles, shared task list, direct messages, plan approval",
            "Avoid file conflicts with explicit ownership; quality gates for parallel work",
            "Monitor token and coordination cost",
        ],
        "outputs": ["Parallel task plan", "Explicit role and file ownership", "Integrated feature", "Passing tests",
                    "Team review and retrospective", "Documented coordination risks"],
        "prompts": [
            ("Launch the team (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)",
             "Read briefs/release-notes-team.md. Create an agent team with three teammates: backend owner, "
             "frontend owner, and test and verification owner, each restricted to the files listed in the brief. "
             "Require plan approval before any teammate edits. Freeze the API contract from the brief first, "
             "write the task list with dependencies to docs/team-plan.md, then let the teammates work in parallel. "
             "When all tasks are done, run both test suites, show the raw output, and summarise what each teammate "
             "changed. Do not commit."),
            ("Steer one teammate",
             "Message the frontend owner: the panel must show an empty-state message when the release has no "
             "notes, and the Copy button must say \"Copied\" for 1.5 seconds."),
        ],
        "evidence": ["Task list with owners and dependencies", "No file edited by two teammates",
                     "Both suites green after integration",
                     "`/engineering-quality:change-review` before acceptance", "Retrospective + token cost"],
        "discussion": [
            "When is an Agent Team worth the extra tokens?",
            "What made parallel work safe here?",
            "What would you change in the plan approval step?",
        ],
        "lab": "Watch the instructor's team, steer one teammate, then review the integrated diff with the plugin. No access? Use the transcript, task board and checkpoint in parts/11.",
        "video": "The team builds release notes in parallel: backend endpoint, frontend panel, tests, integrated and green.",
    },
    {
        "n": 12, "slug": "12-production-readiness", "minutes": 25, "project": "Project 10A: Production Readiness Review",
        "title": "Production readiness, security and code review",
        "goals": [
            "Prototype versus production expectations",
            "Review dependencies, secrets, input validation, authN/authZ, permissions, errors, performance, rollback",
            "Use /security-review, /code-review and ultrareview (`/code-review ultra`)",
            "Separate verified findings from speculative concerns; prioritise by severity, effort and impact",
        ],
        "outputs": ["Security review", "Code review findings", "Top three prioritized fixes", "Named owner",
                    "Verification plan", "Production readiness decision"],
        "prompts": [
            ("Production review",
             "Read briefs/production-review.md. Run /engineering-quality:security-review on notes_api/ and "
             "dashboard/js/, then review the rest yourself. Write reports/production-readiness.md with: risk "
             "summary, severity-ranked findings each with evidence (file:line, config, test or runtime output you "
             "actually ran), a separate list of speculative concerns, top three fixes with owner and verification "
             "action, and a Go / Conditional go / No-go recommendation. Do not fix anything."),
        ],
        "evidence": ["Stored XSS proven at runtime", "Bind 0.0.0.0 + CORS * proven by the probe",
                     "Oversized request blocks a worker", "Top 3 fixes with owners and verification",
                     "Decision: Conditional go"],
        "discussion": [
            "Which finding would you have missed without runtime evidence?",
            "What turns a speculative concern into a verified finding?",
            "Would you sign the conditional go?",
        ],
        "lab": "Run the review on your own project. Every High finding needs a command and its output.",
        "video": "Security review with file:line evidence, runtime proof, top three fixes and a conditional go.",
    },
    {
        "n": 13, "slug": "13-cowork-handoff", "minutes": 20, "project": "Project 10B: Stakeholder Handoff",
        "title": "Claude Cowork: engineering output to stakeholder update",
        "goals": [
            "Extend agentic work beyond code: reports, spreadsheets, presentations, documents",
            "Keep technical accuracy while translating risk into business impact",
            "Cowork permissions, local file access, reviewing browser and connector actions",
            "Manual, automatic and skipped approval modes",
        ],
        "outputs": ["Stakeholder-ready release update", "Risk and decision summary", "Follow-up action list",
                    "Named owners and next steps"],
        "prompts": [
            ("Cowork (or the stakeholder-update skill)",
             "Read reports/production-readiness.md, docs/HANDOFF.md and docs/team-plan.md. Write "
             "reports/stakeholder-update.md: one page for a VP of Engineering reading on a phone, with exactly "
             "these sections: current release status, features completed, customer or business impact, major "
             "risks (plain language, severities unchanged), decisions required, top three fixes, owners and "
             "deadlines (no invented dates), recommended next step."),
        ],
        "evidence": ["One page, eight sections", "Severities match the readiness report",
                     "No invented dates", "Every connector/browser action reviewed before approval"],
        "discussion": [
            "What did the update leave out on purpose?",
            "How do you keep severity honest in business language?",
            "Which approval mode would you use for Cowork in your company?",
        ],
        "lab": "Give Cowork the folder and the prompt. No Cowork? Run `/stakeholder-update` from the Skills Pack with the same inputs.",
        "video": "The readiness report becomes a one-page stakeholder update with honest severities and owners.",
    },
    {
        "n": 14, "slug": "14-remote-routine", "minutes": 20, "project": "Project 10C: Cross-Device Continuation",
        "title": "Web, mobile, Remote Control and work that continues",
        "goals": [
            "Move between terminal, desktop, web and mobile",
            "Continue a local session with Remote Control; monitor and steer from another device",
            "Local sessions versus cloud sessions; when local context or credentials are required",
            "Routines and scheduled work; safe automation with clear stop conditions",
        ],
        "outputs": ["Cross-device continuation checklist", "Remote verification status update",
                    "Post-release routine brief"],
        "prompts": [
            ("Remote Control (`claude --remote-control \"Shipyard v1.4 verification\"`)",
             "Run both test suites and python3 scripts/readiness_probe.py (it starts its own server), then write a five-line verification status to "
             "ops/remote-verification-status.md: test totals with the raw summary lines, probe results, verdict "
             "GREEN/YELLOW/RED and the next step. Stop after writing the file; do not edit anything else."),
            ("Design the routine",
             "Write ops/post-release-routine.md using templates/post-release-routine-brief.md: a recurring post-release check for this repository with trigger, "
             "repository scope, required permissions (least privilege), expected output, the human approval point, "
             "and the completion or stop condition. Say what must stay local and what can run as a cloud routine."),
        ],
        "evidence": ["Session visible on claude.ai/code and the mobile app", "Steered once from the phone",
                     "Status file written by the remote session", "Routine brief with stop conditions"],
        "discussion": [
            "What must never run unattended?",
            "What stays local, and why?",
            "What is your stop condition for a routine that fails twice?",
        ],
        "lab": "Design your own post-release routine with the template; trade it with a neighbour and find one missing stop condition.",
        "video": "Verification runs, a status file is written, and a post-release routine brief with stop conditions is designed.",
    },
]

FINAL = {"title": "Final Q&A and exam briefing", "minutes": 25}


def schedule():
    """Yield (kind, label, start, end, minutes) for every block of the day."""
    h, m = map(int, START.split(":"))
    t = h * 60 + m
    fmt = lambda x: f"{x // 60:02d}:{x % 60:02d}"  # noqa: E731
    for part in PARTS:
        yield "part", part, fmt(t), fmt(t + part["minutes"]), part["minutes"]
        t += part["minutes"]
        if part["n"] in BREAKS:
            label, mins = BREAKS[part["n"]]
            yield "break", label, fmt(t), fmt(t + mins), mins
            t += mins
    yield "final", FINAL["title"], fmt(t), fmt(t + FINAL["minutes"]), FINAL["minutes"]
