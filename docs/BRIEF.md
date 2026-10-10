<!-- Extracted verbatim from the Packt brief "Claude Code Bootcamp: Cohort 2" (.docx). Tables are flattened: one cell per line. -->

# Claude Code Bootcamp: Cohort 2

## Build, Orchestrate, Review, and Ship with 10 new advanced Hands-On Projects in one day
Instructor: Luca Berton
Duration: 7.5 hours  6 hours + 30 mins Q&A and 30 mins break
Schedule: 10:00 AM to 4:30 PM ET
Format: Live virtual workshop with guided builds, instructor demonstrations, hands-on labs, review checkpoints, assessment, and certification
Level: Beginner to intermediate

## Primary Tagline
Build faster. Orchestrate smarter. Verify everything. Ship with confidence.

## Workshop Overview
Claude Code has evolved far beyond a command-line coding assistant. It can now work across the complete software engineering lifecycle, from planning and implementation to browser verification, parallel agent coordination, security review, automation, and stakeholder delivery.
In this intensive 7.5-hour bootcamp, learners will complete 10 connected hands-on projects using Claude Code, Skills, hooks, subagents, plugins, Agent Teams, Claude in Chrome, Cowork, and Remote Control.
By the end of the workshop, learners will have working applications, safer Git and sandbox workflows, a reusable Claude Code Skills Pack, and a repeatable process for taking software from an engineering brief to a production readiness decision.

# Who Should Attend
This workshop is designed for:
- Software developers
- Tech leads and engineering managers
- DevOps and platform engineers
- Automation engineers
- AI engineers
- Technical product builders
- Professionals already using AI coding tools who want a more structured engineering workflow

# Prerequisites
Learners should have:
- Basic programming knowledge
- Familiarity with Git
- Claude Code installed and activated
- A local development environment
- Node.js or Python installed
- Google Chrome for browser verification exercises
- A GitHub account for selected workflows
Advanced features that are experimental or dependent on a particular Claude plan will include instructor demonstrations and downloadable fallback materials.

# Learning Outcomes
By completing this workshop, learners will be able to:
- Delegate substantial engineering tasks using constraints, acceptance criteria, and verification of evidence.
- Configure project context with CLAUDE.md, scoped rules, and auto memory.
- Use Best-of-N to compare solution approaches and document rejected alternatives.
- Generate meaningful tests, debug failures, use checkpoints, and work toward measurable completion conditions.
- Isolate AI-generated work with permissions, sandboxing, branches, and worktrees.
- Convert wireframes and screenshots into working interfaces.
- Verify generated applications in Chrome using real browser evidence.
- Refactor and document applications without changing expected behavior.
- Create reusable SKILL.md workflows, hooks, and specialist subagents.
- Package Claude Code extensions as plugins and understand marketplace distribution.
- Coordinate parallel engineering work with Agent Teams.
- Run security and code reviews that produce prioritized, actionable findings.
- Convert engineering reports into stakeholder-ready outputs using Claude Cowork.
- Continue Claude Code work across desktop, web, terminal, and mobile.

# Exact 6 -Hour Schedule
| Part
| Time
| Session
| Duration
| 1
| 9:00-9:20
| Welcome, setup, AI-first mindset, and safe delegation
| 20m
| 2
| 9:20-9:45
| Prompting like a tech lead: CLI Task Manager
| 25m
| 3
| 9:45-10:10
| CLAUDE.md, scoped rules, and auto memory
| 25m
| 10:10-10:20
| Break
| 10m
| 4
| 10:20-10:50
| Best-of-N: Notes API and Rejected Options Log
| 30m
| 5
| 10:50-11:20
| Testing, debugging, checkpoints, and /goal
| 30m
| 6
| 11:20-11:45
| Git workflows, worktrees, permissions, and sandboxing
| 25m
| 11:45-11:55
| Break
| 10m
| 7
| 11:55-12:20
| Multimodal building and Chrome verification
| 25m
| 12:20-1:00
| Lunch
| 40m
| 8
| 1:00-1:20
| Refactor, document, and create a maintainer handoff
| 20m
| 9
| 1:20-1:55
| Skills, hooks, and specialist subagents
| 35m
| 10
| 1:55-2:20
| Plugins and marketplace distribution
| 25m
| 11
| 2:20-2:50
| Agent Teams: ship a feature in parallel
| 30m
| 2:50-3:00
| Break
| 10m
| 12
| 3:00-3:25
| Production readiness, security, and code review
| 25m
| 13
| 3:25-3:45
| Claude Cowork: engineering output to stakeholder update
| 20m
| 14
| 3:45-4:05
| Web, mobile, Remote Control, and cross-device work
| 20m
| 4:05-4:30
| Final Q&A and exam briefing
| 25m
Total duration: 450 minutes, exactly 7.5 hours.

