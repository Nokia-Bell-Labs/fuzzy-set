#!/usr/bin/env pytest
# flake F401 are dropped in this test file, see setup.cfg

def test_init():
    import fuzzy_set


def test_public_symbols():
    from fuzzy_set import (
        INFINITY, REALS,
        FuzzyNumber,
        FuzzySet,
        TrapezoidalFuzzyNumber,
        find_intersection,
    )
