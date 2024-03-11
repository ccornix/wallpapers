"""Functions for construction of polygonal paths."""

__author__ = "ccornix"
__copyright__ = "Copyright (C) 2024 ccornix"
__license__ = "MIT"
__all__ = ["regular_polygon_path", "rotation_matrix"]

from itertools import accumulate, repeat
from sympy import Matrix, pi

from .path import rotation_matrix


def regular_polygon_path(n: int) -> list[Matrix]:
    """Return points of a regular polygonal path with `n` sides."""
    assert n >= 3
    R = rotation_matrix(-2 * pi / n)
    points = list(
        accumulate(repeat(R, n), lambda v, A: A * v, initial=Matrix([0, 1]))
    )
    assert points[0] == Matrix([0, 1])
    assert points[-1] == points[0]
    return points
