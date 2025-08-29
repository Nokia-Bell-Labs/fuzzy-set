# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause

"""
This module provides utilities to compute the intersection
of two lines.
"""


def find_intersection(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float]
) -> tuple[float, float] | None:
    """
    Computes the intersection of two lines :math:`D`
    and :math:`D'` such that:

    - :math:`D` traverses the points :math:`P_1(x_1, y_1)`
      and :math:`P_2(x_2, y_2)` where :math:`x_1 \\ne x_2``;
    - :math:`D'` traverses the points :math:`P_3(x_3, y_3)`
      and :math:`P_4(x_4, y_4)` where :math:`x_3 \\ne x_4``;

    Args:
        p1 (tuple[float, float]): The point :math:`P_1`.
        p2 (tuple[float, float]): The point :math:`P_2`.
        p3 (tuple[float, float]): The point :math:`P_3`.
        p4 (tuple[float, float]): The point :math:`P_4`.

    Returns:
        The intersection point of :math:`D`
        and :math:`D'` if uniquely defined,
        ``None`` otherwise.
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    d = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    if d == 0:
        return None
    a = (x1 * y2 - y1 * x2)
    b = (x3 * y4 - y3 * x4)
    px = (a * (x3 - x4) - b * (x1 - x2)) / d
    py = (a * (y3 - y4) - b * (y1 - y2)) / d
    return (px, py)
