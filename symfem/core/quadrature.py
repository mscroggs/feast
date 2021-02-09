"""Quadrature definitions."""

import sympy
from ..core.symbolic import one, zero


def gll_points(N):
    """Get Gauss-Lobatto-Legendre points.

    Parameters
    ----------
    N : int
        Number of points
    """
    if N == 2:
        return [zero, one]
    if N == 3:
        return [zero, sympy.Rational(1, 2), one]
    if N == 4:
        return [zero, (1 - 1 / sympy.sqrt(5)) / 2, (1 + 1 / sympy.sqrt(5)) / 2, one]
    if N == 5:
        return [zero, (1 - sympy.sqrt(3) / sympy.sqrt(7)) / 2, sympy.Rational(1, 2),
                (1 + sympy.sqrt(3) / sympy.sqrt(7)) / 2, one]
    if N == 6:
        return [zero,
                (1 - sympy.sqrt(sympy.Rational(1, 3) + (2 * sympy.sqrt(7) / 21))) / 2,
                (1 - sympy.sqrt(sympy.Rational(1, 3) - (2 * sympy.sqrt(7) / 21))) / 2,
                (1 + sympy.sqrt(sympy.Rational(1, 3) - (2 * sympy.sqrt(7) / 21))) / 2,
                (1 + sympy.sqrt(sympy.Rational(1, 3) + (2 * sympy.sqrt(7) / 21))) / 2,
                one]
    if N == 7:
        return [zero,
                (1 - sympy.sqrt((5 + 2 * sympy.sqrt(5) / sympy.sqrt(3)) / 11)) / 2,
                (1 - sympy.sqrt((5 - 2 * sympy.sqrt(5) / sympy.sqrt(3)) / 11)) / 2,
                sympy.Rational(1, 2),
                (1 + sympy.sqrt((5 - 2 * sympy.sqrt(5) / sympy.sqrt(3)) / 11)) / 2,
                (1 + sympy.sqrt((5 + 2 * sympy.sqrt(5) / sympy.sqrt(3)) / 11)) / 2,
                one]
    raise NotImplementedError()


def gll_weights(N):
    """Get Gauss-Lobatto-Legendre weights.

    Parameters
    ----------
    N : int
        Number of points
    """
    if N == 2:
        return [sympy.Rational(1, 2), sympy.Rational(1, 2)]
    if N == 3:
        return [sympy.Rational(1, 6), sympy.Rational(2, 3), sympy.Rational(1, 6)]
    if N == 4:
        return [sympy.Rational(1, 12), sympy.Rational(5, 12), sympy.Rational(5, 12),
                sympy.Rational(1, 12)]
    if N == 5:
        return [sympy.Rational(1, 20), sympy.Rational(49, 180), sympy.Rational(16, 45),
                sympy.Rational(49, 180), sympy.Rational(1, 20)]
    if N == 6:
        return [sympy.Rational(1, 30), (14 - sympy.sqrt(7)) / 60, (14 + sympy.sqrt(7)) / 60,
                (14 + sympy.sqrt(7)) / 60, (14 - sympy.sqrt(7)) / 60, sympy.Rational(1, 30)]
    if N == 7:
        return [sympy.Rational(1, 42),
                (124 - 7 * sympy.sqrt(15)) / 700,
                (124 + 7 * sympy.sqrt(15)) / 700,
                sympy.Rational(128, 525),
                (124 + 7 * sympy.sqrt(15)) / 700,
                (124 - 7 * sympy.sqrt(15)) / 700,
                sympy.Rational(1, 42)]
    raise NotImplementedError()