# Assessment and Certification

Claude Code Bootcamp: Cohort 2 (Packt). Instructor: Luca Berton.

Passing this assessment earns the **Packt Certificate of Completion**. The assessment checks whether you can carry out the workshop's way of working: delegate with constraints, verify with real evidence, and make a defensible release decision. Recalling commands is not enough to pass.

## Structure

| Component | Evidence | Weight | Points | Files |
|---|---|---|---|---|
| Scenario-based knowledge quiz | Permissions, feature selection, context, security, and workflow decisions | 30% | 30 | [`quiz.md`](quiz.md) (25 questions, 1.2 points each) |
| Practical capstone | Working change, tests, diff, verification, and readiness report | 50% | 50 | [`capstone.md`](capstone.md), scored with [`rubric.md`](rubric.md) |
| Engineering reflection | Rejected approach, human checkpoint, and unresolved risk | 20% | 20 | [`reflection-template.md`](reflection-template.md), scored with [`rubric.md`](rubric.md) |
| **Total** | | **100%** | **100** | |

Instructors also use [`quiz-answer-key.md`](quiz-answer-key.md) (do not distribute it) and [`grading-sheet.csv`](grading-sheet.csv).

## Passing criteria

Learners must:
- Score 70% or higher overall
- Score at least 60% on the practical capstone
- Submit genuine test or runtime evidence
- Include a risk summary, top three fixes, named owner, and verification step
- Avoid automatic-fail conditions such as exposed credentials, fabricated test results, or unsafe irreversible actions

In points: an overall score of at least **70/100** and a capstone score of at least **30/50**. The Production Readiness Report must contain the risk summary, top three fixes, named owner, and verification step. You must meet every criterion; a high score on one component cannot make up for a missed gate.

## Automatic-fail conditions

Any of the following fails the assessment, whatever the score:

| Condition | Examples |
|---|---|
| **Exposed credentials** | A real API key, token, password, or private key committed to the repository, included in the diff, visible in a screenshot or log, or pasted into the submission |
| **Fabricated test results** | Test or runtime output that was not actually produced by the submitted code: edited output, output copied from another run or another learner, or "tests pass" with no reproducible command |
| **Unsafe irreversible actions** | A force-push or history rewrite on a shared branch; deleting data outside the project; running `bypassPermissions` on your host machine rather than in a container or VM; disabling hooks or deny rules to get past a block; deploying, or sending external messages, without approval |

Honest failure is **not** an automatic fail. A submission that reports a failing test truthfully, explains it, and says what remains to be done is graded on its merits. A submission that hides a failure is graded as fabricated.

## Submission checklist

Submit one archive or repository link that contains:

- [ ] Quiz answers, if the quiz is not taken on the online form
- [ ] `capstone/brief.md`: your engineering brief (from [`../templates/engineering-brief.md`](../templates/engineering-brief.md))
- [ ] `capstone/permission-boundary.md`: the boundary you worked under
- [ ] The feature branch with focused commits, and `capstone/capstone.diff`
- [ ] `capstone/evidence/tests.txt`: the test command, raw output, and exit code
- [ ] `capstone/evidence/runtime/`: a `curl` transcript, or browser screenshots and an issue log
- [ ] `capstone/review-before-merge.md`: all seven points, each with evidence
- [ ] `capstone/production-readiness-report.md`: all seven required sections
- [ ] `capstone/reflection.md`: from [`reflection-template.md`](reflection-template.md)
- [ ] A final check that no `.env`, tokens, or personal data appear anywhere, including git history and screenshots

## Timeline

| When | What |
|---|---|
| Workshop, final segment | Exam briefing: format, passing criteria, and capstone options. Questions answered |
| Day 0 to Day 7 | Quiz window. Allow 40 minutes, individual work, workshop materials and docs allowed. One attempt |
| Day 0 to Day 7 | Capstone and reflection. Expected effort is 2 to 3 hours. Submit by 23:59 ET on Day 7 |
| Day 8 to Day 17 | Grading. Graders rerun the submitted tests. Automatic-fail findings are confirmed by a second grader |
| By Day 17 | Results and feedback released. Certificates issued to learners who passed |
| Day 18 to Day 24 | One resubmission is allowed for a capstone below 30/50 or a missing readiness element. This does not apply to automatic fails |

The instructor may adjust dates. The cohort announcement is authoritative.

## Academic integrity

You may use Claude Code for all of the capstone; that is the point of the exercise. You may not submit evidence that your code did not produce, or another learner's work. You are the engineer of record for everything you submit.
