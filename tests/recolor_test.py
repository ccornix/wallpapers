"""Unit tests for the recolor script functions."""

from recolor import extract_palette, replace_palette


INPUT_SVG = """\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   width="1920px"
   height="1080px"
   viewBox="0 0 1920 1080"
   version="1.1"
   xmlns="http://www.w3.org/2000/svg">
<metadata xmlns:ccornix="https://codeberg.org/ccornix/wallpapers">
<ccornix:palette>#000000 #777777 #ffffff</ccornix:palette>
</metadata>
<rect width="100%" height="100%" fill="#ffffff"/>
</svg>"""


OUTPUT_SVG = """\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   width="1920px"
   height="1080px"
   viewBox="0 0 1920 1080"
   version="1.1"
   xmlns="http://www.w3.org/2000/svg">
<metadata xmlns:ccornix="https://codeberg.org/ccornix/wallpapers">
<ccornix:palette>#ffffff #777777 #000000</ccornix:palette>
</metadata>
<rect width="100%" height="100%" fill="#000000"/>
</svg>"""


def test_extract_palette() -> None:
    """Test palette extraction from custom SVG metadata tag."""
    assert extract_palette(INPUT_SVG) == ["#000000", "#777777", "#ffffff"]


def test_replace_palette() -> None:
    """Test palette replacement in SVG."""
    obtained = replace_palette(
        INPUT_SVG,
        old=["#000000", "#777777", "#ffffff"],
        new=["#ffffff", "#777777", "#000000"],
    )
    assert obtained == OUTPUT_SVG
