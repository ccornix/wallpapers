"""Unit tests for module `lib.svg`."""

from sympy import Matrix

from lib.svg import SVGPath, SVGPathStyle, generate_svg


expected_svg = """\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   width="200px"
   height="100px"
   viewBox="0 0 200 100"
   version="1.1"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:dc="http://purl.org/dc/elements/1.1/">
<title property="dc:title">title</title>
<desc property="dc:creator">author</desc>
<metadata xmlns:ccornix="ccornix/wallpapers">
<ccornix:palette>#000000 #ffffff</ccornix:palette>
</metadata>
<rect width="100%" height="100%" fill="#000000"/>
<!-- Flip the y axis and move the origin to the bottom left corner -->
<g transform="translate(0,100) scale(1,-1)">
<path style="fill:#000000;stroke:#ffffff;stroke-width:1;stroke-linecap:square" d="M -2.0,-1.0 2.0,-1.0 2.0,1.0 -2.0,1.0 z"/>
</g>
</svg>"""  # noqa: E501


def test_svg_generation() -> None:
    """Test SVG code generation featuring a single rectangular path."""
    svg = generate_svg(
        author="author",
        title="title",
        palette=["#000000", "#ffffff"],
        background_color="#000000",
        paths=[
            SVGPath(
                points=[
                    Matrix([-2, -1]),
                    Matrix([2, -1]),
                    Matrix([2, 1]),
                    Matrix([-2, 1]),
                    Matrix([-2, -1]),
                ],
                style=SVGPathStyle(
                    fill_color="#000000",
                    stroke_color="#ffffff",
                    stroke_width=1,
                ),
            )
        ],
        resolution=(200, 100),
    )
    assert svg == expected_svg
