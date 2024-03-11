"""Functions to construct Minkowski island fractal curves."""

__author__ = "ccornix"
__copyright__ = "Copyright (C) 2024 ccornix"
__license__ = "MIT"
__all__ = ["minkowski_island"]

from sympy import Matrix, Rational, pi

from .functools import repeated
from .path import (
    points_to_segments,
    segments_to_points,
    refined_segments,
    rotation_matrix,
)
from .poly import regular_polygon_path, rotation_matrix

R_m90 = rotation_matrix(-pi / 2)

# Transformation: scale edge by 1/sqrt(5) and rotate counter-clockwise by
# arcsin(1/sqrt(5))
T_minkowski = Rational(1, 5) * Matrix([[2, -1], [1, 2]])


def minkowski_rule(segment: Matrix) -> list[Matrix]:
    """Refine a `segment` vector following the Minkowski rule.

    Reference:
    https://en.wikipedia.org/wiki/Minkowski_sausage
    """
    v1 = T_minkowski * segment
    v2 = R_m90 * v1
    return [v1, v2, v1]


def minkowski_island(iterations: int) -> list[Matrix]:
    """Return Minkowski island after a given number of `iterations`."""
    points = regular_polygon_path(4)
    segments = points_to_segments(points)
    return segments_to_points(
        list(repeated(refined_segments, iterations, minkowski_rule)(segments)),
        points[0],
    )
