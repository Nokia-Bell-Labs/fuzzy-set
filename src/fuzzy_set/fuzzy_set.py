# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from .intersection import find_intersection


INFINITY = np.inf
"""Infinity (:math:`\\infty`)"""

REALS = (-INFINITY, INFINITY)
"""The set of real numbers (:math:`\\mathbb{R}``)"""


class FuzzySet(dict):
    """
    A *fuzzy set* is defined by a :math:`A = (U, \\mu)` pair,
    where:

    - :math:`U` is a set called universe;
    - :math:`m: E \\rightarrow [0, 1]` is the membership
      function of :math:̀`A`.

    The :py:class:`FuzzySet` class implements a
    `Fuzzy set <https://en.wikipedia.org/wiki/Fuzzy_set>`__
    :math:`U \\subseteq \\mathbb{R}` having either

    - a piecewise linear membership function;
    - a discrete membership function.

    In the :py:class:`FuzzySet` class implementation, you should
    choose a universe as tight as possible with respect to the
    `support
    <https://en.wikipedia.org/wiki/Fuzzy_set#Crisp_sets_related_to_a_fuzzy_set>`__
    of the fuzzy set you need to manipulate.

    *Example:*

    >>> import matplotlib.pyplot as plt
    >>> from fuzzy_set import FuzzySet
    >>> a1 = FuzzySet(
    ...     dict(enumerate([0, 0, 0.1, 0.2, 0.7, 1, 1, 0.7, 0.2, 0.1, 0]))
    ... )
    >>> a1.plot(label="$a_1$", marker="x")
    >>> plt.legend()
    >>> plt.grid()
    >>> plt.show()
    """
    def __init__(
        self,
        mu: dict[float, float],
        is_continuous: bool = True,
        e: tuple[float, float] = REALS
    ):
        """
        Constructor.

        Args:
            mu (dict[float, float]): The membership function.

                - If `is_continuous is True`, each (key, value)
                  pair corresponds to an element of the fuzzy set;
                - If `is_continuous is False`, each (key, value)
                  pair characterizes a point of the membership
                  function which is assumed to be piecewise linear.

            is_continuous (bool): Pass `True` if the membership
                function is piecewise linear. Otherwise the
                membership is supposed to be discrete.

            e (tuple[float, float]): The definition interval of
                :math:`mu`. This parameter is only relevant if
                if ``is_continuous is True``, otherwise, the
                definition of set of :math:`mu` is ``set(mu.keys())``.
        """
        super().__init__(mu)
        assert mu
        assert mu[min(mu)] == 0
        assert mu[max(mu)] == 0
        self.is_continuous = is_continuous
        if is_continuous:
            xs = list(mu.keys())
            ys = list(mu.values())
            self._m = interp1d(xs, ys)
            assert isinstance(e, tuple)
            assert len(e) == 2
            assert e[0] < e[1]
            self.e = e
        else:
            self.e = set(mu.keys())

    def _xs(self, other: "FuzzySet") -> iter:
        """
        Implementation method, used to iterate on the relevant
        value of this fuzzy set and another one.

        Args:
            other (FuzzySet): The other fuzzy set.

        Returns:
            The corresponding iterator.
        """
        xs = sorted(set(self.keys()) | set(other.keys()))
        if self.is_continuous:
            assert other.is_continuous
            # Search for interesction points. This is needed
            # for set-based operation (i.e., &, |, -) as the
            # resulting fuzzy set may require to consider
            # additional points.
            x_prev = y1_prev = y2_prev = None
            for (i, x) in enumerate(xs):
                y1 = self.m(x)
                y2 = other.m(x)
                if i > 0:
                    a = (x_prev, y1_prev)
                    b = (x, y1)
                    c = (x_prev, y2_prev)
                    d = (x, y2)
                    inter = find_intersection(a, b, c, d)
                    if inter and x_prev < inter[0] < x:
                        yield inter[0]
                yield x
                (x_prev, y1_prev, y2_prev) = (x, y1, y2)
                if i == 0:
                    continue
        else:
            assert not other.is_continuous
            yield from xs

    def m(self, x: float) -> float:
        """
        Retrieves the membership degrees of an element.

        If this :py:class:`FuzzySet` instance is continuous,
        (i.e., if `self.is_continuous`), the value use obtained
        using a linear interpolation.

        Args:
            x (float): The considered element.

        Returns:
            The membership value corresponding to `x`.
        """
        assert isinstance(x, (int, float)), x
        if self.is_continuous:
            if x < min(self.keys()) or x > max(self.keys()):
                return 0.0
            elif x in self:
                return self[x]
            else:
                ret = self._m(x)
                if isinstance(ret, float):
                    return ret
                return (
                    ret if isinstance(ret, float)
                    else float(ret)
                )
        else:
            return self.get(x)

    def fully_contains(self, x: float) -> bool:
        """
        Checks whether this :py:class:`FuzzySet` instance
        fully contains an element.

        Args:
            x (float): The considered element.

        Returns:
            ``True`` if ``x`` is fully contained in ``self``,
            ``False`` otherwise.
        """
        return self.m(x) == 1

    def partially_contains(self, x: float) -> bool:
        """
        Checks whether this :py:class:`FuzzySet` instance
        partially contains an element.

        Args:
            x (float): The considered element.

        Returns:
            ``True`` if ``x`` is partially contained in ``self``,
            ``False`` otherwise.
        """
        return 0 < self.m(x) < 1

    def doesnt_contain(self, x: float) -> bool:
        """
        Checks whether this :py:class:`FuzzySet` instance
        doesn't contains an element.

        Args:
            x (float): The considered element.

        Returns:
            ``True`` if ``x`` isn't contained in ``self``,
            ``False`` otherwise.
        """
        return self.m(x) == 0

    # Crisp sets related to a fuzzy set
    # https://en.wikipedia.org/wiki/Fuzzy_set#Crisp_sets_related_to_a_fuzzy_set

    def cut(self, alpha: float) -> set:
        """
        Computes an
        :math:`\\alpha`-`cut
        <https://en.wikipedia.org/wiki/Fuzzy_set#Crisp_sets_related_to_a_fuzzy_set>`__
        of this fuzzy set, denoted by :math:`A^{x \\ge \\alpha}`.

        Args:
            alpha (float): The threshold involved in the
                :math:`\\alpha`-cut.

        Returns:
            The crisp set containing every element involved in
            the :math:`\\alpha`-cut.
        """
        return set(x for x in self if self.m(x) >= alpha)

    def strong_cut(self, alpha: float) -> set:
        """
        Assuming this fuzzy set is discrete, computes a strong
        :math:`\\alpha`-`cut
        <https://en.wikipedia.org/wiki/Fuzzy_set#Crisp_sets_related_to_a_fuzzy_set>`__
        of this fuzzy set, denoted by :math:`A^{x \\gt \\alpha}`.

        Args:
            alpha (float): The :math:`alpha value, contained in
                the :math:`[0.0, 1.0]` interval.

        Returns:
            The crisp set containing every element involved in
            the :math:`\\alpha`-cut.
        """
        return set(x for x in self if self.m(x) > alpha)

    def at(self, alpha: float) -> set:
        """
        Assuming this fuzzy set is discrete, retrieves the
        element that matches a given arbitrary :math:`alpha` value.

        Args:
            alpha (float): The :math:`alpha value, contained in
                the :math:`[0.0, 1.0]` interval.
        """
        return set(x for x in self if self.m(x) == alpha)

    def support(self) -> set:
        """
        Assuming this fuzzy set is discrete, computes the `support
        <https://en.wikipedia.org/wiki/Fuzzy_set#Crisp_sets_related_to_a_fuzzy_set>`__
        of this fuzzy set, denoted by :math:`A^{>0}`.

        Returns:
            The crisp set containing every element involved in
            the support.
        """
        return self.strong_cut(0)

    def core(self) -> set:
        """
        Assuming this fuzzy set is discrete, computes the `core
        <https://en.wikipedia.org/wiki/Fuzzy_set#Crisp_sets_related_to_a_fuzzy_set>`__
        of this fuzzy set, denoted by :math:`A^{=1}`.

        Returns:
            The crisp set containing every element involved in
            the core.
        """
        return self.at(1)

    # Other definitions
    # https://en.wikipedia.org/wiki/Fuzzy_set#Other_definitions

    def is_empty(self) -> bool:
        """
        Assuming this fuzzy set is discrete,
        checks whether this fuzzy set is empty.

        Returns:
            ``True`` if this fuzzy set is empty,
            ``False`` otherwise.
        """
        return all(self.m(x) == 0 for x in self)

    def __eq__(self, other: "FuzzySet") -> bool:
        """
        Checks whether two fuzzy sets are
        `equal <https://en.wikipedia.org/wiki/Fuzzy_set#Other_definitions>`__.

        Args:
            other (FuzzySet): The right operand.

        Returns:
            ``True`` if the fuzzy sets are equal,
            ``False`` otherwise.
        """
        return (
            self.e == other.e
            and self.is_continuous == other.is_continuous
            and all(self.m(x) == other.m(x) for x in self._xs(other))
        )

    def __ne__(self, other: "FuzzySet") -> bool:
        """
        Checks whether two fuzzy sets are `different
        <https://en.wikipedia.org/wiki/Fuzzy_set#Other_definitions>`__.

        Args:
            other (FuzzySet): The right operand.

        Returns:
            ``True`` if the fuzzy sets are different,
            ``False`` otherwise.
        """
        return (not self == other)

    def __le__(self, other: "FuzzySet") -> bool:
        """
        Checks whether this fuzzy set is `contained
        <https://en.wikipedia.org/wiki/Fuzzy_set#Other_definitions>`__
        in another fuzzy set.

        Args:
            other (FuzzySet): The right operand.

        Returns:
            ``True`` if this fuzzy set is included in ``other``,
            ``False`` otherwise.
        """
        assert self.e == other.e
        return all(self.m(x) <= other.m(x) for x in self._xs(other))

    def __lt__(self, other: "FuzzySet") -> bool:
        """
        Checks whether this fuzzy set is `strictly contained
        <https://en.wikipedia.org/wiki/Fuzzy_set#Other_definitions>`__
        in another fuzzy set.

        Args:
            other (FuzzySet): The right operand.

        Returns:
            ``True`` if this fuzzy set is included in ``other``,
            ``False`` otherwise.
        """
        assert self.e == other.e
        return all(self.m(x) < other.m(x) for x in self._xs(other))

    def __ge__(self, other: "FuzzySet") -> bool:
        """
        Checks whether this fuzzy set `contains
        <https://en.wikipedia.org/wiki/Fuzzy_set#Other_definitions>`__
        another fuzzy set.

        Args:
            other (FuzzySet): The right operand.

        Returns:
            ``True`` if this fuzzy set contains ``other``,
            ``False`` otherwise.
        """
        assert self.e == other.e
        return all(self.m(x) >= other.m(x) for x in self._xs(other))

    def __gt__(self, other: "FuzzySet") -> bool:
        """
        Checks whether this fuzzy set `striclty contains
        <https://en.wikipedia.org/wiki/Fuzzy_set#Other_definitions>`__
        another fuzzy set.

        Args:
            other (FuzzySet): The right operand.

        Returns:
            ``True`` if this fuzzy set contains ``other``,
            ``False`` otherwise.
        """
        assert self.e == other.e
        return all(self.m(x) >= other.m(x) for x in self._xs(other))

    def is_crossover(self, x: float) -> bool:
        """
        Checks whether a value is a `crossover point
        <https://en.wikipedia.org/wiki/Fuzzy_set#Other_definitions>`__
        of this fuzzy set.

        Args:
            x (float): A value in ``self``.

        Returns:
            ``True`` if ``x`` is a crossover points of this fuzzy set,
            ``False`` otherwise.
        """
        return self.at(0.5)

    def height(self) -> float:
        """
        Computes the `height
        <https://en.wikipedia.org/wiki/Fuzzy_set#Other_definitions>`__
        of this fuzzy set.

        Returns:
            The height of this fuzzy set.
        """
        return max(self.m(x) for x in self)

    def is_normalized(self) -> bool:
        """
        Tests whether this fuzzy set is `normalized
        <https://en.wikipedia.org/wiki/Fuzzy_set>`__.

        Returns:
           ``True`` if this fuzzy set is normalized,
           ``False`` otherwise.
        """
        return self.height() == 1

    def width(self) -> float:
        """
        Computes the
        `width <https://en.wikipedia.org/wiki/Fuzzy_set>`__
        of this fuzzy set.

        Returns:
            The width of this fuzzy set.
        """
        return self.height() - min(self.m(x) for x in self)

    # Fuzzy set operations
    # https://en.wikipedia.org/wiki/Fuzzy_set#Fuzzy_set_operations

    def __not__(self) -> "FuzzySet":
        """
        Assuming this fuzzy set membership is piecewise linear,
        computes the `complement
        <https://en.wikipedia.org/wiki/Fuzzy_set#Fuzzy_set_operations>`__
        of this fuzzy set.

        Returns:
            The complement of this fuzzy set.
        """
        return FuzzySet(set(self), lambda x: 1 - self.m(x))

    def __neg__(self) -> "FuzzySet":
        """
        Assuming this fuzzy set membershup is piecewise linear,
        computes the `negation
        <https://en.wikipedia.org/wiki/Fuzzy_set#Fuzzy_set_operations>`__
        of this fuzzy set.

        Returns:
            The negation of this fuzzy set.
        """
        return not self

    def _intersection_union(
        self,
        other: "FuzzySet",
        norm: callable
    ) -> "FuzzySet":
        """
        Implementation method, used when computing the intersection
        or the union of this uzzy set and another one.

        See also the
        :py:meth:`FuzzySet.intersection`,
        :py:meth:`FuzzySet.union`,
        :py:meth:`FuzzySet.__and__`,
        :py:meth:`FuzzySet.__or__` methods.

        Args:
            other (FuzzySet): The other fuzzy set.

        Returns:
            The corresponding iterator.
        """
        return FuzzySet({
            x: norm(self.m(x), other.m(x))
            for x in self._xs(other)
        })

    def intersection(
        self,
        other: "FuzzySet",
        tnorm: callable = min
    ) -> "FuzzySet":
        """
        Computes the `intersection
        <https://en.wikipedia.org/wiki/Fuzzy_set#Fuzzy_set_operations>`__
        of two fuzzy-sets according to an arbitrary
        `T-norm <https://en.wikipedia.org/wiki/T-norm>`__
        (e.g., :math:`min` ).

        Args:
            other (FuzzySet): The right operand.
            tnorm (callable): A `T-norm
                <https://en.wikipedia.org/wiki/T-norm>`__.

        Returns:
            The fuzzy set intersection.
        """
        return self._intersection_union(other, tnorm)

    def __and__(self, other: "FuzzySet") -> "FuzzySet":
        """
        Computes the `(default) intersection
        <https://en.wikipedia.org/wiki/Fuzzy_set#Fuzzy_set_operations>`__
        of two fuzzy-sets.

        Args:
            other (FuzzySet): The right operand.

        Returns:
            The default fuzzy set intersection.
        """
        return self.intersection(other, min)

    def union(self, other: "FuzzySet", snorm: callable = min) -> "FuzzySet":
        """
        Computes the `union
        <https://en.wikipedia.org/wiki/Fuzzy_set#Fuzzy_set_operations>`__
        of two fuzzy-sets according to an arbitrary
        `S-norm <https://en.wikipedia.org/wiki/T-norm>`__ (e.g., :math:`min` ).

        Args:
            other (FuzzySet): The right operand.
            snorm (callable): A `T-norm
                <https://en.wikipedia.org/wiki/T-norm>`__.

        Returns:
            The fuzzy set intersection.
        """
        return self._intersection_union(other, snorm)

    def __or__(self, other: "FuzzySet") -> "FuzzySet":
        """
        Computes the `(default) union
        <https://en.wikipedia.org/wiki/Fuzzy_set#Fuzzy_set_operations>`__
        of two fuzzy-sets.

        Args:
            other (FuzzySet): The right operand.

        Returns:
            The default fuzzy set intersection.
        """
        return self.union(other, max)

    def __pow__(self, nu: float) -> "FuzzySet":
        """
        Computes the :math:`nu`-`power
        <https://en.wikipedia.org/wiki/Fuzzy_set#Fuzzy_set_operations>`__
        of this fuzzy set.

        Args:
            nu (float): A positive real.

        Returns:
            The corresponding fuzzy set.
        """
        assert nu >= 0
        return FuzzySet({
            x: y ** nu
            for (x, y) in self.items()
        })

    def concentration(self) -> "FuzzySet":
        """
        Computes the `concentration
        <https://en.wikipedia.org/wiki/Fuzzy_set#Fuzzy_set_operations>`__
        of this fuzzy set.

        Returns:
            The corresponding fuzzy set.
        """
        return self ** 2

    def difference(self, other: "FuzzySet", tnorm: callable) -> "FuzzySet":
        """
        Computes the `difference
        <https://en.wikipedia.org/wiki/Fuzzy_set#Fuzzy_set_operations>`__
        of two fuzzy-sets.

        Args:
            other (FuzzySet): The right operand.
            tnorm (callable): A `T-norm
                <https://en.wikipedia.org/wiki/T-norm>`__.

        Returns:
            The fuzzy set difference.
        """
        return FuzzySet({
            x: self.m(x) - tnorm(self.m(x), other.m(x))
            for x in self._xs(other)
        })

    def __sub__(self, other: "FuzzySet", tnorm: callable = min) -> "FuzzySet":
        """
        Computes the `default difference
        <https://en.wikipedia.org/wiki/Fuzzy_set#Fuzzy_set_operations>`__
        of two fuzzy-sets.

        Args:
            other (FuzzySet): The right operand.
            tnorm (callable): A `T-norm
                <https://en.wikipedia.org/wiki/T-norm>`__.

        Returns:
            The default fuzzy set difference.
        """
        return FuzzySet({
            # x: min(self.m(x), 1 - other.m(x))
            x: self.m(x) - tnorm(self.m(x), other.m(x))
            for x in self._xs(other)
        })

    def absolute_difference(self, other: "FuzzySet") -> "FuzzySet":
        """
        Computes the `absolute default difference
        <https://en.wikipedia.org/wiki/Fuzzy_set#Fuzzy_set_operations>`__
        of two fuzzy-sets.

        Args:
            other (FuzzySet): The right operand.

        Returns:
            The default fuzzy set absolute difference.
        """
        return FuzzySet({
            x: abs(self.m(x) - other.m(x))
            for x in self._xs(other)
        })

    # Disjoint fuzzy sets
    # https://en.wikipedia.org/wiki/Fuzzy_set#Fuzzy_set_operations

    def is_disjoint(self, other: "FuzzySet") -> bool:
        """
        Tests whether this fuzzy set and another are `disjoint
        <https://en.wikipedia.org/wiki/Fuzzy_set#Fuzzy_set_operations>`__.

        Args:
            other (FuzzySet): The fuzzy set compared to ``self``.

        Returns:
            ``True`` if the fuzzy sets are disjoint,
            ``False`` otherwise.
        """
        return all(
            self.m(x) == 0 or other.m(x) == 0
            for x in self._xs(other)
        )

    # Scalar cardinality
    # https://en.wikipedia.org/wiki/Fuzzy_set#Scalar_cardinality

    def card(self) -> float:
        """
        Computes the `scalar cardinality
        <https://en.wikipedia.org/wiki/Fuzzy_set#Scalar_cardinality>`__
        of a fuzzy set.

        Returns:
            The scalar cardinality of this fuzzy set.
        """
        return sum(self.m(x) for x in self)

    def relative_card(self, other: "FuzzySet" = None) -> float:
        """
        Computes the `relative cardinality
        <https://en.wikipedia.org/wiki/Fuzzy_set#Scalar_cardinality>`__
        of this fuzzy set or the intersection of two fuzzy set.

        Args:
            g (FuzzySet): Another fuzzy set.
                Pass ``None`` or ``self`` is equivalent.

        Returns:
            The relative cardinality of this fuzzy set.
        """
        if not other or other is self:
            return self.card() / len(self)
        else:
            return (self & other) / len(self)

    # Distance and similarity
    # https://en.wikipedia.org/wiki/Fuzzy_set#Distance_and_similarity

    def plot(
        self,
        *cls,
        ax: matplotlib.axes.Axes = None,
        **kwargs
    ) -> matplotlib.collections.PathCollection:
        """
        Plots this Fuzzy Set.

        Args:
            cls, args: See the :py:func:`plt.plot` function.
            ax (matplotlib.axes.Axes): The axes of the figure where
                this :py:class:`FuzzySet` instance must be plotted.
                Pass `None` if not needed.

        Returns:
            The resulting corresponding plot.
        """
        if ax is None:
            ax = plt.gca()
        xs = sorted(list(self))
        ys = list(self.m(x) for x in xs)
        return ax.plot(xs, ys, *cls, **kwargs)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}<"
            f"{super().__repr__()}, "
            f"{'continuous' if self.is_continuous else 'discrete'}"
            ">"
        )

    def __str__(self) -> str:
        return self.__repr__()
