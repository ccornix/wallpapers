"""Functions for transforming points of paths with straight line segments."""

__author__ = "ccornix"
__copyright__ = "Copyright (C) 2024 ccornix"
__license__ = "MIT"
__all__ = [
    "points_to_segments",
    "refined_segments",
    "rotate",
    "rotation_matrix",
    "scale",
    "segments_to_points",
    "shift",
]

from collections.abc import Callable, Iterable, Sequence
from itertools import accumulate, chain, pairwise
from sympy import Matrix, cos, shape, sin
import operator

from .typing import TNum


def points_to_segments(points: Sequence[Matrix]) -> list[Matrix]:
    """Return segment vectors from path point coordinates."""
    assert all(_is_2d_vector(v) for v in points)
    return [x1 - x0 for x0, x1 in pairwise(points)]


def segments_to_points(
    segments: Sequence[Matrix], initial_point: Matrix
) -> list[Matrix]:
    """Construct path points from segment vectors and an initial point."""
    assert all(_is_2d_vector(v) for v in segments)
    return list(accumulate(segments, operator.add, initial=initial_point))


def scale(
    points: Sequence[Matrix], factors: tuple[TNum, TNum]
) -> list[Matrix]:
    """Scale path points anisotropically with given factors."""
    assert all(_is_2d_vector(v) for v in points)
    sx, sy = factors
    S = Matrix([[sx, 0], [0, sy]])
    return [S * v for v in points]


def shift(
    points: Sequence[Matrix], offsets: tuple[TNum, TNum]
) -> list[Matrix]:
    """Shift path points by given offsets."""
    assert all(_is_2d_vector(v) for v in points)
    d = Matrix(offsets)
    return [v + d for v in points]


def rotate(points: Sequence[Matrix], theta: TNum) -> list[Matrix]:
    """Rotate path points by given angle.

    The angle `theta` of rotation is expected in radians.
    """
    assert all(_is_2d_vector(v) for v in points)
    R = rotation_matrix(theta)
    return [R * v for v in points]


def rotation_matrix(theta: TNum) -> Matrix:
    """Return a rotation matrix.

    The angle `theta` of rotation is expected in radians.
    """
    c, s = cos(theta), sin(theta)
    return Matrix([[c, -s], [s, c]])


def refined_segments(
    segments: Iterable[Matrix], rule: Callable[..., Iterable[Matrix]]
) -> Iterable[Matrix]:
    """Return an iterator over path `segments` refined according to `rule`.

    Function `rule` is expected to return an iterable of refined line segment
    vectors.
    """
    return chain.from_iterable(rule(segment) for segment in segments)


def _is_2d_vector(obj) -> bool:
    return isinstance(obj, Matrix) and shape(obj) == (2, 1)
