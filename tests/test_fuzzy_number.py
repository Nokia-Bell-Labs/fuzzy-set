from fuzzy_set import FuzzyNumber
from pprint import pformat


pts_convex = dict(
    enumerate([0, 0.6, 0.8, 1, 1, 0.9, 0.75, 0.4, 0])
)


def test_fuzzy_number_convex():
    # Points are unaligned, and the fuzzy number is convex
    a = FuzzyNumber(pts_convex)
    assert a.x1 <= a.x2 <= a.x3 <= a.x4


def test_fuzzy_number_is_normalized():
    a = FuzzyNumber(pts_convex)
    assert a.is_normalized()


def test_fuzzy_number_convex_corner_case():
    # Some points are aligned, but the fuzzy number
    # is still convex.
    pts_convex2 = dict(
        enumerate([0, 0.5, 0.75, 1, 1, 0.7, 0.4, 0])
    )
    _ = FuzzyNumber(pts_convex2)


def test_fuzzy_number_non_convex():
    pts_non_convex = dict(
        enumerate([0, 0.5, 0.7, 1, 1, 0.5, 0.4, 0])
    )
    try:
        _ = FuzzyNumber(pts_non_convex)
        assert "Implementation error", pts_non_convex
    except ValueError:
        pass


def test_fuzzy_number_non_normalized():
    pts_non_normalized = dict(
        enumerate([0, 0.1, 0.7, 0.1, 0])
    )
    try:
        _ = FuzzyNumber(pts_non_normalized)
        assert "Implementation error", pts_non_normalized
    except ValueError:
        pass


def test_fuzzy_number_support():
    a = FuzzyNumber(pts_convex)
    assert a.support() == (a.x1, a.x4)


def test_fuzzy_number_core():
    a = FuzzyNumber(pts_convex)
    assert a.core() == (a.x2, a.x3)
    in_core = set(
        x
        for (x, y) in pts_convex.items()
        if y == 1
    )
    assert a.core() == (
        min(in_core),
        max(in_core)
    ), pformat(locals())


# TODO add missing tests


def test_fuzzy_number_plot():
    a = FuzzyNumber(pts_convex)
    a.plot()
