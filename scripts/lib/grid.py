"""Generator of a seamless grid of path tiles."""

__author__ = "ccornix"
__copyright__ = "Copyright (C) 2024 ccornix"
__license__ = "MIT"
__all__ = ["generate_grid", "make_random_color_element_style_fn"]

from collections.abc import Callable, Sequence
from sympy import Matrix
from typing import cast
import operator
import random

from .path import shift
from .svg import SVGPath, SVGPathStyle
from .typing import TNum


def generate_grid(
    *,
    element_paths: Sequence[Sequence[Matrix]],
    spacings: tuple[int, int],
    offsets_fn: Callable[[int, int], tuple[TNum, TNum]] | None,
    resolution: tuple[int, int],
    element_style_fn: Callable[[int, int], list[SVGPathStyle]],
) -> list[SVGPath]:
    """Generate a whole grid of SVG paths.

    The path(s) for a single element in the grid is (are) passed through
    `element_paths`, which is then cloned and layed out with given `spacings`.
    Function `offests_fn` may define an index-dependent offset, which can be
    used, for instance, to define a hexagonal grid with alternating horizontal
    row offsets. The `resolution` of the target image is used to estimate how
    many times elements needs to be repeated in the horizontal and vertical
    directions. Finally, `element_style_fn` enables one to define an
    index-dependent style for each path of a cell.

    A list of SVG path data is returned.
    """
    dx, dy = spacings
    w, h = resolution
    assert w % dx == 0 and h % dy == 0
    Nx, Ny = w // dx, h // dy

    offsets_fn = offsets_fn or (lambda ix, iy: (0, 0))

    edge_style_cache: dict[tuple[int, int], list[SVGPathStyle]] = {}

    def wrapped_style(ix: int, iy: int) -> list[SVGPathStyle]:
        jx = ix % Nx
        jy = iy % Ny
        try:
            style = edge_style_cache[jx, jy]
        except KeyError:
            style = element_style_fn(jx, jy)
            if jx == 0 or jy == 0:
                edge_style_cache[jx, jy] = style
        return style

    return [
        SVGPath(
            points=shift(
                element_path,
                # HACK: https://github.com/python/mypy/issues/7509
                cast(
                    tuple[TNum, TNum],
                    tuple(
                        map(
                            operator.add,
                            offsets_fn(ix, iy),
                            (ix * dx, iy * dy),
                        )
                    ),
                ),
            ),
            style=wrapped_style(ix, iy)[ip],
        )
        for iy in range(Ny + 1)
        for ix in range(Nx + 1)
        for ip, element_path in enumerate(element_paths)
    ]


def make_random_color_element_style_fn(
    fill_color: str | Sequence[str],
    stroke_color: str | Sequence[str],
    stroke_width: int,
    stroke_linecap: str = "square",
    count: int = 1,
) -> Callable[[int, int], list[SVGPathStyle]]:
    """Make an element style factory function for `count` number of paths.

    If `fill_color` is a sequence of colors, a random color is chosen from the
    sequence. The same applies for `stroke_color`.
    """

    def make_element_styles(ix: int, iy: int) -> list[SVGPathStyle]:
        """Return SVG path styles with a randomly selected fill color."""
        return [
            SVGPathStyle(
                fill_color=(
                    fill_color
                    if isinstance(fill_color, str)
                    else random.choice(fill_color)
                ),
                stroke_color=(
                    stroke_color
                    if isinstance(stroke_color, str)
                    else random.choice(stroke_color)
                ),
                stroke_width=stroke_width,
                stroke_linecap=stroke_linecap,
            )
            for _ in range(count)
        ]

    return make_element_styles
