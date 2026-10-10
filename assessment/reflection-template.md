# Engineering Reflection

> **How to use.** Write this after you finish the capstone, while the decisions are fresh. Save it as `capstone/reflection.md`. It is worth 20 points. Answer each section in 150 to 300 words, and point to concrete evidence: a commit hash, a file, a transcript excerpt, or a checklist row. Graders reward specific, honest reasoning, and that includes admitting what went wrong. They do not reward polished prose or claims without evidence.

---

**Learner:** `__________`  **Capstone option:** `__________`  **Branch / final commit:** `__________`

## 1. Rejected approach (7 points)

Describe one approach you, or Claude, considered and rejected. This can be a design, a fix, a test strategy, or a tool choice.

- What was the approach? Who proposed it?
- What would it have done well?
- What was the primary reason you rejected it? What evidence or criterion decided it?
- Under what conditions would it become the right choice later?
- Did you try it before rejecting it? If so, how did you get back to a known-good state (`/rewind`, git, or a branch)?

`__________`

## 2. Human checkpoint (7 points)

Describe the most important moment where you, as the engineer of record, stopped Claude, redirected it, or made a decision it could not make for you.

- What was the situation, and what was Claude about to do or claiming?
- What did you check, and what did you find? Cite the evidence.
- What did you decide, and why?
- What would have happened without the checkpoint?
- Would you move this checkpoint earlier or later next time, or enforce it with a permission rule or hook? Why?

`__________`

## 3. Unresolved risk (6 points)

Describe one risk that remains after your change. Every real change has at least one; "none" scores zero.

- What is the risk, and how likely and how severe is it?
- What evidence shows it exists, or why can't it be verified yet?
- Why did you not fix it in this change? Think about scope, time, or a decision that belongs to someone else.
- Who should own it, and what verification action would show it has been addressed?
- Does it appear in your Production Readiness Report? Where?

`__________`

## 4. Optional: one thing you would change in your workflow

One or two sentences. This section is not scored, but the instructor reads it.

`__________`
