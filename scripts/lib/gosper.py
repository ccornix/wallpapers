"""Functions to construct Gosper island fractal curves."""

__author__ = "ccornix"
__copyright__ = "Copyright (C) 2024 ccornix"
__license__ = "MIT"
__all__ = ["gosper_island"]

from sympy import Matrix, Rational, sqrt, eye

from .functools import repeated
from .path import points_to_segments, segments_to_points, refined_segments
from .poly import regular_polygon_path


# Transformation: scale edge by 1/sqrt(7) and rotate counter-clockwise by
# arcsin(sqrt(3)/(2*sqrt(7)))
T_gosper = Rational(1, 14) * Matrix([[5, -sqrt(3)], [sqrt(3), 5]])


def gosper_rule(segment: Matrix) -> list[Matrix]:
    """Refine a `segment` vector following the Gosper island rule.

    Reference:
    https://larryriddle.agnesscott.org/ifs/ksnow/flowsnake.htm
    """
    v1 = T_gosper * segment
    v2 = (eye(2) - 2 * T_gosper) * segment
    return [v1, v2, v1]


def gosper_island(iterations: int) -> list[Matrix]:
    """Return Gosper island after a given number of `iterations`."""
    points = regular_polygon_path(6)
    segments = points_to_segments(points)
    return segments_to_points(
        list(repeated(refined_segments, iterations, gosper_rule)(segments)),
        points[0],
    )
