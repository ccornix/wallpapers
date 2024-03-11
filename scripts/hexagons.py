"""Script to generate a wallpaper of randomly colored hexagons."""

__author__ = "ccornix"
__copyright__ = "Copyright (c) 2024 ccornix"
__license__ = "MIT"

from sympy import sqrt
import random

from lib.grid import generate_grid, make_random_color_element_style_fn
from lib.path import scale
from lib.poly import regular_polygon_path
from lib.svg import generate_svg


PALETTE = ["#202020", "#303030", "#404040", "#505050"]
RESOLUTION = (1920, 1080)
CELL_SIZE = (32, 36)
SPACINGS = (CELL_SIZE[0], 3 * CELL_SIZE[1] // 4)
ISLE = regular_polygon_path(6)
ELEMENT_PATHS = [scale(ISLE, (CELL_SIZE[0] / sqrt(3), CELL_SIZE[1] // 2))]


def offsets_fn(ix: int, iy: int) -> tuple[int, int]:
    """Shift each odd row of the hexagonal grid."""
    return (CELL_SIZE[0] // 2 * (iy % 2), 0)


element_style_fn = make_random_color_element_style_fn(
    fill_color=PALETTE[1:],
    stroke_color=PALETTE[0],
    stroke_width=1,
)


def main() -> None:  # noqa: D103
    random.seed(1)
    print(
        generate_svg(
            author=__author__,
            title="Randomly colored hexagons",
            palette=PALETTE,
            background_color=PALETTE[0],
            resolution=RESOLUTION,
            paths=generate_grid(
                element_paths=ELEMENT_PATHS,
                spacings=SPACINGS,
                offsets_fn=offsets_fn,
                resolution=RESOLUTION,
                element_style_fn=element_style_fn,
            ),
        )
    )


if __name__ == "__main__":
    main()