# The 10 Hands-On Projects

## Project 1: AI-Ready Engineering Workspace
Learners configure a safe Claude Code workspace, establish permission boundaries, initialize Git, and create a recovery point.

## Project 2: CLI Release Task Manager
Learners use a structured engineering brief to build a command-line task manager with tests and documentation.

## Project 3: Project Brain
Learners create a reusable CLAUDE.md, path-scoped rules, and a reviewed auto-memory setup.

## Project 4: Notes API Design Tournament
Learners compare three genuinely different backend designs, select one, and document why the others were rejected.

## Project 5: Resilient Notes API
Learners add tests, diagnose a seeded defect, use checkpoints, and verify completion against a measurable goal.

## Project 6: Isolated Search Feature
Learners use a worktree and feature branch to add search and tagging without destabilizing the main project.

## Project 7: Dashboard from a Wireframe
Learners turn a visual brief into a componentized dashboard and verify the application in Chrome.

## Project 8: Maintainer-Ready Dashboard
Learners refactor the dashboard, preserve its behavior, and generate a developer handoff.

## Project 9: Engineering Quality Plugin and Parallel Feature Sprint
Learners create Skills, hooks, and subagents, package them as a plugin, and apply them during an Agent Team feature build.

## Project 10: Production Readiness and Stakeholder Handoff
Learners run a production review, prioritize fixes, assign ownership, and turn the findings into a stakeholder-ready Cowork update.

# Detailed Workshop Curriculum

## Part 1: Welcome, Setup, and the AI-First Engineering Mindset
Time: 20 minutes
Project 1: AI-Ready Engineering Workspace

### Topics
- What Claude Code can do across CLI, IDE, desktop, web, and mobile
- The current Claude Code engineering lifecycle
- Plan, implement, verify, review, and commit
- Choosing the right model, context, and effort for a task
- Permission modes and workspace trust
- Safe delegation versus blind trust
- Reversible versus irreversible actions
- Establishing recovery points before autonomous work

### Safe Delegation Example
Blind trust:
“Update every dependency, fix whatever breaks, and deploy the application.”
Safe delegation:
“Inspect the dependency list and propose an upgrade plan. Do not modify deployment configuration or production credentials. Update only the approved packages in an isolated branch, run the complete test suite, document breaking changes, and stop for review before merging.”

### Hands-On Activity
Learners initialize the starter repository, verify their Claude Code environment, choose a permission mode, establish allowed and blocked actions, and create a baseline Git commit.

### Learner Output
- Working Claude Code environment
- Trusted starter repository
- Written permission and safety boundary
- Baseline Git commit and recovery point

## Part 2: Prompting Claude Code Like a Tech Lead
Time: 25 minutes
Project 2: CLI Release Task Manager

### Topics
- Small prompts versus complete engineering briefs
- Defining the desired outcome
- Providing relevant project context
- Setting constraints and protected areas
- Writing acceptance criteria
- Requiring proof instead of accepting completion claims
- Asking Claude to plan before coding
- Reviewing and challenging the implementation plan
- Intervening at decision points without micromanaging

### Hands-On Activity
Learners ask Claude Code to build a CLI release task manager with the following capabilities:
- Add a release task
- Assign an owner
- Set a due date
- List pending tasks
- Mark tasks as completed
- Delete tasks
- Filter tasks by owner or status
Claude must propose a plan, implement the application, generate tests, and explain how the evidence satisfies the acceptance criteria.

### Learner Output
- Working CLI application
- Structured engineering brief
- Test suite
- Acceptance evidence
- README with usage examples

## Part 3: Build the Project Brain with CLAUDE.md, Rules, and Auto Memory
Time: 25 minutes
Project 3: Project Brain

