# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause

from fuzzy_set import TrapezoidalFuzzyNumber


class TriangularFuzzyNumber(TrapezoidalFuzzyNumber):
    """
    A *Triangular Fuzzy Number* is a Trapezoidal
    Fuzzy Number whose core is reduced to a single value.
    Therefore, it is piecewise linear and continuous and
    has a triangular shape. As a consequence, it is fully
    characterized by a triple of real numbers, denoted by
    :math:`[x_1, x_2, x_3]`, where:

    - :math:`a_1 \\le a_2 \\le a_3`;
    - :math:`[a_1, a_3]` is its support;
    - :math:`\\{a_2\\}` is its core.

    **Example:**

    >>> from fuzzy_set import TriangularFuzzyNumber
    >>> t1 = TriangularFuzzyNumber(1, 3, 10)
    >>> t2 = TriangularFuzzyNumber(2, 5, 8)
    >>> t1 + t2
    TriangularFuzzyNumber<(3, 8, 18)>
    >>> t1 - t2
    TriangularFuzzyNumber<(-7, -2, 8)>
    >>> t1 * t2
    TriangularFuzzyNumber<(2, 15, 80)>
    >>> t1 / t2
    TriangularFuzzyNumber<(0.125, 0.6, 5.0)>

    **Example:**

    .. code-block:: python

        import matplotlib.pyplot as plt
        from operator import __add__, __sub__, __mul__, __truediv__
        (fig, axs) = plt.subplots(2, 2)
        for (ij, (op, opname)) in {
            (0, 0): (__add__, "+"),
            (0, 1): (__sub__, "-"),
            (1, 0): (__mul__, "\\cdot"),
            (1, 1): (__truediv__, "/"),
        }.items():
            ax = axs[ij]
            title = f"$a_1 {opname} a_2$"
            ax.set_title(title)
            t1.plot(ax=ax, label="$a_1$")
            t2.plot(ax=ax, label="$a_2$")
            op(t1, t2).plot(ax=axs[ij], label=title)
            ax.grid()
            ax.legend()
            ax.legend(bbox_to_anchor=(1, 0.5), loc="center left")
        plt.tight_layout()
    """
    def __init__(self, a1: float, a2: float, a3: float):
        super().__init__(x1=a1, x2=a2, x3=a2, x4=a3)

    @property
    def a1(self) -> float:
        return self.x1

    @property
    def a2(self) -> float:
        return self.x2

    @property
    def a3(self) -> float:
        return self.x4

    @a1.setter
    def a1(self, value: float):
        self.x1 = value

    @a2.setter
    def a2(self, value: float):
        self.x2 = self.x3 = value

    @a3.setter
    def a3(self, value: float):
        self.x4 = value

    def __add__(
        self,
        other: "TriangularFuzzyNumber"
    ) -> "TriangularFuzzyNumber":
        """
        Adds this :math:`[a_1, a_2, a_3]` TFN
        and another :math:`[b_1, b_2, b_3]` TFN.

        Args:
            other (TriangularFuzzyNumber): The other TFN.

        Returns:
            The resulting
            :math:`[a_1 + b_1, a_2 + b_2, a_3 + b_3]`
            TFN.
        """
        return self.__class__(
            self.a1 + other.a1,
            self.a2 + other.a2,
            self.a3 + other.a3,
        )

    def __sub__(
        self,
        other: "TriangularFuzzyNumber"
    ) -> "TriangularFuzzyNumber":
        """
        Subtracts this :math:`[a_1, a_2, a_3]` TFN
        and another :math:`[b_1, b_2, b_3]` TFN.

        Args:
            other (TriangularFuzzyNumber): The other TFN.

        Returns:
            The resulting
            :math:`[a_1 - b_3, a_2 - b_2, a_3 - b_1]` TFN.
        """
        return self.__class__(
            self.a1 - other.a3,
            self.a2 - other.a2,
            self.a3 - other.a1,
        )

    def __mul__(
        self,
        other: "TriangularFuzzyNumber"
    ) -> "TriangularFuzzyNumber":
        """
        Approximates the multiplication of
        this :math:`[a_1, a_2, a_3]` TFN
        and another :math:`[b_1, b_2, b_3]` TFN.

        Args:
            other (TriangularFuzzyNumber): The other TFN.

        Returns:
            The resulting approximated
            :math:`[a_1 \\cdot b_1, a_2 \\cdot b_2,
            a_3 \\cdot b_3]` TFN.
        """
        return self.__class__(
            self.a1 * other.a1,
            self.a2 * other.a2,
            self.a3 * other.a3,
        )

    def __truediv__(
        self,
        other: "TriangularFuzzyNumber"
    ) -> "TriangularFuzzyNumber":
        """
        Approximates the division of
        this :math:`[a_1, a_2, a_3]` TFN
        and another :math:`[b_1, b_2, b_3]` TFN.

        Args:
            other (TriangularFuzzyNumber): The other TFN.

        Returns:
            The resulting approximated
            :math:`[a_1 / b_3 , a_2 / b_2 , a_3 / b_1]` TFN.
        """
        return self.__class__(
            self.a1 / other.a3,
            self.a2 / other.a2,
            self.a3 / other.a1
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"<{self.a1, self.a2, self.a3}>"
        )
