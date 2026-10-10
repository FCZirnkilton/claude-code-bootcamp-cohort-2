"""Tests for the Packt mock test: question bank schema, scoring and report generation.

Run from the repository root:
    python3 -m unittest discover -s mock-test/tests -v
"""

import json
import os
import random
import re
import sys
import tempfile
import unittest
from collections import Counter
from urllib.parse import urlparse

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
MOCK_DIR = os.path.dirname(TESTS_DIR)
sys.path.insert(0, MOCK_DIR)

import run  # noqa: E402

BANK_PATH = os.path.join(MOCK_DIR, "questions.json")
FIXTURE = os.path.join(TESTS_DIR, "fixtures", "sample_answers.json")

EXPECTED_DOMAINS = {
    "Prompting and Task Execution": 8,
    "Output Evaluation and Validation": 13,
    "Product and Model Selection": 7,
    "Workflow Integration and Solution Design": 10,
    "Configuration and Knowledge Management": 7,
    "Governance, Risk, and Responsible Use": 9,
    "Troubleshooting and Optimization": 6,
}
ALLOWED_HOSTS = {
    "code.claude.com", "platform.claude.com", "support.claude.com", "claude.com", "www.anthropic.com",
}
LETTERS = ["A", "B", "C", "D", "E"]


def load_questions():
    return run.load_bank(BANK_PATH)["questions"]


class QuestionBankSchemaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions = load_questions()

    def test_exactly_60_questions(self):
        self.assertEqual(len(self.questions), 60)

    def test_ids_unique_and_sequential(self):
        ids = [q["id"] for q in self.questions]
        self.assertEqual(len(ids), len(set(ids)), "duplicate ids")
        self.assertEqual(ids, ["Q%02d" % i for i in range(1, 61)])

    def test_exact_domain_counts(self):
        counts = Counter(q["domain"] for q in self.questions)
        self.assertEqual(dict(counts), EXPECTED_DOMAINS)

    def test_domain_counts_match_runner_weights(self):
        self.assertEqual(set(run.DOMAIN_WEIGHTS), set(EXPECTED_DOMAINS))
        self.assertEqual(sum(run.DOMAIN_WEIGHTS.values()), 100)

    def test_required_fields_and_types(self):
        required = {"id", "domain", "type", "scenario", "question", "options", "answer",
                    "explanations", "doc_links", "difficulty"}
        for q in self.questions:
            with self.subTest(q=q["id"]):
                self.assertTrue(required.issubset(q), "missing: %s" % (required - set(q)))
                self.assertIn(q["type"], ("single", "multiple"))
                self.assertIn(q["difficulty"], ("foundation", "applied"))
                for field in ("scenario", "question"):
                    self.assertIsInstance(q[field], str)
                self.assertGreater(len(q["scenario"].strip()), 100, "scenario too short")
                self.assertGreater(len(q["question"].strip()), 10, "question too short")
                self.assertTrue(q["question"].strip().endswith(("?", ")")), "question should be a question")

    def test_options_are_a_to_e(self):
        for q in self.questions:
            with self.subTest(q=q["id"]):
                self.assertEqual(sorted(q["options"]), LETTERS)
                texts = [t.strip().lower() for t in q["options"].values()]
                self.assertEqual(len(texts), len(set(texts)), "duplicate option text")
                for t in texts:
                    self.assertTrue(t)
                    self.assertNotIn("all of the above", t)
                    self.assertNotIn("none of the above", t)

    def test_every_option_explained(self):
        for q in self.questions:
            with self.subTest(q=q["id"]):
                self.assertEqual(sorted(q["explanations"]), LETTERS)
                for letter, text in q["explanations"].items():
                    self.assertGreater(len(text.strip()), 20, "thin explanation for %s" % letter)

    def test_explanations_agree_with_answer_key(self):
        for q in self.questions:
            with self.subTest(q=q["id"]):
                for letter, text in q["explanations"].items():
                    if letter in q["answer"]:
                        self.assertTrue(text.startswith("Correct."), letter)
                    else:
                        self.assertTrue(text.startswith("Incorrect."), letter)

    def test_answers_subset_of_options(self):
        for q in self.questions:
            with self.subTest(q=q["id"]):
                self.assertIsInstance(q["answer"], list)
                self.assertTrue(set(q["answer"]).issubset(q["options"]))
                self.assertEqual(len(q["answer"]), len(set(q["answer"])))

    def test_single_has_one_answer_multiple_has_at_least_two(self):
        for q in self.questions:
            with self.subTest(q=q["id"]):
                if q["type"] == "single":
                    self.assertEqual(len(q["answer"]), 1)
                else:
                    self.assertGreaterEqual(len(q["answer"]), 2)
                    self.assertLess(len(q["answer"]), 5)

    def test_multiple_response_questions_state_how_many(self):
        words = {2: "TWO", 3: "THREE"}
        for q in self.questions:
            if q["type"] == "multiple":
                with self.subTest(q=q["id"]):
                    self.assertIn("Select %s" % words[len(q["answer"])], q["question"])

    def test_mix_of_question_types(self):
        types = Counter(q["type"] for q in self.questions)
        self.assertGreaterEqual(types["multiple"], 10)
        self.assertGreaterEqual(types["single"], 30)

    def test_doc_links(self):
        for q in self.questions:
            with self.subTest(q=q["id"]):
                self.assertTrue(1 <= len(q["doc_links"]) <= 2)
                for link in q["doc_links"]:
                    parsed = urlparse(link)
                    self.assertEqual(parsed.scheme, "https")
                    self.assertIn(parsed.netloc, ALLOWED_HOSTS)

    def test_answer_positions_are_balanced(self):
        singles = Counter(q["answer"][0] for q in self.questions if q["type"] == "single")
        for letter in LETTERS:
            self.assertGreaterEqual(singles[letter], 5, "answer key skewed away from %s" % letter)


class ScoringTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions = load_questions()
        cls.responses, cls.marked = run.load_answers_file(FIXTURE)

    def test_parse_letters(self):
        self.assertEqual(run.parse_letters("b"), ["B"])
        self.assertEqual(run.parse_letters("c, a"), ["A", "C"])
        self.assertEqual(run.parse_letters(["E", "a", "E"]), ["A", "E"])
        self.assertEqual(run.parse_letters(None), [])

    def test_multiple_response_requires_exact_match(self):
        q = next(q for q in self.questions if q["type"] == "multiple")
        self.assertTrue(run.is_correct(q, list(q["answer"])))
        self.assertFalse(run.is_correct(q, q["answer"][:1]))
        wrong_extra = sorted(set(q["answer"]) | {next(l for l in LETTERS if l not in q["answer"])})
        self.assertFalse(run.is_correct(q, wrong_extra))
        self.assertFalse(run.is_correct(q, []))

    def test_readiness_thresholds(self):
        self.assertEqual(run.readiness_level(100), "Strong exam readiness")
        self.assertEqual(run.readiness_level(80), "Strong exam readiness")
        self.assertEqual(run.readiness_level(79.9), "Nearly ready, with focused revision recommended")
        self.assertEqual(run.readiness_level(70), "Nearly ready, with focused revision recommended")
        self.assertEqual(run.readiness_level(69.9), "Additional study required")
        self.assertEqual(run.readiness_level(60), "Additional study required")
        self.assertEqual(run.readiness_level(59.9),
                         "Revisit the learning path before scheduling the official exam")
        self.assertEqual(run.readiness_level(0),
                         "Revisit the learning path before scheduling the official exam")

    def test_fixture_score(self):
        result = run.grade(self.questions, self.responses, self.marked)
        # Fixture: Q01-Q42 correct; Q43-Q55 wrong or partially correct; Q56-Q60 unanswered.
        self.assertEqual(result["total"], 60)
        self.assertEqual(result["correct"], 42)
        self.assertEqual(result["percent"], 70.0)
        self.assertEqual(result["level"], "Nearly ready, with focused revision recommended")
        self.assertEqual(sum(d["total"] for d in result["by_domain"].values()), 60)
        self.assertEqual(sum(d["correct"] for d in result["by_domain"].values()), 42)
        unanswered = [i["question"]["id"] for i in result["items"] if not i["answered"]]
        self.assertEqual(unanswered, ["Q56", "Q57", "Q58", "Q59", "Q60"])
        self.assertEqual(sorted(i["question"]["id"] for i in result["items"] if i["marked"]),
                         ["Q03", "Q45"])

    def test_perfect_and_zero_scores(self):
        perfect = {q["id"]: q["answer"] for q in self.questions}
        result = run.grade(self.questions, perfect)
        self.assertEqual(result["percent"], 100.0)
        self.assertEqual(result["level"], "Strong exam readiness")
        result = run.grade(self.questions, {})
        self.assertEqual(result["correct"], 0)

    def test_domain_filter_and_resolution(self):
        name = run.resolve_domain("troubleshooting", self.questions)
        self.assertEqual(name, "Troubleshooting and Optimization")
        self.assertEqual(len(run.filter_questions(self.questions, name)), 6)
        with self.assertRaises(ValueError):
            run.resolve_domain("and", self.questions)  # ambiguous

    def test_revision_plan_weighted_to_weakest(self):
        result = run.grade(self.questions, self.responses, self.marked)
        days = run.allocate_days(result["by_domain"], days=5)
        self.assertEqual(len(days), 5)
        strongest, weakest = run.strongest_weakest(result["by_domain"])
        for name in weakest:
            self.assertIn(name, days, "weakest domain missing from plan")
        self.assertIn(days[0], weakest, "plan should start with a weakest domain")
        self.assertNotIn(strongest[0], days)

    def test_revision_plan_concentrates_on_single_weak_domain(self):
        responses = {q["id"]: q["answer"] for q in self.questions
                     if q["domain"] != "Output Evaluation and Validation"}
        result = run.grade(self.questions, responses)
        days = run.allocate_days(result["by_domain"], days=5)
        self.assertEqual(days, ["Output Evaluation and Validation"] * 5)

    def test_domain_table_uses_canonical_order(self):
        result = run.grade(self.questions, self.responses)
        self.assertEqual(list(result["by_domain"]), list(run.DOMAIN_WEIGHTS))


class ReportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions = load_questions()
        responses, marked = run.load_answers_file(FIXTURE)
        cls.result = run.grade(cls.questions, responses, marked)
        cls.report = run.build_report(cls.result, {"mode": "test", "timestamp": "2026-10-10 10:00:00"})

    def test_report_sections(self):
        for heading in [
            "# Certification Readiness Report",
            "## Overall score",
            "## Score by certification domain",
            "## Questions marked for review",
            "## Explanation of incorrect answers",
            "## Recommended official documentation",
            "## Suggested seven-day revision plan",
            "## Should you attempt the mock test again?",
        ]:
            self.assertIn(heading, self.report)

    def test_report_content(self):
        r = self.report
        self.assertIn("42 / 60 correct (70.0%)", r)
        self.assertIn("Nearly ready, with focused revision recommended", r)
        self.assertIn("**Strongest domain:**", r)
        self.assertIn("**Weakest domain:**", r)
        self.assertIn("- Q03 (", r)
        self.assertIn("- Q45 (", r)
        for day in range(1, 8):
            self.assertIn("**Day %d:" % day, r)
        for name in run.DOMAIN_WEIGHTS:
            self.assertIn("| %s |" % name, r)
        self.assertIn("scaled scoring", r)

    def test_report_explains_every_incorrect_answer(self):
        for item in self.result["items"]:
            qid = item["question"]["id"]
            if item["correct"]:
                self.assertNotIn("### %s:" % qid, self.report)
            else:
                self.assertIn("### %s:" % qid, self.report)

    def test_report_recommends_docs_from_missed_questions(self):
        missed_links = {l for i in self.result["items"] if not i["correct"]
                        for l in i["question"]["doc_links"]}
        section = self.report.split("## Recommended official documentation")[1].split("## ")[0]
        for link in missed_links:
            self.assertIn(link, section)

    def test_disclaimer_present(self):
        self.assertIn("independently created by Packt", self.report)
        self.assertIn("not endorsed by Anthropic", self.report)
        self.assertIn("do not contain official examination questions", self.report)
        self.assertIn("does not guarantee success", self.report)

    def test_perfect_score_report(self):
        perfect = {q["id"]: q["answer"] for q in self.questions}
        report = run.build_report(run.grade(self.questions, perfect), {"mode": "test"})
        self.assertIn("No incorrect answers", report)
        self.assertIn("Strong exam readiness", report)


class CommandLineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.devnull = open(os.devnull, "w")
        self.addCleanup(self.devnull.close)
        self._stdout = sys.stdout
        sys.stdout = self.devnull
        self.addCleanup(setattr, sys, "stdout", self._stdout)

    def test_non_interactive_grading_writes_report(self):
        code = run.main(["--answers", FIXTURE, "--results-dir", self.tmp.name])
        self.assertEqual(code, 0)
        files = os.listdir(self.tmp.name)
        self.assertEqual(len(files), 1)
        self.assertRegex(files[0], r"^\d{8}-\d{6}(-\d+)?\.md$")
        with open(os.path.join(self.tmp.name, files[0]), encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn("42 / 60 correct (70.0%)", text)
        self.assertIn("independently created by Packt", text)

    def test_domain_grading(self):
        code = run.main(["--answers", FIXTURE, "--domain", "Governance, Risk, and Responsible Use",
                         "--results-dir", self.tmp.name])
        self.assertEqual(code, 0)
        path = os.path.join(self.tmp.name, os.listdir(self.tmp.name)[0])
        with open(path, encoding="utf-8") as fh:
            self.assertIn("Domain practice: Governance, Risk, and Responsible Use", fh.read())

    def test_unknown_domain_returns_error(self):
        stderr = sys.stderr
        sys.stderr = self.devnull
        try:
            self.assertEqual(run.main(["--domain", "Astrology", "--no-save"]), 2)
        finally:
            sys.stderr = stderr

    def test_review_mode(self):
        self.assertEqual(run.main(["--review", "--domain", "Product and Model Selection"]), 0)

    def test_interactive_with_marking_and_skips(self):
        questions = run.filter_questions(load_questions(), "Troubleshooting and Optimization")
        script = ["m"]  # mark the first question, then answer it
        for i, q in enumerate(questions):
            if i == 1:
                script.append("s")  # skip
            elif i == 2:
                script.extend(["Z", "A B C", "".join(q["answer"])])  # invalid, wrong count, valid
            else:
                script.append(" ".join(q["answer"]))
        feed = iter(script)
        code = run.main(["--domain", "Troubleshooting", "--results-dir", self.tmp.name],
                        input_fn=lambda prompt: next(feed))
        self.assertEqual(code, 0)
        path = os.path.join(self.tmp.name, os.listdir(self.tmp.name)[0])
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn("5 / 6 correct", text)
        self.assertIn("- %s (" % questions[0]["id"], text)  # marked
        self.assertIn("### %s:" % questions[1]["id"], text)  # skipped counts as incorrect
        self.assertIn("(no answer)", text)

    def test_interactive_shuffle_maps_letters_back(self):
        questions = run.filter_questions(load_questions(), "Product and Model Selection")
        seed = 7
        rng = random.Random(seed)
        script = []
        for q in questions:
            order = LETTERS[:]
            rng.shuffle(order)
            shown = [LETTERS[order.index(c)] for c in q["answer"]]
            script.append(",".join(shown))
        feed = iter(script)
        responses, marked, orders, _ = run.run_interactive(
            questions, 120, shuffle=True, seed=seed, input_fn=lambda prompt: next(feed))
        result = run.grade(questions, responses, marked, orders)
        self.assertEqual(result["correct"], len(questions))
        self.assertTrue(any(o != LETTERS for o in orders.values()))

    def test_quit_early_grades_remaining_as_unanswered(self):
        questions = load_questions()
        feed = iter(["".join(questions[0]["answer"]), "q"])
        responses, marked, orders, _ = run.run_interactive(
            questions, 120, shuffle=False, input_fn=lambda prompt: next(feed))
        result = run.grade(questions, responses, marked, orders)
        self.assertEqual(result["correct"], 1)
        self.assertEqual(result["total"], 60)


if __name__ == "__main__":
    unittest.main()
