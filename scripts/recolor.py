"""Helper script to recolor an existing SVG file with custom palette tag."""

import argparse
import pathlib
import re

PALETTE_PATTERN = re.compile(
    r"<ccornix:palette>([#0-9a-fA-F\s]+)<\/ccornix:palette>"
)
COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")


def main() -> None:  # noqa: D103
    args = parse_arguments()
    svg = args.input_file.read_text()
    print(replace_palette(svg, old=extract_palette(svg), new=args.palette))


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Internal script for SVG wallpaper recoloring."
    )
    parser.add_argument(
        "input_file",
        metavar="INPUT_FILE",
        help="input SVG file",
        type=pathlib.Path,
    )
    parser.add_argument(
        "palette",
        metavar="COLOR",
        nargs="*",
        help="HTML color code of a palette color; e.g. #123456",
    )
    return parser.parse_args()


# NOTE: no need to fully parse SVG XML to just get palette colors
#
# def extract_palette(svg: str) -> list[str]:
#     """Return the palette extracted from the custom tag of the SVG code."""
#     from xml.etree import ElementTree
#     tree = ElementTree.fromstring(svg)
#     NS_URL = "https://codeberg.org/ccornix/wallpapers"
#     element = tree.getroot().find(f".//{{{NS_URL}}}palette")
#     palette = element.text.split()
#     assert all(COLOR_PATTERN.match(color) for color in palette)
#     return palette


def extract_palette(svg: str) -> list[str]:
    """Return the palette extracted from the custom tag of the SVG code."""
    match = next(PALETTE_PATTERN.finditer(svg))
    palette = match.group(1).split()
    assert all(COLOR_PATTERN.match(color) for color in palette)
    return palette


def replace_palette(svg: str, old: list[str], new: list[str]) -> str:
    """Replace all colors in the SVG code."""
    if not new:
        return svg
    assert len(new) >= len(old)
    dct = {re.escape(k): v for k, v in zip(old, new)}
    pattern = re.compile("|".join(dct))
    return pattern.sub(lambda match: dct[re.escape(match.group(0))], svg)


if __name__ == "__main__":
    main()
