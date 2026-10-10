# Claude Certified Associate – Foundations: Free Mock Test

This is the free full-length mock test that comes with **Claude Code Bootcamp: Cohort 2** (Packt, instructor Luca Berton). It helps you prepare for the **Claude Certified Associate – Foundations** certification offered by Anthropic.

> **Important disclaimer.** This workshop and mock test are independently created by Packt. They are not official Anthropic training, are not endorsed by Anthropic, and do not contain official examination questions. Claude and Anthropic certification names are used only to identify the certification for which the materials provide independent preparation. Completing the workshop or the mock test does not guarantee success in the official certification examination.

## Format

| Item | Detail |
|---|---|
| Questions | 60 original, scenario-based questions |
| Recommended time | 120 minutes. A countdown appears in each prompt, but nothing is cut off. |
| Question types | Single answer (43) and multiple response, "Select TWO" (17) |
| Coverage | All seven certification domains, weighted as shown below |
| Feedback | An explanation for every option, right or wrong, plus 1–2 official documentation links per question |
| Report | Certification Readiness Report, printed and saved to `mock-test/results/<timestamp>.md` |
| Attempts | Unlimited for workshop attendees. Use `--shuffle` to vary option order. |

## Domain distribution

| Domain | Weight | Questions | Workshop alignment |
|---|---|---|---|
| Prompting and Task Execution | 14% | 8 | Structured briefs, constraints, acceptance criteria, Best-of-N, iterative prompting |
| Output Evaluation and Validation | 21% | 13 | Tests, browser verification, evidence review, security findings, Review Before Merge checklist |
| Product and Model Selection | 12% | 7 | Claude product surfaces, model selection, Claude Code, Cowork, Chrome, web, mobile, Remote Control |
| Workflow Integration and Solution Design | 16% | 10 | Skills, hooks, subagents, plugins, Agent Teams, Git workflows, stakeholder handoffs |
| Configuration and Knowledge Management | 12% | 7 | CLAUDE.md, scoped rules, auto memory, Skills, supporting files, reusable project context |
| Governance, Risk, and Responsible Use | 15% | 9 | Permissions, sandboxing, secrets, privacy, safe delegation, security review, human approval |
| Troubleshooting and Optimization | 10% | 6 | Testing, debugging, checkpoints, rewind, `/goal`, context management, workflow improvement |
| **Total** | **100%** | **60** | |

Questions are interleaved across domains, as in a real exam. About a quarter are `foundation` level (recognise the right concept) and the rest are `applied` (choose the best action in a realistic situation).

## How to run

You need Python 3.9 or later. The test uses only the standard library and runs on macOS, Linux and WSL. Run these commands from the repository root:

```bash
python3 mock-test/run.py                      # full 60-question attempt, 120-minute countdown
python3 mock-test/run.py --shuffle            # shuffle the answer options of every question
python3 mock-test/run.py --shuffle --seed 42  # reproducible shuffle
python3 mock-test/run.py --domain "Governance, Risk, and Responsible Use"   # practise one domain
python3 mock-test/run.py --domain trouble     # a unique part of the domain name also works
python3 mock-test/run.py --time 90            # change the recommended time limit (minutes)
python3 mock-test/run.py --review             # print every question with answers and explanations
python3 mock-test/run.py --list-domains       # show domains and question counts
python3 mock-test/run.py --answers my-answers.json   # grade a submission non-interactively
```

Other options: `--results-dir DIR` writes the report somewhere else, and `--no-save` prints the report without writing a file.

### During an interactive attempt

| Input | Effect |
|---|---|
| `B` | Answer a single-answer question |
| `A C` or `A,C` or `AC` | Answer a "Select TWO" question. You must give exactly the number of letters asked for. |
| `m` | Mark or unmark the current question for review (`B m` answers and marks in one go) |
| `s` | Skip. The question counts as unanswered. |
| `q` | Finish early. The remaining questions count as unanswered and the report is generated. |

### Answers file format (non-interactive mode)

```json
{
  "Q01": ["C"],
  "Q02": "B",
  "Q08": ["A", "C"],
  "marked": ["Q05", "Q17"]
}
```

Letters always refer to the original order in `questions.json`. Any question you leave out counts as unanswered. The `marked` list is optional. There's a worked example in `tests/fixtures/sample_answers.json`.

## Scoring

