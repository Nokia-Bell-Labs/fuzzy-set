from fuzzy_set import INFINITY, REALS, FuzzySet


def test_infinity():
    for x in [-1000000, 0, 100000]:
        assert x < INFINITY
        assert abs(x) < INFINITY
        assert x > -INFINITY


def test_reals():
    (r_min, r_max) = REALS
    assert r_min == -INFINITY
    assert r_max == INFINITY


def test_fuzzy_set_eq():
    pts = dict(enumerate([0, 0, 0.1, 0.2, 0.7, 1, 1, 0.7, 0.2, 0.1, 0]))
    a1 = FuzzySet(pts)
    a2 = FuzzySet(pts)
    assert a1 == a2
    assert a1 <= a2
    assert not a1 < a2
    assert a1 >= a2
    assert a1 > a2
    a3 = FuzzySet(pts, e=(0, 20))
    assert a1 != a3


def test_fuzzy_set_ne():
    a1 = FuzzySet(
        dict(enumerate([0, 0, 0.1, 0.2, 0.7, 1, 1, 0.7, 0.2, 0.1, 0]))
    )
    a2 = FuzzySet(
        dict(enumerate([0, 0, 0.2, 0.3, 0.8, 1, 1, 0.8, 0.3, 0.2, 0]))
    )
    assert a1 != a2
    assert not a1 == a2


# TODO add missing methods


def test_fuzzy_set_plot():
    a = FuzzySet(
        dict(enumerate([0, 0, 0.1, 0.2, 0.7, 1, 1, 0.7, 0.2, 0.1, 0]))
    )
    a.plot()
