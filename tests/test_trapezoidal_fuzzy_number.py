from fuzzy_set import TrapezoidalFuzzyNumber
from pprint import pformat


a1 = TrapezoidalFuzzyNumber(1, 3, 8, 10)
a2 = TrapezoidalFuzzyNumber(2, 5, 7, 8)


def test_trapezoidal_add():
    obtained = a1 + a2
    expected = TrapezoidalFuzzyNumber(3, 8, 15, 18)
    assert obtained == expected, pformat(locals())


def test_trapezoidal_sub():
    obtained = a1 - a2
    expected = TrapezoidalFuzzyNumber(-7, -4, 3, 8)
    assert obtained == expected, pformat(locals())


def test_trapezoidal_mul():
    obtained = a1 * a2
    expected = TrapezoidalFuzzyNumber(2, 15, 56, 80)
    assert obtained == expected, pformat(locals())


def test_trapezoidal_truediv():
    obtained = a1 / a2
    expected = TrapezoidalFuzzyNumber(
        0.125, 0.42857142857142855, 1.6, 5.0
    )
    assert obtained == expected, pformat(locals())


def test_trapezoidal_xis():
    for xis in [
        (1, 3, 8, 10),
        (2, 5, 7, 8),
    ]:
        a = TrapezoidalFuzzyNumber(*xis)
        assert xis == (a.x1, a.x2, a.x3, a.x4)