- Each question is worth 1 point.
- **Multiple-response questions score 1 only when your selection is exactly right.** There is no partial credit.
- Unanswered questions score 0.
- Readiness levels, as defined in the workshop brief:

| Score | Readiness level |
|---|---|
| 80% or higher | Strong exam readiness |
| 70% to 79% | Nearly ready, with focused revision recommended |
| 60% to 69% | Additional study required |
| Below 60% | Revisit the learning path before scheduling the official exam |

The official examination uses scaled scoring, which an independent mock test can't reproduce precisely. Your mock test score doesn't guarantee success in the official examination.

## Certification Readiness Report

At the end of every attempt, the report is printed and saved to `mock-test/results/<YYYYMMDD-HHMMSS>.md`. It contains:

1. Overall score and readiness level
2. Score by certification domain, with the exam weight of each
3. Strongest domain and weakest domain
4. Questions you marked for review
5. An explanation of each incorrect answer: your choice, the correct choice, why each is right or wrong, and documentation links
6. Recommended official documentation, ranked by how many missed questions point to it
7. A suggested seven-day revision plan. Days 1–5 focus on your weakest domains, weighted by score gap × exam weight. Day 6 is mixed review and day 7 is a timed retake.
8. A recommendation on whether to attempt the mock test again
9. The disclaimer

## Scenario coverage

The scenarios follow the themes listed in the workshop brief:

| Brief theme | Example questions |
|---|---|
| Improving an incomplete or ambiguous prompt | Q04, Q27, Q34, Q57 |
| Detecting an unsupported claim in Claude's output | Q01, Q29, Q41 |
| Choosing between Chat, Projects, Claude Code, Cowork, Artifacts and Research | Q05, Q13, Q22, Q47, Q55 |
| Selecting a model by quality, speed and cost | Q30, Q38 |
| Deciding when human review is required | Q24, Q51, Q53 |
| Protecting confidential or regulated information | Q03, Q18, Q58 |
| Designing a workflow with approval checkpoints | Q33, Q45, Q11 |
| Creating reusable project instructions | Q06, Q23, Q48 |
| Managing outdated knowledge and context | Q31, Q56 |
| Troubleshooting poor or inconsistent outputs | Q07, Q27, Q46 |
| Communicating capabilities and limitations to stakeholders | Q40, Q43 |
| Deciding whether a task should be automated | Q52, Q45 |

## Files

```
mock-test/
├── README.md                     this file
├── questions.json                the 60-question bank (id, domain, type, scenario, question,
│                                 options A–E, answer, explanations for every option,
│                                 doc_links, difficulty)
├── run.py                        interactive quiz, review mode and non-interactive grader
├── results/                      readiness reports (created on first run)
└── tests/
    ├── test_run.py               schema, scoring and report tests
    └── fixtures/sample_answers.json
```

Run the tests from the repository root:

```bash
python3 -m unittest discover -s mock-test/tests -v
```

The tests check that there are exactly 60 questions, that the domain counts are exact, that IDs are unique, that every option is explained, that each explanation agrees with the answer key, that answers are a subset of the options, that single-answer questions have exactly one answer and multiple-response questions have at least two, that doc links come from official domains, and that answer positions are balanced. They also cover scoring (exact-match rule and thresholds), report content, the revision plan, the interactive flow (marking, skipping, shuffle letter mapping) and non-interactive grading.

## Accuracy and maintenance

- Product details were checked against the official documentation on **10 October 2026**: the [Claude Code docs](https://code.claude.com/docs), the [Claude Developer Platform docs](https://platform.claude.com/docs) (models overview, choosing a model, prompting best practices, hallucination and consistency guides), [Claude Help Center](https://support.claude.com) articles on Projects, Artifacts, Research and Cowork, and the [Cowork overview](https://claude.com/docs/cowork/overview).
- Claude products change quickly. Where a fact depends on plan tier or version, the questions are written so the right answer rests on stable principles, such as evidence over claims, least privilege and matching autonomy to consequence, rather than on a detail that may change.
- If you edit `questions.json`, keep the explanations' `Correct.` and `Incorrect.` prefixes and rerun the tests. Explanations never refer to other options by letter, so `--shuffle` stays correct.
- These questions are original Packt material written for this workshop. They aren't taken from, and aren't intended to reproduce, any official examination content.
