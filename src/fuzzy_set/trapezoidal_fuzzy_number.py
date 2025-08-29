# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause

from .fuzzy_number import FuzzyNumber


class TrapezoidalFuzzyNumber(FuzzyNumber):
    """
    A *Trapezoidal Fuzzy Number (TFN)* is a Fuzzy Number (FN)
    which is piecewise linear and continuous. Thus, it has a
    trapezoidal shape). As a consequence, a TFN is fully
    characterized by a quadruple of real numbers, denoted by
    :math:`[x_1, x_2, x_3, x_4]`, where:

    - :math:`x_1 \\le ... \\le x_n`;
    - :math:`[x_1, x_4]` is the support of the TFN;
    - :math:`[x_2, x_3]` is the core of the TFN.

    Trapezoidal Fuzzy Numbers support arithmetic operators, i.e., +, -, \\*, /.
    See `Reliability Range Through Upgraded Operation with TFN
    <https://www.tandfonline.com/doi/full/10.1080/16168658.2021.1918039#d1e133>`__.

    Example:

    >>> from fuzzy_set import TrapezoidalFuzzyNumber
    >>> a1 = TrapezoidalFuzzyNumber(1, 3, 8, 10)
    >>> a2 = TrapezoidalFuzzyNumber(2, 5, 7, 8)
    >>> a1 + a2
    TrapezoidalFuzzyNumber<(3, 8, 15, 18)>
    >>> a1 - a2
    TrapezoidalFuzzyNumber<(-7, -4, 3, 8)>
    >>> a1 * a2
    TrapezoidalFuzzyNumber<(2, 15, 56, 80)>
    >>> a1 / a2
    TrapezoidalFuzzyNumber<(0.125, 0.42857142857142855, 1.6, 5.0)>

    To get an overview:

    >>> import matplotlib.pyplot as plt
    ... from operator import __add__, __sub__, __mul__, __truediv__
    ... (fig, axs) = plt.subplots(2, 2)
    ... for (ij, (op, opname)) in {
    ...     (0, 0): (__add__, "+"),
    ...     (0, 1): (__sub__, "-"),
    ...     (1, 0): (__mul__, "\\cdot"),
    ...     (1, 1): (__truediv__, "/"),
    ... }.items():
    ...     ax = axs[ij]
    ...     title = f"$a_1 {opname} a_2$"
    ...     ax.set_title(title)
    ...     a1.plot(ax=ax, label="$a_1$")
    ...     a2.plot(ax=ax, label="$a_2$")
    ...     op(a1, a2).plot(ax=axs[ij], label=title)
    ...     ax.grid()
    ...     ax.legend()
    ...     ax.legend(bbox_to_anchor=(1, 0.5), loc="center left")
    ... plt.tight_layout()
    """
    def __init__(self, x1: float, x2: float, x3: float, x4: float):
        """
        Constructor. Makes a _Trapezoidal Fuzzy Number (TFN)_
        from four real numbers :math:`x_1 \\le x_2 \\le x_3 \\le x_4``.

        Args:
            x1 (float): The value of :math:`x_1`.
            x2 (float): The value of :math:`x_2`.
            x3 (float): The value of :math:`x_3`.
            x4 (float): The value of :math:`x_4`.
        """
        assert x1 <= x2 <= x3 <= x4, (x1, x2, x3, x4)
        super().__init__({x1: 0, x2: 1, x3: 1, x4: 0})

    def _init_xis(self):
        (self.x1, self.x2, self.x3, self.x4) = sorted(self.keys())

    def _check_convexity(self, points: dict[float, float]):
        pass

    def __add__(
        self,
        other: "TrapezoidalFuzzyNumber"
    ) -> "TrapezoidalFuzzyNumber":
        """
        Adds this :math:`[a_1 , a_2 , a_3 , a_4]` TFN
        and another :math:`[b_1 , b_2 , b_3 , b_4]` TFN.

        Args:
            other (TrapezoidalFuzzyNumber): The other TFN.

        Returns:
            The resulting
            :math:`[a_1 + b_1 , a_2 + b_2 , a_3 + b_3 , a_4 + b_4]`
            TFN.
        """
        return self.__class__(
            self.x1 + other.x1,
            self.x2 + other.x2,
            self.x3 + other.x3,
            self.x4 + other.x4
        )

    def __sub__(
        self,
        other: "TrapezoidalFuzzyNumber"
    ) -> "TrapezoidalFuzzyNumber":
        """
        Subtracts this :math:`[a_1 , a_2 , a_3 , a_4]` TFN
        and another :math:`[b_1 , b_2 , b_3 , b_4]` TFN.

        Args:
            other (TrapezoidalFuzzyNumber): The other TFN.

        Returns:
            The resulting
            :math:`[a_1 - b_4, a_2 - b_3, a_3 - b_2, a_4 - b_1]` TFN.
        """
        return self.__class__(
            self.x1 - other.x4,
            self.x2 - other.x3,
            self.x3 - other.x2,
            self.x4 - other.x1
        )

    def __mul__(
        self,
        other: "TrapezoidalFuzzyNumber"
    ) -> "TrapezoidalFuzzyNumber":
        """
        Approximates the multiplication of
        this :math:`[a_1 , a_2 , a_3 , a_4]` TFN
        and another :math:`[b_1 , b_2 , b_3 , b_4]` TFN.

        Args:
            other (TrapezoidalFuzzyNumber): The other TFN.

        Returns:
            The resulting approximated
            :math:`[a_1 \\cdot b_1, a_2 \\cdot b_2,
            a_3 \\cdot b_3, a_4 \\cdot b_4]` TFN.
        """
        return self.__class__(
            self.x1 * other.x1,
            self.x2 * other.x2,
            self.x3 * other.x3,
            self.x4 * other.x4
        )

    def __truediv__(
        self,
        other: "TrapezoidalFuzzyNumber"
    ) -> "TrapezoidalFuzzyNumber":
        """
        Approximates the division of
        this :math:`[a_1 , a_2 , a_3 , a_4]` TFN
        and another :math:`[b_1 , b_2 , b_3 , b_4]` TFN.

        Args:
            other (TrapezoidalFuzzyNumber): The other TFN.

        Returns:
            The resulting approximated
            :math:`[a_1 / b_4 , a_2 / b_3 , a_3 / b_2 , a_4 / b_1]` TFN.
        """
        return self.__class__(
            self.x1 / other.x4,
            self.x2 / other.x3,
            self.x3 / other.x2,
            self.x4 / other.x1
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"<{self.x1, self.x2, self.x3, self.x4}>"
        )

    def __str__(self) -> str:
        return self.__repr__()
