"""Timing argument for the illustrative cache example, not a deployed cache test."""

from __future__ import annotations

import unittest
from typing import Optional


def freshness_deadline(
    coverage_at: Optional[float],
    received_at: float,
    budget: float,
    clock_error: Optional[float],
) -> Optional[float]:
    """Coverage is source time; absolute consumer/source clock error is bounded.

    Receipt permits using the watermark, but does not renew its coverage age.
    Subtracting the error makes expiry conservative even when the consumer lags.
    """
    if coverage_at is None or clock_error is None:
        return None
    if budget <= 0 or clock_error < 0:
        raise ValueError("budget must be positive and clock error nonnegative")
    return coverage_at + budget - clock_error


def cache_allowed(
    coverage_at: Optional[float],
    received_at: float,
    now: float,
    budget: float = 5.0,
    clock_error: Optional[float] = 0.0,
) -> bool:
    deadline = freshness_deadline(coverage_at, received_at, budget, clock_error)
    return deadline is not None and received_at <= now < deadline


class TestFreshnessCoverageModel(unittest.TestCase):
    def test_delayed_prewrite_watermark_cannot_extend_the_source_budget(self) -> None:
        write_at = 0.1
        deadline = freshness_deadline(0.0, 1.9, 5.0, 0.0)
        self.assertEqual(5.0, deadline)
        self.assertLessEqual(deadline, write_at + 5.0)
        self.assertTrue(cache_allowed(0.0, 1.9, 4.9))
        self.assertFalse(cache_allowed(0.0, 1.9, 5.2))

    def test_expired_replay_cannot_reenable_cached_reads(self) -> None:
        self.assertFalse(cache_allowed(0.0, 6.0, 6.0))
        self.assertFalse(cache_allowed(0.0, 6.0, 6.1))

    def test_clock_error_is_subtracted_conservatively(self) -> None:
        self.assertEqual(4.75, freshness_deadline(0.0, 1.9, 5.0, 0.25))
        self.assertFalse(cache_allowed(0.0, 1.9, 4.8, clock_error=0.25))
        # A consumer lagging source time by the full error cannot serve at source 5.0.
        self.assertFalse(cache_allowed(0.0, 1.9, 5.0 - 0.25, clock_error=0.25))

    def test_arrival_does_not_change_the_coverage_deadline(self) -> None:
        deadlines = [freshness_deadline(0.0, arrival, 5.0, 0.0) for arrival in (0.0, 1.9, 6.0)]
        self.assertEqual([5.0, 5.0, 5.0], deadlines)

    def test_unknown_clock_bound_or_coverage_cannot_claim_freshness(self) -> None:
        self.assertIsNone(freshness_deadline(0.0, 1.9, 5.0, None))
        self.assertIsNone(freshness_deadline(None, 1.9, 5.0, 0.0))
        self.assertFalse(cache_allowed(0.0, 1.9, 2.0, clock_error=None))
        self.assertFalse(cache_allowed(None, 1.9, 2.0))

    def test_no_cached_read_before_the_watermark_arrives(self) -> None:
        self.assertFalse(cache_allowed(0.0, 1.9, 1.8))

    def test_new_source_coverage_can_advance_the_deadline(self) -> None:
        self.assertEqual(9.9, freshness_deadline(5.0, 6.0, 5.0, 0.1))
        self.assertTrue(cache_allowed(5.0, 6.0, 6.1, clock_error=0.1))

    def test_invalid_assumptions_are_rejected(self) -> None:
        for budget, error in ((0.0, 0.0), (-1.0, 0.0), (5.0, -0.1)):
            with self.subTest(budget=budget, error=error), self.assertRaises(ValueError):
                freshness_deadline(0.0, 1.9, budget, error)


if __name__ == "__main__":
    unittest.main()