### Topics
- What belongs in CLAUDE.md
- What should not be placed in CLAUDE.md
- Architecture notes and project conventions
- Build, test, and validation commands
- Security requirements
- Protected files and “do not touch” areas
- Keeping CLAUDE.md concise
- Using .claude/rules for directory-specific or language-specific instructions
- Moving occasional reference material into Skills
- How auto memory works
- Reviewing, correcting, and removing stale memory

### Hands-On Activity
Learners create a concise CLAUDE.md for the starter workspace, add one path-scoped rule, and ask Claude to make a change that demonstrates whether the context has been applied correctly.

### Learner Output
- Reusable CLAUDE.md
- Path-scoped project rule
- Documented coding and testing conventions
- Reviewed auto-memory entry
- Evidence that Claude followed the project context

## Part 4: Best-of-N and Better Engineering Decisions
Time: 30 minutes
Project 4: Notes API Design Tournament

### Topics
- What Best-of-N means in software engineering
- Asking for genuinely different approaches
- Avoiding cosmetic variations of the same design
- Comparing simplicity, testability, security, scalability, and maintenance
- Combining strong ideas without creating an incoherent hybrid
- Avoiding the first-answer-wins trap
- Recording both the chosen and rejected approaches

### Hands-On Activity
Learners ask Claude Code to propose three different backend designs for a Notes API. The options are evaluated using a fixed decision matrix.
The selected design is implemented only after the comparison is complete.

### Required Rejected Options Log
For every rejected design, learners record:
- Summary of the approach
- Main advantages
- Main disadvantages
- Primary reason for rejection
- Conditions under which the approach may become appropriate later

### Learner Output
- Working Notes API
- Three-option decision matrix
- Selected architecture with reasoning
- Rejected Options Log

## Part 5: Testing, Debugging, Checkpoints, and Verifiable Completion
Time: 30 minutes
Project 5: Resilient Notes API

### Topics
- Generating meaningful tests rather than superficial coverage
- Asking Claude to identify missing edge cases
- Using failing tests as debugging contracts
- Asking Claude to investigate before editing
- Checkpointing and rewind
- Restoring files without discarding the entire conversation
- Using /goal for a measurable completion condition
- Separating test evidence from Claude’s own completion claim
- Knowing when human review is required

### Hands-On Activity
Learners receive a seeded defect in the Notes API. Claude must:
- Reproduce the failure.
- Explain the likely cause.
- Add a failing regression test.
- Implement a bounded fix.
- Run the relevant test suite.
- Demonstrate that the regression test now passes.
- Complete the Review Before Merge checklist.
Learners deliberately try one unsuccessful approach and use checkpointing to return to a known working state.

### Review Before Merge Checklist
- Scope: Did the change stay within the approved files and acceptance criteria?
- Diff: Can I explain every material line that changed?
- Tests: Do the relevant tests pass, including new edge cases?
- Security: Were secrets, dependencies, permissions, and unsafe inputs checked?
- Runtime: Was the feature verified in the real interface?
- Rollback: Is there a clean checkpoint, branch, or commit to return to?
- Handoff: Are risks, documentation, ownership, and next steps clear?

### Learner Output
- Expanded test suite
- Documented diagnosis
- Verified bug fix
- Successful checkpoint restore
- Completed Review Before Merge checklist

## Part 6: Git Workflows, Worktrees, Permissions, and Sandboxing
Time: 25 minutes
Project 6: Isolated Search Feature

### Topics
- Why Git becomes more important with agentic coding
- Feature branches and focused commits
- Reviewing Claude-generated diffs
- Safe rollback
- Worktrees for isolated experiments
- Parallel sessions without contaminating the main checkout
- Filesystem and network boundaries
- Sandboxed command execution
- Matching autonomy to consequence and reversibility

### Hands-On Activity
Learners create an isolated worktree and ask Claude Code to add search and tagging to the Notes API.
Claude implements the feature inside the worktree. Learners review the diff, run tests, inspect unexpected changes, and only then merge the feature.

### Learner Output
- Isolated worktree
- Feature branch
- Search and tagging functionality
- Reviewed diff
- Passing test suite
- Clean merge and commit history

