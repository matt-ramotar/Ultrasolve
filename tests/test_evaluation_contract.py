"""Validate authored v2 evaluation assets. Never grade an agent's behavior."""

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "evals" / "portable" / "v2"
METHODS = ("simplify", "analogize", "restate", "generalize", "decompose", "invert")
CATEGORIES = {"invocation", "method", "outcome", "utility"}
RESOLUTIONS = {"VERIFIED", "CANDIDATE", "PARTIAL", "INFEASIBLE", "BLOCKED"}
CASE_FIELDS = {
    "id", "family", "evaluation_class", "setup", "turns", "supplied_facts",
    "invariants", "expected_route", "expected_definition_status",
    "allowed_resolution_statuses", "criteria", "forbidden_claims",
}


class TestEvaluationContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = json.loads((V2 / "cases.json").read_text())
        cls.cases = cls.corpus["cases"]
        cls.by_id = {case["id"]: case for case in cls.cases}
        cls.rubrics = (V2 / "rubrics.md").read_text()
        cls.calibration = json.loads((V2 / "grader-calibration.json").read_text())

    def test_exact_case_inventory_and_unique_ids(self):
        self.assertEqual(set(self.corpus), {"schema_version", "cases"})
        self.assertEqual(self.corpus["schema_version"], 2)
        expected = {f"A{i:02d}" for i in range(1, 21) if i not in (8, 9, 10, 20)}
        expected |= {f"A08-{state}-{method}" for state in ("confirmed", "open", "assumed") for method in METHODS}
        expected |= {f"A09-{kind}-{method}" for kind in ("undefined", "ideation") for method in METHODS}
        expected |= {f"A10-{kind}" for kind in ("result-only", "parameterization-only", "both-applicable")}
        expected |= {f"A20-{kind}" for kind in ("ordinary", "single-failure", "diagnosis")}
        expected |= {f"M{i:02d}" for i in range(1, 13)}
        self.assertEqual(len(self.cases), 64)
        self.assertEqual(len(self.by_id), 64)
        self.assertEqual(set(self.by_id), expected)

    def test_case_shape_and_status_domains(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(set(case), CASE_FIELDS)
                self.assertTrue(case["family"])
                self.assertIn(case["evaluation_class"], {"routing", "regression", "transfer", "integration"})
                self.assertIsInstance(case["setup"], dict)
                self.assertIn(case["expected_definition_status"], {None, "CONFIRMED", "DRAFT"})
                self.assertIsInstance(case["allowed_resolution_statuses"], list)
                self.assertEqual(len(case["allowed_resolution_statuses"]), len(set(case["allowed_resolution_statuses"])))
                self.assertLessEqual(set(case["allowed_resolution_statuses"]), RESOLUTIONS)
                if case["expected_definition_status"] is None:
                    self.assertEqual(case["allowed_resolution_statuses"], [])
                    self.assertIn(case["expected_route"]["entry"], {"direct", "brainstorming"})
                else:
                    self.assertTrue(case["allowed_resolution_statuses"])
                for field in ("turns", "supplied_facts", "invariants", "criteria", "forbidden_claims"):
                    self.assertIsInstance(case[field], list)
                    self.assertTrue(case[field], field)
                self.assertTrue(case["expected_route"]["entry"])

    def test_required_families_match_the_acceptance_inventory(self):
        families = {
            "A01": "definition-authority", "A02": "definition-authority",
            "A03": "reaffirmation", "A04": "proportional-definition",
            "A05": "deep-definition", "A06": "operational-sufficiency",
            "A07": "joint-inconclusive", "A08": "inherited-contract",
            "A09": "direct-leaf-boundary", "A10": "generalize-applicability",
            "A11": "constraint-interaction", "A12": "partial-composition",
            "A13": "evidence-status", "A14": "effort-exhaustion",
            "A15": "derived-infeasibility", "A16": "resource-integrity",
            "A17": "loader-capability", "A18": "denied-resource",
            "A19": "acceptance-provenance", "A20": "activation-boundary",
        }
        for case in self.cases:
            prefix = case["id"].split("-", 1)[0]
            if prefix.startswith("M"):
                method = METHODS[(int(prefix[1:]) - 1) // 2]
                self.assertEqual(case["family"], f"transfer-{method}")
            else:
                self.assertEqual(case["family"], families[prefix])

    def test_exact_turns_and_observation_releases(self):
        for case in self.cases:
            seen = set()
            for index, turn in enumerate(case["turns"]):
                with self.subTest(case=case["id"], turn=index):
                    self.assertNotIn(turn["id"], seen)
                    self.assertEqual(turn["message"]["role"], "user")
                    self.assertGreater(len(turn["message"]["content"].strip()), 40)
                    self.assertNotRegex(turn["message"]["content"], r"\{\{[^}]+\}\}|<INSERT|TODO|TBD")
                    release = turn["release"]
                    if index == 0:
                        self.assertEqual(release, {"event": "case_start"})
                    else:
                        self.assertEqual(release["event"], "assistant_turn_completed")
                        self.assertIn(release["after_turn"], seen)
                        self.assertTrue(release["observation"])
                        self.assertTrue(release["if_not_observed"])
                    seen.add(turn["id"])
        self.assertEqual(len(self.by_id["A03"]["turns"]), 2)
        self.assertGreaterEqual(len(self.by_id["A19"]["turns"]), 2)

    def test_invariant_sources_are_exact_and_covered_by_required_outcomes(self):
        global_ids = set()
        for case in self.cases:
            messages = {turn["id"]: turn["message"]["content"] for turn in case["turns"]}
            ids = {inv["id"] for inv in case["invariants"]}
            self.assertEqual(len(ids), len(case["invariants"]))
            self.assertFalse(global_ids & ids)
            global_ids |= ids
            for inv in case["invariants"]:
                self.assertTrue(inv["statement"])
                self.assertIn(inv["source_turn"], messages)
                self.assertIn(inv["source_quote"], messages[inv["source_turn"]])
                self.assertTrue(inv["source_quote"])
                matching = [c for c in case["criteria"] if c["category"] == "outcome" and c["required"] and inv["id"] in c["invariant_ids"]]
                self.assertTrue(matching, inv["id"])
            for fact in case["supplied_facts"]:
                self.assertIn(fact["source_turn"], messages)
                self.assertIn(fact["statement"], messages[fact["source_turn"]])

    def test_criterion_categories_ids_and_rubric_references(self):
        rubric_ids = set(re.findall(r"^## (R-[A-Z-]+)$", self.rubrics, re.M))
        rubric_categories = dict(re.findall(r"^## (R-[A-Z-]+)\n\nCategory: (\w+)\.", self.rubrics, re.M))
        self.assertTrue(rubric_ids)
        self.assertEqual(set(rubric_categories), rubric_ids)
        global_ids = set()
        for case in self.cases:
            invariant_ids = {inv["id"] for inv in case["invariants"]}
            categories = set()
            for criterion in case["criteria"]:
                self.assertEqual(set(criterion), {"id", "category", "invariant_ids", "rubric_id", "required", "assertion", "evidence_source"})
                self.assertNotIn(criterion["id"], global_ids)
                global_ids.add(criterion["id"])
                categories.add(criterion["category"])
                self.assertIn(criterion["category"], CATEGORIES)
                self.assertIn(criterion["rubric_id"], rubric_ids)
                self.assertEqual(rubric_categories[criterion["rubric_id"]], criterion["category"])
                self.assertLessEqual(set(criterion["invariant_ids"]), invariant_ids)
                if criterion["category"] == "outcome":
                    self.assertTrue(criterion["invariant_ids"])
                self.assertIs(type(criterion["required"]), bool)
                self.assertTrue(criterion["assertion"])
                self.assertIn(criterion["evidence_source"], {"answer", "trace", "answer_and_trace"})
            self.assertEqual(categories, CATEGORIES)
        for section in re.split(r"^## R-[A-Z-]+$", self.rubrics, flags=re.M)[1:]:
            for label in ("Category:", "Pass:", "Fail:", "Pass example:", "Fail example:"):
                self.assertIn(label, section)

    def test_expanded_contract_and_routing_families(self):
        for method in METHODS:
            for state in ("confirmed", "open", "assumed"):
                case = self.by_id[f"A08-{state}-{method}"]
                self.assertEqual(case["expected_route"]["entry"], method)
                self.assertEqual(case["expected_definition_status"], "CONFIRMED" if state == "confirmed" else "DRAFT")
                self.assertEqual(case["setup"]["effort"], {"full_attempts_consumed": 1, "full_attempts_remaining": 1})
            self.assertEqual(self.by_id[f"A09-undefined-{method}"]["expected_route"]["entry"], "define")
            self.assertEqual(self.by_id[f"A09-ideation-{method}"]["expected_route"]["entry"], "brainstorming")

    def test_conditional_technical_verification_status_pair_is_represented(self):
        covered = [case for case in self.cases if case["expected_definition_status"] == "DRAFT" and "VERIFIED" in case["allowed_resolution_statuses"]]
        self.assertTrue(covered)
        self.assertIn("A10-parameterization-only", {case["id"] for case in covered})
        case = self.by_id["A10-parameterization-only"]
        self.assertEqual(case["expected_route"]["entry"], "generalize")
        self.assertEqual(case["allowed_resolution_statuses"], ["VERIFIED"])
        self.assertTrue(any(criterion["required"] and criterion["category"] == "outcome" and criterion["rubric_id"] == "R-EVIDENCE-STATUS" for criterion in case["criteria"]))

    def test_transfer_inventory_and_documented_holdout_limits(self):
        transfer = [case for case in self.cases if case["evaluation_class"] == "transfer"]
        self.assertEqual(len(transfer), 12)
        self.assertEqual({case["id"] for case in transfer}, {f"M{i:02d}" for i in range(1, 13)})
        for case in transfer:
            self.assertEqual(case["setup"]["holdout_scope"], "held out from this plugin's shipped worked examples only")
            self.assertTrue(case["setup"]["changed_constraints"])
            self.assertTrue(case["setup"]["rejection_condition"])
            self.assertEqual(case["setup"]["invocation"]["mode"], "explicit")
        self.assertIn("not confidential", self.rubrics)
        self.assertIn("not guaranteed unseen", self.rubrics)

    def test_baseline_preserves_substantive_messages(self):
        for case in self.cases:
            setup = case["setup"]
            self.assertEqual(setup["baseline_rendering"], "Use turns[].message.content unchanged; omit only the explicit invocation prefix.")
            invocation = setup["invocation"]
            self.assertIn(invocation["mode"], {"automatic", "explicit", "none"})
            if invocation["mode"] == "explicit":
                skill = invocation["skill"]
                self.assertIn(skill, {"define", "solve", *METHODS})
                self.assertEqual(invocation["prefix_by_host"], {"codex": f"${skill}\n\n", "claude": f"/ultrasolve:{skill}\n\n"})
            else:
                self.assertEqual(invocation["prefix_by_host"], {})

    def test_integration_fixtures_describe_capabilities_without_runner_flags(self):
        integration = [case for case in self.cases if case["evaluation_class"] == "integration"]
        self.assertEqual({case["id"] for case in integration}, {"A16", "A17", "A18"})
        for case in integration:
            self.assertTrue(case["setup"]["required_capabilities"])
            self.assertIn("not_executed", case["setup"]["evidence_state"])
            self.assertNotRegex(json.dumps(case["setup"]), r"--[a-zA-Z][a-zA-Z-]+")

    def test_calibration_is_authored_not_a_semantic_score(self):
        self.assertEqual(self.calibration["schema_version"], 2)
        self.assertEqual(self.calibration["evidence_status"], "authored expectations; no judge or model run")
        examples = self.calibration["examples"]
        self.assertEqual(len(examples), 6)
        self.assertEqual(len({example["id"] for example in examples}), 6)
        expected_kinds = {"label-perfect-destructive-merge", "invented-benchmark", "correct-unlabeled-baseline", "wrong-automatic-activation", "valid-one-sided-generalize", "correct-conditional-draft"}
        self.assertEqual({example["kind"] for example in examples}, expected_kinds)
        for example in examples:
            case = self.by_id[example["case_id"]]
            self.assertTrue(example["response"])
            self.assertIsInstance(example["observed_trace"], list)
            self.assertEqual(example["provenance"], "authored synthetic answer and trace; not observed execution")
            self.assertEqual(set(example["expected_labels"]), {criterion["id"] for criterion in case["criteria"]})
            self.assertLessEqual(set(example["expected_labels"].values()), {"pass", "fail", "not_assessable"})
            self.assertTrue(example["rationale"])
            self.assertFalse({"score", "accuracy", "measured_pass_rate"} & set(example))


if __name__ == "__main__":
    unittest.main()
