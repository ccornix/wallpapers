"""Generator of a seamless grid of path tiles."""

__author__ = "ccornix"
__copyright__ = "Copyright (C) 2024 ccornix"
__license__ = "MIT"
__all__ = ["generate_grid"]

from collections.abc import Callable, Sequence
from operator import add
from sympy import Matrix
from typing import cast

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

    A dict is returned that contains a list of SVG path data and the target
    resolution. This dict can readily be used as keyword arguments to
    `generate_svg()` of the `svg` submodule.
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
                    tuple(map(add, offsets_fn(ix, iy), (ix * dx, iy * dy))),
                ),
            ),
            style=wrapped_style(ix, iy)[ip],
        )
        for iy in range(Ny + 1)
        for ix in range(Nx + 1)
        for ip, element_path in enumerate(element_paths)
    ]