## Part 7: Multimodal Building with Claude in Chrome
Time: 25 minutes
Project 7: Dashboard from a Wireframe

### Topics
- Using screenshots, sketches, and wireframes
- Turning visual requirements into components and states
- Extracting layout, navigation, and interaction requirements
- Improving the prompt before manually patching generated UI
- Connecting Claude Code to Chrome
- Testing navigation and form behavior
- Inspecting console errors
- Checking responsive layouts
- Capturing browser evidence
- Converting verification findings into focused fixes

### Hands-On Activity
Learners use a supplied wireframe to build a release dashboard. Claude opens the application in Chrome, tests the core user flow, inspects console output, records issues, and applies a verified fix.

### Learner Output
- Working dashboard
- Componentized frontend
- Browser verification evidence
- Console and interaction issue log
- Before-and-after status for identified issues

### Fallback Path
Learners who cannot use the Chrome integration receive captured browser evidence and complete the same review using a manual verification checklist.

## Part 8: Refactor, Document, and Create a Maintainer Handoff
Time: 20 minutes
Project 8: Maintainer-Ready Dashboard

### Topics
- Refactoring with behavior-preserving constraints
- Identifying duplication and unclear responsibilities
- Improving naming and project structure
- Keeping tests and browser checks as refactor guardrails
- Generating architecture notes
- Writing useful onboarding documentation
- Recording known limitations
- Creating a developer handoff
- Sharing visual outputs as artifacts where appropriate

### Hands-On Activity
Learners ask Claude Code to propose a bounded refactoring plan. After reviewing the plan, they allow Claude to implement it, rerun verification, and create a maintainer handoff.

### Learner Output
- Refactored project structure
- Passing tests
- Updated README
- Architecture note
- Maintainer handoff
- Known limitations and next steps

## Part 9: Skills, Hooks, and Specialist Subagents
Time: 35 minutes
Project 9A: Engineering Quality Skills Pack

### Topics
- Choosing between CLAUDE.md, rules, Skills, hooks, MCP, subagents, and Agent Teams
- SKILL.md structure
- Skill descriptions and automatic discovery
- Action Skills versus reference Skills
- Progressive loading and supporting files
- Passing arguments into Skills
- Running Skills in forked context
- Background and nested subagents
- Hooks as deterministic engineering controls
- Post-edit formatting and test hooks
- Blocking unsafe commands
- Creating specialist security, test, and documentation agents
- Tool and permission restrictions for subagents

### Hands-On Activity
Learners customize a supplied change-review/SKILL.md, configure a post-edit validation hook, define a security reviewer subagent, and apply the complete workflow to their dashboard project.

### Learner Output
- Customized SKILL.md
- Working post-edit validation hook
- Specialist subagent definition
- Structured review output

## Part 10: Plugins and Marketplace Distribution
Time: 25 minutes
Project 9B: Package the Engineering Quality Plugin

### Topics
- Plugins as the packaging layer
- Bundling Skills, hooks, subagents, and MCP configurations
- Plugin folder structure
- Plugin manifests
- Namespaced Skills and commands
- Validating a plugin
- Installing and testing locally
- Marketplace concepts
- Versioning and dependencies
- Plugin trust and maintenance
- Distributing plugins across teams and repositories

### Hands-On Activity
Learners package the Skill, hook, and security reviewer from Part 9 into one Engineering Quality plugin. They validate it, install it locally, and invoke its namespaced review workflow.

### Learner Output
- Validated Claude Code plugin
- Local plugin installation
- Successful namespaced invocation
- Distribution README

## Part 11: Agent Teams and Parallel Feature Delivery
Time: 30 minutes
Project 9C: Parallel Feature Sprint

### Topics
- Subagents versus Agent Teams
- Background sessions and agent view
- When to use worktrees
- Agent Team lead and teammate roles
- Shared task lists
- Direct communication between teammates
- Assigning and claiming tasks
- Requiring plan approval
- Avoiding file conflicts
- Quality gates for parallel work
- Monitoring token and coordination cost
- Dynamic workflows as a scaling path for larger tasks

### Hands-On Activity
The instructor launches a three-role Agent Team:
- Frontend owner
- Backend owner
- Test and verification owner
The team adds release notes functionality to the dashboard. Learners monitor the shared tasks, steer one teammate, review the integrated output, and apply the Engineering Quality plugin before accepting the feature.

