"""Unit tests for module `lib.grid`."""

from sympy import Matrix

from lib.grid import generate_grid
from lib.path import shift
from lib.svg import SVGPath, SVGPathStyle


rectangle = [
    Matrix([-2, -1]),
    Matrix([2, -1]),
    Matrix([2, 1]),
    Matrix([-2, 1]),
    Matrix([-2, -1]),
]


def test_rectangular_grid() -> None:
    """Test path generation for a 3x3 rectangular grid with seamless style."""

    def element_style_fn(ix, iy):
        return [
            SVGPathStyle(
                fill_color=f"#{str(ix)*6}",
                stroke_color=f"#{str(iy)*6}",
                stroke_width=1,
            )
        ]

    paths = generate_grid(
        element_paths=[rectangle],
        spacings=(4, 2),
        offsets_fn=None,
        resolution=(8, 4),
        element_style_fn=element_style_fn,
    )

    assert paths == [
        # Row 0
        SVGPath(
            points=shift(rectangle, Matrix([0, 0])),
            style=SVGPathStyle(
                fill_color="#000000", stroke_color="#000000", stroke_width=1
            ),
        ),
        SVGPath(
            points=shift(rectangle, Matrix([4, 0])),
            style=SVGPathStyle(
                fill_color="#111111", stroke_color="#000000", stroke_width=1
            ),
        ),
        SVGPath(
            points=shift(rectangle, Matrix([8, 0])),
            style=SVGPathStyle(
                fill_color="#000000", stroke_color="#000000", stroke_width=1
            ),
        ),
        # Row 1
        SVGPath(
            points=shift(rectangle, Matrix([0, 2])),
            style=SVGPathStyle(
                fill_color="#000000", stroke_color="#111111", stroke_width=1
            ),
        ),
        SVGPath(
            points=shift(rectangle, Matrix([4, 2])),
            style=SVGPathStyle(
                fill_color="#111111", stroke_color="#111111", stroke_width=1
            ),
        ),
        SVGPath(
            points=shift(rectangle, Matrix([8, 2])),
            style=SVGPathStyle(
                fill_color="#000000", stroke_color="#111111", stroke_width=1
            ),
        ),
        # Row 2
        SVGPath(
            points=shift(rectangle, Matrix([0, 4])),
            style=SVGPathStyle(
                fill_color="#000000", stroke_color="#000000", stroke_width=1
            ),
        ),
        SVGPath(
            points=shift(rectangle, Matrix([4, 4])),
            style=SVGPathStyle(
                fill_color="#111111", stroke_color="#000000", stroke_width=1
            ),
        ),
        SVGPath(
            points=shift(rectangle, Matrix([8, 4])),
            style=SVGPathStyle(
                fill_color="#000000", stroke_color="#000000", stroke_width=1
            ),
        ),
    ]
