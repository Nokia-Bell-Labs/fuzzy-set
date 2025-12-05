from pprint import pformat
from fuzzy_set import find_intersection


def test_find_intersection_vertical_cross():
    p1, p2 = (-10, 0), (10, 0)
    p3, p4 = (0, -10), (0, 10)
    obtained = find_intersection(p1, p2, p3, p4)
    expected = (0, 0)
    assert obtained == expected, pformat(locals())


def test_find_intersection_cross():
    p1, p2 = (1, 1), (4, 4)
    p3, p4 = (0, 3), (6, 0)
    obtained = find_intersection(p1, p2, p3, p4)
    expected = (2, 2)
    assert obtained == expected, pformat(locals())


def test_find_intersection_superposed():
    p1, p2 = (1, 1), (5, 1)
    p3, p4 = (2, 1), (7, 1)
    obtained = find_intersection(p1, p2, p3, p4)
    expected = None
    assert obtained == expected, pformat(locals())


def test_find_intersection_parallel():
    p1, p2 = (1, 1), (5, 1)
    p3, p4 = (2, 2), (7, 2)
    obtained = find_intersection(p1, p2, p3, p4)
    expected = None
    assert obtained == expected, pformat(locals())


def test_find_intersection_undefined():
    p1, p2 = (9, 0.1), (10, 0)
    p3, p4 = p1, p2
    obtained = find_intersection(p1, p2, p3, p4)
    expected = None
    assert obtained == expected, pformat(locals())