### Learner Output
- Parallel task plan
- Explicit role and file ownership
- Integrated feature
- Passing tests
- Team review and retrospective
- Documented coordination risks

### Important Availability Note
Agent Teams are currently experimental and disabled by default. The instructor will run the canonical live build. Learners without access will receive the team transcript, task board, diffs, and repository checkpoint needed to complete the review exercise.

## Part 12: Production Readiness with Security and Code Review
Time: 25 minutes
Project 10A: Production Readiness Review

### Topics
- Prototype versus production expectations
- Dependency review
- Secrets and environment variables
- Input validation
- Authentication and authorization
- Permission boundaries
- Error handling
- Performance and maintainability
- Deployment and rollback readiness
- Security Guidance and Claude Security
- Claude Code Review
- Deep multi-agent review and ultrareview
- Separating verified findings from speculative concerns
- Prioritizing by severity, effort, and business impact

### Hands-On Activity
Learners run a structured production review on one of their workshop projects. Every important finding must be connected to code, configuration, test, or runtime evidence.

### Required Production Readiness Report
The report must contain:
- Concise risk summary
- Severity-ranked findings
- Evidence for each significant finding
- Top three fixes
- Recommended next-step owner
- Verification action
- Go, conditional go, or no-go recommendation

### Learner Output
- Security review
- Code review findings
- Top three prioritized fixes
- Named owner
- Verification plan
- Production readiness decision

## Part 13: Claude Cowork for Stakeholder Delivery
Time: 20 minutes
Project 10B: Stakeholder Handoff

### Topics
- How Cowork extends Claude’s agentic capabilities beyond coding
- Moving from technical files to professional business outputs
- Creating reports, spreadsheets, presentations, and stakeholder documents
- Using engineering evidence without losing technical accuracy
- Cowork permissions and local file access
- Reviewing browser and connector actions
- Manual, automatic, and skipped approval modes
- Converting technical risk into business impact

### Hands-On Activity
Learners provide their production readiness report and maintainer handoff to Cowork.
Cowork creates a one-page stakeholder update containing:
- Current release status
- Features completed
- Customer or business impact
- Major risks
- Decisions required
- Top three fixes
- Owners and deadlines
- Recommended next step

### Learner Output
- Stakeholder-ready release update
- Risk and decision summary
- Follow-up action list
- Named owners and next steps

### Access Note
Cowork requires a paid Claude plan, and availability can vary across surfaces. The instructor will demonstrate the complete workflow. Learners without access can use the supplied stakeholder-update Skill and document template.

## Part 14: Web, Mobile, Remote Control, and Work That Continues
Time: 20 minutes
Project 10C: Cross-Device Continuation

### Topics
- Moving between terminal, desktop, web, and mobile
- Continuing a local session with Remote Control
- Monitoring and steering work from another device
- Local sessions versus cloud sessions
- Knowing when local context or credentials are required
- Routines and scheduled work
- Recurring code review and release verification
- Computer use and browser actions
- Designing safe automation with clear stop conditions

### Hands-On Activity
The instructor starts a local verification task, connects it to Remote Control, and continues monitoring it from another surface.
Learners then design a safe post-release monitoring routine with:
- Trigger
- Repository or project scope
- Required permissions
- Expected output
- Human approval point
- Completion or stop condition

### Learner Output
- Cross-device continuation checklist
- Remote verification status update
- Post-release routine brief

# Final Q&A and Exam Briefing
Time: 25 minutes

### Topics
- Common Claude Code mistakes
- Prompting and delegation anti-patterns
- When not to use Agent Teams
- When a Skill is better than CLAUDE.md
- When a hook should enforce a rule
- Managing costs and context
- Maintaining the attendee Skills Pack
- Assessment format
- Passing criteria
- Learner questions

# Free Claude Code Skills Pack
Every attendee receives a reusable Claude Code Skills Pack containing:

