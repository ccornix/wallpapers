"""Dataclasses and functions for SVG generation."""

__author__ = "ccornix"
__copyright__ = "Copyright (c) 2024 ccornix"
__license__ = "MIT"
__all__ = ["SVGPathStyle", "SVGPath", "generate_svg"]

from dataclasses import dataclass
from collections.abc import Sequence
from sympy import Matrix
import re

COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")


@dataclass(kw_only=True)
class SVGPathStyle:
    """Style parameters of an SVG path."""

    stroke_width: int
    stroke_linecap: str = "square"
    stroke_color: str
    fill_color: str

    def __post_init__(self) -> None:
        """Perform additional checks at run-time."""
        assert isinstance(self.stroke_width, int)
        assert self.stroke_linecap in ("butt", "round", "square")
        assert COLOR_PATTERN.match(self.stroke_color)
        assert COLOR_PATTERN.match(self.fill_color)

    def __str__(self) -> str:
        """Return an SVG XML string representation of the style."""
        return (
            f"fill:{self.fill_color};"
            f"stroke:{self.stroke_color};"
            f"stroke-width:{self.stroke_width};"
            f"stroke-linecap:{self.stroke_linecap}"
        )


@dataclass(kw_only=True)
class SVGPath:
    """Representation of an SVG path."""

    points: list[Matrix]
    style: SVGPathStyle

    def __str__(self) -> str:
        """Return an SVG XML string representation."""
        is_closed = self.points[-1] == self.points[0]
        if is_closed:
            points = self.points[:-1]
            suffix = " z"
        else:
            points = self.points
            suffix = ""
        points_str = " ".join(f"{float(p[0])},{float(p[1])}" for p in points)
        return f'<path style="{str(self.style)}" d="M {points_str}{suffix}"/>'


def generate_svg(
    *,
    author: str,
    title: str,
    palette: Sequence[str],
    background_color: str,
    paths: Sequence[SVGPath],
    resolution: tuple[int, int],
) -> str:
    """Generate the SVG code of the wallpaper.

    Include metadata such as `author`, `title` and `palette`. The latter is a
    sequence of HTML color codes that includes `background_color` and all
    other colors appearing in the SVG graphics. It is included in a custom XML
    tag to facilitate quick optional posterior re-coloring by switching the
    palette.

    A sequence of SVG paths that compose the wallpaper are contained in
    `paths`. The desired nominal resolution of the SVG in pixels is given by
    `resolution`. This is independent of the final PNG resolution that can be a
    multiple of this nominal one.
    """
    assert all(COLOR_PATTERN.match(color) for color in palette)
    assert COLOR_PATTERN.match(background_color)
    assert background_color in palette
    assert all(
        path.style.fill_color in palette and path.style.stroke_color in palette
        for path in paths
    )
    width, height = resolution
    palette_str = " ".join(palette)
    paths_str = "\n".join(str(path) for path in paths)
    return SVG_TEMPLATE.format(**locals())


SVG_TEMPLATE = """\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   width="{width}px"
   height="{height}px"
   viewBox="0 0 {width} {height}"
   version="1.1"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:dc="http://purl.org/dc/elements/1.1/">
<title property="dc:title">{title}</title>
<desc property="dc:creator">{author}</desc>
<metadata xmlns:ccornix="https://codeberg.org/ccornix/wallpapers">
<ccornix:palette>{palette_str}</ccornix:palette>
</metadata>
<rect width="100%" height="100%" fill="{background_color}"/>
{paths_str}
</svg>"""
