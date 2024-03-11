"""Unit tests for module `lib.path`."""

from sympy import Matrix, Rational, pi

from lib.path import (
    points_to_segments,
    refined_segments,
    rotate,
    scale,
    segments_to_points,
    shift,
)


points = [
    Matrix([-2, -1]),
    Matrix([2, -1]),
    Matrix([2, 1]),
    Matrix([-2, 1]),
    Matrix([-2, -1]),
]


def test_points_segments_conversion() -> None:
    """Test converting path points to segment vectors and vice versa."""
    segments = points_to_segments(points)
    assert segments == [
        Matrix([4, 0]),
        Matrix([0, 2]),
        Matrix([-4, 0]),
        Matrix([0, -2]),
    ]
    points_back = segments_to_points(segments, points[0])
    assert points_back == points


def test_identity_scaling() -> None:
    """Test whether scaling with factors of unity is an identity operation."""
    scaled = scale(points, (1, 1))
    assert scaled == points


def test_scaling() -> None:
    """Test anisotropic scaling."""
    scaled = scale(points, (Rational(1, 2), 3))
    assert scaled == [
        Matrix([-1, -3]),
        Matrix([1, -3]),
        Matrix([1, 3]),
        Matrix([-1, 3]),
        Matrix([-1, -3]),
    ]


def test_identity_shift() -> None:
    """Test whether shifting with zero offsets is an identity operation."""
    shifted = shift(points, (0, 0))
    assert shifted == points


def test_shift() -> None:
    """Test shift with unequal offsets in each direction."""
    shifted = shift(points, (1, 2))
    assert shifted == [
        Matrix([-1, 1]),
        Matrix([3, 1]),
        Matrix([3, 3]),
        Matrix([-1, 3]),
        Matrix([-1, 1]),
    ]


def test_identity_rotation() -> None:
    """Test whether rotating with zero angle is an identity operation."""
    rotated = rotate(points, 0)
    assert rotated == points


def test_rotation() -> None:
    """Test 90-deg rotation."""
    rotated = rotate(points, pi / 2)
    assert rotated == [
        Matrix([1, -2]),
        Matrix([1, 2]),
        Matrix([-1, 2]),
        Matrix([-1, -2]),
        Matrix([1, -2]),
    ]


def test_identity_refinement() -> None:
    """Test if an identity refinement returns the original segment."""

    def rule(seg: Matrix) -> list[Matrix]:
        return [seg]

    segments = points_to_segments(points)
    assert list(refined_segments(segments, rule)) == segments


def test_division_refinement() -> None:
    """Test a simple refinement rule where the segment is halved."""

    def rule(seg: Matrix) -> list[Matrix]:
        return [seg / 2, seg / 2]

    segments = points_to_segments(points)
    assert list(refined_segments(segments, rule)) == [
        Matrix([2, 0]),
        Matrix([2, 0]),
        Matrix([0, 1]),
        Matrix([0, 1]),
        Matrix([-2, 0]),
        Matrix([-2, 0]),
        Matrix([0, -1]),
        Matrix([0, -1]),
    ]
