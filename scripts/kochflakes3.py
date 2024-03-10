"""Script to generate a wallpaper of randomly colored Koch islands."""

__author__ = "ccornix"
__copyright__ = "Copyright (c) 2024 ccornix"
__license__ = "MIT"

from sympy import Rational, pi, sqrt
from typing import Callable
import random

from lib.koch import koch_island
from lib.grid import generate_grid
from lib.path import scale, shift, rotate
from lib.svg import SVGPathStyle, generate_svg


PALETTE = ["#202020", "#303030", "#404040", "#505050"]


def make_element_style_fn(
    count: int,
) -> Callable[[int, int], list[SVGPathStyle]]:
    """Make an element style factory function for `count` number of elements.

    Return a function that produces a list of `count` number of SVG path
    styles with a randomly selected fill color.
    """

    def element_style_fn(ix: int, iy: int) -> list[SVGPathStyle]:
        return [
            SVGPathStyle(
                fill_color=PALETTE[random.randrange(1, len(PALETTE))],
                stroke_color=PALETTE[0],
                stroke_width=1,
            )
            for _ in range(count)
        ]

    return element_style_fn


if __name__ == "__main__":
    random.seed(1)

    resolution = (1920, 1080)

    ax = 64
    ay = 72
    spacings = (2 * ax, ay // 2)

    def offsets_fn(ix: int, iy: int) -> tuple[int, int]:
        return (ax * (iy % 2), 0)

    koch_isle = koch_island(iterations=3)

    big = scale(koch_isle, (ax / sqrt(3), Rational(1, 2) * ay))
    big_element_paths = [big]
    big_element_style_fn = make_element_style_fn(1)

    small = scale(
        rotate(koch_isle, pi / 6),
        (Rational(1, 3) * ax, Rational(1, 2) / sqrt(3) * ay),
    )
    small_element_paths = [
        shift(small, (-ax * Rational(2, 3), 0)),
        shift(small, (ax * Rational(2, 3), 0)),
    ]
    small_element_style_fn = make_element_style_fn(2)

    print(
        generate_svg(
            author=__author__,
            title="Randomly colored Koch islands",
            palette=PALETTE,
            background_color=PALETTE[0],
            resolution=resolution,
            paths=(
                generate_grid(
                    element_paths=big_element_paths,
                    spacings=spacings,
                    offsets_fn=offsets_fn,
                    resolution=resolution,
                    element_style_fn=big_element_style_fn,
                )
                + generate_grid(
                    element_paths=small_element_paths,
                    spacings=spacings,
                    offsets_fn=offsets_fn,
                    resolution=resolution,
                    element_style_fn=small_element_style_fn,
                )
            ),
        )
    )
