"""Script to generate a wallpaper of randomly colored Koch islands."""

__author__ = "ccornix"
__copyright__ = "Copyright (c) 2024 ccornix"
__license__ = "MIT"

from sympy import Rational, pi, sqrt
import random

from lib.koch import koch_island
from lib.grid import generate_grid, make_random_color_element_style_fn
from lib.path import scale, shift, rotate
from lib.svg import generate_svg


PALETTE = ["#202020", "#303030", "#404040", "#505050"]
RESOLUTION = (1920, 1080)
CELL_SIZE = (64, 72)
SPACINGS = (2 * CELL_SIZE[0], CELL_SIZE[1] // 2)
ISLE = koch_island(iterations=3)
BIG_ISLE = scale(ISLE, (CELL_SIZE[0] / sqrt(3), CELL_SIZE[1] // 2))
SMALL_ISLE = scale(
    rotate(ISLE, pi / 6),
    (Rational(1, 3) * CELL_SIZE[0], Rational(1, 2) / sqrt(3) * CELL_SIZE[1]),
)
BIG_ELEMENT_PATHS = [BIG_ISLE]
SMALL_ELEMENT_PATHS = [
    shift(SMALL_ISLE, (-CELL_SIZE[0] * Rational(2, 3), 0)),
    shift(SMALL_ISLE, (CELL_SIZE[0] * Rational(2, 3), 0)),
]


def offsets_fn(ix: int, iy: int) -> tuple[int, int]:
    """Shift each odd row."""
    return (CELL_SIZE[0] * (iy % 2), 0)


big_element_style_fn = make_random_color_element_style_fn(
    fill_color=PALETTE[1:],
    stroke_color=PALETTE[0],
    stroke_width=1,
)


small_element_style_fn = make_random_color_element_style_fn(
    fill_color=PALETTE[1:],
    stroke_color=PALETTE[0],
    stroke_width=1,
    count=2,
)


def main() -> None:  # noqa: D103
    random.seed(1)
    print(
        generate_svg(
            author=__author__,
            title="Randomly colored Koch islands",
            palette=PALETTE,
            background_color=PALETTE[0],
            resolution=RESOLUTION,
            paths=(
                generate_grid(
                    element_paths=BIG_ELEMENT_PATHS,
                    spacings=SPACINGS,
                    offsets_fn=offsets_fn,
                    resolution=RESOLUTION,
                    element_style_fn=big_element_style_fn,
                )
                + generate_grid(
                    element_paths=SMALL_ELEMENT_PATHS,
                    spacings=SPACINGS,
                    offsets_fn=offsets_fn,
                    resolution=RESOLUTION,
                    element_style_fn=small_element_style_fn,
                )
            ),
        )
    )


if __name__ == "__main__":
    main()
