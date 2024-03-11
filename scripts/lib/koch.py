"""Functions to construct Koch island fractal curves."""

__author__ = "ccornix"
__copyright__ = "Copyright (C) 2024 ccornix"
__license__ = "MIT"
__all__ = ["koch_island"]

from sympy import Matrix, pi

from .functools import repeated
from .path import points_to_segments, segments_to_points, refined_segments
from .poly import regular_polygon_path, rotation_matrix

R_m60 = rotation_matrix(-pi / 3)
R_p60 = rotation_matrix(pi / 3)


def koch_rule(segment: Matrix) -> list[Matrix]:
    """Refine a `segment` vector following the Koch island rule.

    Reference:
    https://mathworld.wolfram.com/KochSnowflake.html
    """
    v1 = segment / 3
    v2 = R_p60 * v1
    v3 = R_m60 * v1
    return [v1, v2, v3, v1]


def koch_island(iterations: int) -> list[Matrix]:
    """Return Koch island after a given number of `iterations`."""
    points = regular_polygon_path(3)
    segments = points_to_segments(points)
    return segments_to_points(
        list(repeated(refined_segments, iterations, koch_rule)(segments)),
        points[0],
    )
