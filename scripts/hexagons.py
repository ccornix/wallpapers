"""Script to generate a wallpaper of randomly colored hexagons."""

__author__ = "ccornix"
__copyright__ = "Copyright (c) 2024 ccornix"
__license__ = "MIT"

from sympy import Rational, sqrt
import random

from lib.grid import generate_grid
from lib.path import scale
from lib.poly import regular_polygon_path
from lib.svg import SVGPathStyle, generate_svg


PALETTE = ["#202020", "#303030", "#404040", "#505050"]


def element_style_fn(ix: int, iy: int) -> list[SVGPathStyle]:
    """Return an SVG path style with a randomly selected fill color."""
    return [
        SVGPathStyle(
            fill_color=PALETTE[random.randrange(1, len(PALETTE))],
            stroke_color=PALETTE[0],
            stroke_width=1,
        )
    ]


if __name__ == "__main__":
    random.seed(1)

    resolution = (1920, 1080)

    ax = 32
    ay = 36
    spacings = (ax, 3 * ay // 4)

    def offsets_fn(ix: int, iy: int) -> tuple[int, int]:
        return (ax // 2 * (iy % 2), 0)

    hexagon = regular_polygon_path(6)

    element_paths = [scale(hexagon, (ax / sqrt(3), Rational(ay, 2)))]

    print(
        generate_svg(
            author=__author__,
            title="Randomly colored hexagons",
            palette=PALETTE,
            background_color=PALETTE[0],
            resolution=resolution,
            paths=generate_grid(
                element_paths=element_paths,
                spacings=spacings,
                offsets_fn=offsets_fn,
                resolution=resolution,
                element_style_fn=element_style_fn,
            ),
        )
    )
