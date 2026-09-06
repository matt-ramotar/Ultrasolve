#!/usr/bin/env python3
"""Run the repository's free unittest checks sequentially, without retries."""

import json
from pathlib import Path
import platform
import sys
import traceback
import unittest


REQUIRED_MODULES = (
    "test_plugin_contract.py",
    "test_portability_contract.py",
    "test_example_models.py",
    "test_contract_mutations.py",
    "test_evaluation_contract.py",
    "test_eval_bundle.py",
)


def main():
    if len(sys.argv) != 1:
        print("Usage: python3 tools/check.py (no arguments)", file=sys.stderr)
        return 2

    root = Path(__file__).resolve().parents[1]
    test_root = root / "tests"
    names = list(REQUIRED_MODULES)
    names.extend(sorted(path.name for path in test_root.glob("test_*.py")
                        if path.name not in REQUIRED_MODULES))
    print(f"Repository: {root}")
    print(f"Python: {platform.python_version()}")
    print("Checks: unittest discovery; sequential execution; no retries.")
    checks = []

    for name in names:
        record = {
            "module": "tests." + name[:-3],
            "status": "FAIL",
            "discovered": 0,
            "tests_run": 0,
            "failures": 0,
            "errors": 0,
            "skipped": 0,
            "expected_failures": 0,
            "unexpected_successes": 0,
        }
        checks.append(record)
        print(f"\nRUN {record['module']}", flush=True)
        try:
            if not (test_root / name).is_file():
                raise ValueError(f"Required test module is missing: tests/{name}")
            suite = unittest.TestLoader().discover(
                start_dir=str(test_root), pattern=name, top_level_dir=str(root)
            )
            record["discovered"] = suite.countTestCases()
            if not record["discovered"]:
                raise ValueError(f"No tests discovered in tests/{name}")
            result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
            record.update({
                "tests_run": result.testsRun,
                "failures": len(result.failures),
                "errors": len(result.errors),
                "skipped": len(result.skipped),
                "expected_failures": len(result.expectedFailures),
                "unexpected_successes": len(result.unexpectedSuccesses),
            })
            if (result.wasSuccessful() and not result.skipped and not result.expectedFailures
                    and result.testsRun == record["discovered"]):
                record["status"] = "PASS"
            elif result.skipped:
                record["reason"] = "Required checks were skipped."
            elif result.expectedFailures:
                record["reason"] = "Required checks have expected failures."
            elif result.testsRun != record["discovered"]:
                record["reason"] = "Executed count differs from discovered count."
        except (Exception, SystemExit) as error:
            record["reason"] = str(error)
            record["errors"] += 1
            traceback.print_exc(file=sys.stdout)
        print(f"{record['status']} {record['module']}: "
              f"{record['tests_run']}/{record['discovered']} tests executed, "
              f"{record['failures']} failures, {record['errors']} errors, "
              f"{record['skipped']} skipped, {record['expected_failures']} expected failures",
              flush=True)
        if "reason" in record:
            print(record["reason"], flush=True)

    passed = all(check["status"] == "PASS" for check in checks)
    summary = {
        "status": "PASS" if passed else "FAIL",
        "repository": str(root),
        "python_version": platform.python_version(),
        "checks": checks,
        "modules_checked": len(checks),
        "modules_passed": sum(check["status"] == "PASS" for check in checks),
        "tests_discovered": sum(check["discovered"] for check in checks),
        "tests_run": sum(check["tests_run"] for check in checks),
    }
    print(f"\n{summary['status']}: {summary['modules_passed']}/"
          f"{summary['modules_checked']} modules passed; "
          f"{summary['tests_run']} tests executed.")
    print("Not run: hosted CI, host behavior, model or judge evaluation.")
    print("CHECK_SUMMARY " + json.dumps(summary, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
