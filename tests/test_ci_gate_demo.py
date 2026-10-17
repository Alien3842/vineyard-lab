"""Disposable PR demonstration of required CI checks. Do not merge this branch."""


def test_intentional_failure_for_merge_gate_demo():
    assert False, "Intentional failure: verify required quality check blocks PR merging"
