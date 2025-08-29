# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause

import matplotlib
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid
from .fuzzy_set import FuzzySet


class FuzzyNumber(FuzzySet):
    """
    A *Fuzzy Number (FN)* is Fuzzy Set :math:`A = (U, \\mu)` such that:

    - :math:`U = \\mathbb{R}`;
    - :math:`\\mu`  is a :math:`\\mathbb{R}` is a piecewise continuous
      function;
    - :math:`\\mu` is convex;
    - :math:`\\mu` is normalized (i.e., :math:`\\mu(\\mathbb{R}) = [0, 1]`).

    As such, a fuzzy number models a fuzzy interval of real numbers.

    The :py:class:`FuzzySet` class assumes a *discrete* Fuzzy Set.
    Therefore, the :py:class:`FuzzyNumber` takes a list of
    :math:`{(x_1, y_1), ..., (x_n, y_n)}` points enough to describe
    :math:`\\mu` such that:

    - :math:`x_1 \\le ... \\le x_n`;
    - :math:`\\mu(x_1) = 0` and :math:`\\mu(x_n) = 0`;
    - :math:`\\forall x \\le x_1 = 0`;
    - :math:`\\forall x \\ge x_n = 0`;
    - for all :math:`i \\in \\{1, ..., n-1\\}`,
      for all :math:`x \\in [x_i, x_{i+1}]`,
      :math:`\\mu` matches the linear function that traverses
      :math:`(x_i, y_i)` and :math:`(x_{i+1}, y_{i+1})`.

    *Example:*

    >>> import matplotlib.pyplot as plt
    >>> from fuzzy_set import FuzzyNumber
    >>> a1 = FuzzyNumber(dict(enumerate([0, 0, 0.01, 1, 1, 0.7, 0.2, 0.1, 0])))
    >>> a1.plot(label="$a_1$", marker=".", with_xis=False, with_ei=True)
    >>> plt.legend()
    >>> plt.grid()
    >>> plt.show()
    """
    def __init__(self, mu: dict[float, float]):
        """
        Constructor.

        Args:
            mu (dict[float, float]): The membership function. Each (key, value)
                  pair corresponds to an element of the fuzzy set.

        Raises:
            ValueError: if mu is not corresponding to a piecewise
                linear function or if it is not normalized.

        Example:
        >>> a1 = FuzzyNumber(
        ...     dict(enumerate([0, 0.6, 0.8, 1, 1, 0.9, 0]))
        ... )  # Convex
        >>> a2 = FuzzyNumber(
        ...     dict(enumerate([0, 0.1, 0.8, 1, 1, 0.9, 0]))
        ... )  # Not Convex
        """
        super().__init__(mu, is_continuous=True)
        if not self.is_normalized():
            raise ValueError("Not normalized")
        self.x1 = self.x2 = self.x3 = self.x4 = None
        self._init_xis()
        self._check_convexity(mu)

    def _init_xis(self):
        i = 0
        x_prev = y_prev = None
        for x in sorted(self):
            y = self.m(x)
            if y < 0:
                raise ValueError("Negative image")
            if i == 0:  # _
                if y > 0:  # _/
                    if x_prev is None:
                        raise ValueError("Invalid first element")
                    self.x1 = x_prev
                    i = 1
            elif i == 1:  # /
                if y < y_prev:
                    raise ValueError("Not normalized")
                elif y == 1.0:  # /-
                    self.x2 = self.x3 = x
                    i = 2
            elif i == 2:  # -
                if y < 1.0:  # --
                    self.x3 = x_prev
                    i = 3
            elif i == 3:  # \
                if y > y_prev:
                    raise ValueError("Not convex")
                elif y == 0:  # \_
                    self.x4 = x
                    i = 4
            elif i == 4:  # _
                if self.m(x) != 0:
                    raise ValueError("Not convex")
            x_prev = x
            y_prev = y

        assert self.x1 is not None
        assert self.x2 is not None
        assert self.x3 is not None
        assert self.x4 is not None
        assert self[self.x1] == 0.0, (self.x1, self[self.x1])
        assert self[self.x2] == 1.0, (self.x2, self[self.x2])
        assert self[self.x3] == 1.0, (self.x3, self[self.x3])
        assert self[self.x4] == 0.0, (self.x4, self[self.x4])

    def _check_convexity(self, points: dict[float, float]):
        from scipy.interpolate import interp1d
        from pprint import pformat
        x0 = y0 = x1 = y1 = y1 = None
        for (i, (x2, y2)) in enumerate(sorted(points.items())):
            if i > 1:
                # (x1, y1) must be above [(x0, y0), (x2, y2)]
                y1_ = interp1d([x0, x2], [y0, y2])(x1)
                if not (y1 >= y1_):
                    raise ValueError(pformat(locals()))
            if i > 0:
                (x0, y0) = (x1, y1)
            (x1, y1) = (x2, y2)

    def support(self) -> tuple:
        """
        Computes the `support
        <https://en.wikipedia.org/wiki/Fuzzy_set#Crisp_sets_related_to_a_fuzzy_set>`__
        of this fuzzy number, denoted by :math:`A^{>0}`.

        Returns:
            The interval of reals corresponding
            to the support of this fuzzy number.
        """
        return (self.x1, self.x4)

    def core(self) -> tuple:
        """
        Computes the `core
        <https://en.wikipedia.org/wiki/Fuzzy_set#Crisp_sets_related_to_a_fuzzy_set>`__
        of this fuzzy number, denoted by :math:`A^{=1}`.

        Returns:
            The interval of reals corresponding
            to the core of this fuzzy number.
        """
        return (self.x2, self.x3)

    def ei_l(self) -> float:
        """
        Computes the `Expected Interval Lower Bound
        <https://www.atlantis-press.com/article/2302.pdf>`__,
        formally defined by:
        :math:`\\text{EI}_L(A) = \\int_{0}^1 A_L(\\alpha).d\\alpha`
        where:
        :math:`A_L(\\alpha) = \\inf({x \\in \\mathbb{R}
        : \\mu_A(x) \\ge \\alpha})`

        Intuitively, :math:`\\text{EI}_L(A)` is the
        :math:`\\ell \\in \\mathbb{R}` value such that
        :math:`\\mu_A(\\ell)` equals average value of the left
        arm of this Fuzzy Number.

        Returns:
            The Expected Interval Lower Bound.
        """
        (xs, ys) = zip(*(
            (x, self[x])
            for x in sorted(self.keys())
            if self.x1 <= x <= self.x2
        ))
        return trapezoid(xs, x=ys)

    def ei_u(self) -> float:
        """
        Computes the `Expected Interval Upper Bound
        <https://www.atlantis-press.com/article/2302.pdf>`__,
        formally defined by:
        :math:`\\text{EI}_L(A) = \\int_{0}^1 A_U(\\alpha).d\\alpha`.
        where:
        :math:`A_U(\\alpha) = \\sup({x \\in \\mathbb{R}
        : \\mu_A(x) \\ge \\alpha})`

        Intuitively, :math:`\\text{EI}_L(A)` is the :math:`r \\in \\mathbb{R}`
        value such that :math:`\\mu_A(r)` equals average value of the right
        arm of this Fuzzy Number.

        Returns:
            The Expected Interval Upper Bound.
        """
        (xs, ys) = zip(*(
            (x, self[x])
            for x in sorted(self.keys(), reverse=True)
            if self.x3 <= x <= self.x4
        ))
        return trapezoid(xs, x=ys)

    def ei(self) -> tuple:
        """
        Computes the `Expected Interval
        <https://www.atlantis-press.com/article/2302.pdf>`__,
        formally defined by:
        :math:`\\text{EI}(A) = [\\text{EI}_L(A), \\text{EI}_U(A)]`.

        See also the
        :py:meth:`FuzzyNumber.ei_l`,
        :py:meth:`FuzzyNumber.ei_u`,
        :py:meth:`FuzzyNumber.ev` methods.

        Returns:
            The Expected Interval.
        """
        return (self.ei_l(), self.ei_u())

    def ev(self, q: float = 0.5) -> float:
        """
        Computes the `(Weighed) Expected Value
        <https://www.atlantis-press.com/article/2302.pdf>`__
        of this fuzzy number, formally defined as
        the middle of the `Expected Interval
        <https://www.atlantis-press.com/article/2302.pdf>`__:
        :math:`\\text{EV}(A)
        = q \\cdot \\text{EI}_L(A) + (1 - q) \\cdot \\text{EI}_U(A)`

        See also the
        :py:meth:`FuzzyNumber.ei_l`,
        :py:meth:`FuzzyNumber.ei_u`,
        :py:meth:`FuzzyNumber.ei` methods.

        Args:
            q (float): A value in :math:`[0, 1]`.
                Default to ``0.5``.

        Returns:
            The weighted expected value of this fuzzy number.
        """
        assert 0 <= q <= 1
        return q * self.ei_l() + (1 - q) * self.ei_u()

    def width(self) -> float:
        """
        Computes the `width
        <https://www.atlantis-press.com/article/2302.pdf>`__
        of this fuzzy number, formally defined as
        the middle of the `Expected Interval
        <https://www.atlantis-press.com/article/2302.pdf>`__:
        :math:`\\text{w}(A) = \\text{EI}_U(A) - \\text{EI}_L(A))`

        See also the
        :py:meth:`FuzzyNumber.ei_l`,
        :py:meth:`FuzzyNumber.ei_u`,
        :py:meth:`FuzzyNumber.ei` methods.

        Returns:
            The width of this fuzzy number.
        """
        return self.ei_u() - self.ei_l()

    def plot(
        self,
        *args,
        ax=None,
        with_xis: bool = False,
        with_ei: bool = False,
        **kwargs
    ) -> matplotlib.collections.PathCollection:
        """
        Plots this Fuzzy Number.

        Args:
            cls, args: See the :py:func:`plt.plot` function.
            ax (matplotlib.axes.Axes): The axes of the figure where
                this :py:class:`FuzzySet` instance must be plotted.
                Pass `None` if not needed.
            with_xis (bool): Pass `True` to display the support
                and the core of this Fuzzy Number. See also:

                - the :py:meth:`FuzzyNumber.support` method;
                - the :py:meth:`FuzzyNumber.core` method.

        Returns:
            The resulting corresponding plot.
        """
        if ax is None:
            ax = plt.gca()
        kwargs.pop("with_xis", None)
        kwargs.pop("with_ei", None)
        label = kwargs.pop("label", "")
        kwargs.pop("marker", None)
        p = super().plot(*args, ax=ax, marker=".", label=label, **kwargs)[0]
        color = kwargs.pop("color", p.get_color())

        # Transition phase points
        if with_xis:
            xs = [self.x1, self.x2, self.x3, self.x4]
            ys = [self[self.x1], self[self.x2], self[self.x3], self[self.x4]]
            p = ax.scatter(
                xs, ys,
                *args,
                color=color, marker="o", label=f"{label}.{{x1, x2, x3, x3}}",
                **kwargs
            )

        # Expected interval
        if with_ei:
            (ei_l, ei_u) = self.ei()
            ev = self.ev()
            xs = [ei_l, ev, ei_u]
            ys = [self.m(x) for x in xs]
            if "marker" in kwargs:
                kwargs.pop("marker")
            p = ax.scatter(
                xs, ys,
                *args,
                color=color, marker="^", label=f"EI({label})",
                **kwargs
            )

        return p
