"""Functions to construct Minkowski island fractal curves."""

__author__ = "ccornix"
__copyright__ = "Copyright (C) 2024 ccornix"
__license__ = "MIT"
__all__ = ["minkowski_island"]

from sympy import Matrix

from .functools import repeated
from .path import points_to_segments, segments_to_points, refined_segments
from .poly import regular_polygon_path, rotation_matrix

R_m90 = rotation_matrix(-pi / 4)
R_p90 = rotation_matrix(pi / 4)


def minkowski_rule(segment: Matrix) -> list[Matrix]:
    """Refine a `segment` vector following the Minkowski rule.

    Reference:
    https://en.wikipedia.org/wiki/Minkowski_sausage
    """
    v1 = segment / 4
    v2 = R_p90 * v1
    v3 = 2 * R_m90 * v1
    return [v1, v2, v1, v3, v1, v2, v1]


def minkowski_island(iterations: int) -> list[Matrix]:
    """Return Minkowski island after a given number of `iterations`."""
    points = regular_polygon_path(4)
    segments = points_to_segments(points)
    return segments_to_points(
        list(repeated(refined_segments, iterations, minkowski_rule)(segments)),
        points[0],
    )
