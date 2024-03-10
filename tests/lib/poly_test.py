"""Unit tests for module `lib.poly`."""

from sympy import Matrix, Rational, sqrt

from lib.poly import regular_polygon_path


def test_triangle() -> None:
    """Test path triangular path generation."""
    assert regular_polygon_path(3) == [
        Matrix([0, 1]),
        Matrix([-sqrt(3) / 2, -Rational(1, 2)]),
        Matrix([sqrt(3) / 2, -Rational(1, 2)]),
        Matrix([0, 1]),
    ]


def test_square() -> None:
    """Test square path generation."""
    assert regular_polygon_path(4) == [
        Matrix([0, 1]),
        Matrix([-1, 0]),
        Matrix([0, -1]),
        Matrix([1, 0]),
        Matrix([0, 1]),
    ]


def test_hexagon() -> None:
    """Test hexagonal path generation."""
    assert regular_polygon_path(6) == [
        Matrix([0, 1]),
        Matrix([-sqrt(3) / 2, Rational(1, 2)]),
        Matrix([-sqrt(3) / 2, -Rational(1, 2)]),
        Matrix([0, -1]),
        Matrix([sqrt(3) / 2, -Rational(1, 2)]),
        Matrix([sqrt(3) / 2, Rational(1, 2)]),
        Matrix([0, 1]),
    ]