## Included Skills
- feature-brief/SKILL.md
Converts an idea into scope, constraints, acceptance criteria, and proof.
- best-of-n-decision/SKILL.md
Generates distinct approaches, evaluates trade-offs, and creates a Rejected Options Log.
- change-review/SKILL.md
Applies the seven-point Review Before Merge checklist.
- test-debug-loop/SKILL.md
Guides Claude from failing test to diagnosis, fix, regression check, and evidence.
- browser-verification/SKILL.md
Verifies web features using a repeatable Chrome and UI checklist.
- security-review/SKILL.md
Reviews secrets, dependencies, inputs, authentication, permissions, and unsafe flows.
- release-readiness/SKILL.md
Creates a risk summary, top fixes, owner, verification step, and release recommendation.
- stakeholder-update/SKILL.md
Converts engineering evidence into a concise business-facing update.

## Additional Downloadable Assets
- CLAUDE.md starter template
- Scoped rules examples
- Formatting and test hooks
- Unsafe-command blocking hook
- Security reviewer subagent
- Test verifier subagent
- Plugin scaffold
- Best-of-N decision matrix
- Rejected Options Log
- Review Before Merge checklist
- Production readiness report template
- Stakeholder update template
- Starter repository and project checkpoints
- Agent Team transcript and fallback materials

# Assessment and Certification

## Assessment Structure
Component
Evidence
Weight
Scenario-based knowledge quiz
Permissions, feature selection, context, security, and workflow decisions
30%
Practical capstone
Working change, tests, diff, verification, and readiness report
50%
Engineering reflection
Rejected approach, human checkpoint, and unresolved risk
20%

## Passing Criteria
Learners must:
- Score 70% or higher overall
- Score at least 60% on the practical capstone
- Submit genuine test or runtime evidence
- Include a risk summary, top three fixes, named owner, and verification step
- Avoid automatic-fail conditions such as exposed credentials, fabricated test results, or unsafe irreversible actions

## Certificate Title

# Free Attendee Resources and Certification Readiness
Every attendee will receive two separate learning benefits:
- A Packt Certificate of Completion for successfully completing the workshop assessment.
- A free preparation pack for the Claude Certified Associate – Foundations certification offered by Anthropic.

## Free Claude Code Skills Pack
Attendees will receive eight complete, ready-to-use SKILL.md workflows. These are working files that can be downloaded, inspected, customized, and installed in their own Claude Code environment.

### Included SKILL.md Files
- feature-brief/SKILL.md
Converts an idea or feature request into a structured engineering brief containing scope, constraints, acceptance criteria, protected areas, and required evidence.
- best-of-n-decision/SKILL.md
Generates multiple genuinely different approaches, evaluates their trade-offs, and produces a Rejected Options Log.
- change-review/SKILL.md
Applies the seven-point Review Before Merge checklist to Claude-generated code changes.
- test-debug-loop/SKILL.md
Guides Claude from a failing test through diagnosis, implementation, regression testing, and final verification.
- browser-verification/SKILL.md
Provides a repeatable process for verifying a web application using Claude in Chrome.
- security-review/SKILL.md
Reviews secrets, dependencies, input validation, authentication, authorization, permissions, and unsafe data flows.
- release-readiness/SKILL.md
Generates a production readiness report containing risks, evidence, top fixes, owners, verification actions, and a release recommendation.
- stakeholder-update/SKILL.md
Converts technical findings into a concise stakeholder update containing business impact, risks, decisions, owners, and next steps.

## Additional Downloadable Resources
The Skills Pack will also include:
- CLAUDE.md starter template
- Scoped .claude/rules examples
- Formatting and test hooks
- Unsafe-command blocking hook
- Security reviewer subagent
- Test verifier subagent
- Plugin scaffold
- Best-of-N decision matrix
- Rejected Options Log
- Review Before Merge checklist
- Production readiness report template
- Stakeholder update template
- Starter repository
- Completed project checkpoints
- Agent Team transcript and fallback materials
- Claude Code certification study checklist

## How the Skills Pack Is Used During the Workshop
The Skills Pack will not be treated only as a post-workshop giveaway.
During the workshop, learners will:
- Install a supplied Skill
- Examine the structure of a SKILL.md file
- Customize the Skill description and instructions
- Add supporting reference files
- Run the Skill against a real project
- Combine a Skill with a hook and specialist subagent
- Package the complete workflow as a plugin
- Learn how to reuse the Skills across other repositories
This ensures learners understand how the files work rather than downloading a collection of unexplained prompts.

# Free Claude Certified Associate Foundations:
- Claude Certified Developer - Foundations:
- Claude Certified Architect - Foundations: Foundations Mock Test
Every attendee will receive a free full-length mock test designed to support preparation for the Claude Certified Foundations certifications, Anthropic currently offers 4 certifications,

## Mock Test Format
- 60 original scenario-based questions
- 120-minute recommended time limit
- Multiple-choice and multiple-response questions
- Questions covering all seven certification domains
- Detailed explanation for every correct and incorrect option
- Domain-level performance report
- Personalized study recommendations
- Links to relevant official Claude documentation
- Unlimited attempts for workshop attendees

## Mock Test Domain Distribution
Domain
Weight
Questions
Prompting and Task Execution
14%
8
Output Evaluation and Validation
21%
13
Product and Model Selection
12%
7
Workflow Integration and Solution Design
16%
10
Configuration and Knowledge Management
12%
7
Governance, Risk, and Responsible Use
15%
9
Troubleshooting and Optimization
10%
6
Total
100%
60

## Mock Test Scenarios
Questions will be based on realistic workplace situations such as:
- Improving an incomplete or ambiguous prompt
- Detecting an unsupported claim in Claude’s output
- Choosing between Claude Chat, Projects, Claude Code, Cowork, Artifacts, and Research
- Selecting an appropriate Claude model based on quality, speed, and cost
- Deciding when human review is required
- Protecting confidential or regulated information
- Designing a workflow with appropriate approval checkpoints
- Creating reusable project instructions
- Managing outdated knowledge and context
- Troubleshooting poor or inconsistent outputs
- Communicating Claude’s capabilities and limitations to stakeholders
- Deciding whether a task should be automated

## Readiness Scoring
The official examination uses scaled scoring, which cannot be reproduced precisely by an independent mock test.
For the Packt mock test, the recommended readiness levels will be:
- 80% or higher: Strong exam readiness
- 70% to 79%: Nearly ready, with focused revision recommended
- 60% to 69%: Additional study required
- Below 60%: Revisit the learning path before scheduling the official exam
The mock test score does not guarantee success in the official examination.

## Certification Readiness Report
After completing the mock test, learners will receive:
- Overall score
- Score by certification domain
- Strongest domain
- Weakest domain
- Questions marked for review
- Explanation of incorrect answers
- Recommended official documentation
- Suggested seven-day revision plan
- Recommendation on whether to attempt the mock test again

# Certification Alignment

## Recommended Certification
The recommended certification for learners completing this beginner-friendly bootcamp is:
Claude Certified Associate – Foundations
The workshop supports preparation across all seven certification domains.
Certification domain
Workshop alignment
Prompting and Task Execution
Structured briefs, constraints, acceptance criteria, Best-of-N, and iterative prompting
Output Evaluation and Validation
Tests, browser verification, evidence review, security findings, and Review Before Merge checklist
Product and Model Selection
Claude product surfaces, model selection, Claude Code, Cowork, Chrome, web, mobile, and Remote Control
Workflow Integration and Solution Design
Skills, hooks, subagents, plugins, Agent Teams, Git workflows, and stakeholder handoffs
Configuration and Knowledge Management
CLAUDE.md, scoped rules, auto memory, Skills, supporting files, and reusable project context
Governance, Risk, and Responsible Use
Permissions, sandboxing, secrets, privacy, safe delegation, security review, and human approval
Troubleshooting and Optimization
Testing, debugging, checkpoints, rewind, /goal, context management, and workflow improvement

## Certification Briefing
The final 25 minutes of the workshop will include:
- 10-minute certification briefing
- Overview of the four Anthropic certification paths
- Explanation of why Associate Foundations is the recommended starting point
- Walkthrough of the free mock test
- Exam preparation and registration guidance
- 15-minute final Q&A

## Important Disclaimer
This workshop and mock test are independently created by Packt.
They are not official Anthropic training, are not endorsed by Anthropic, and do not contain official examination questions. Claude and Anthropic certification names are used only to identify the certification for which the materials provide independent preparation.
Completion of the workshop or mock test does not guarantee success in the official certification examination.
