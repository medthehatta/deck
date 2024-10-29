from pprint import pprint

from coolname import generate_slug
from svgpathtools import svg2paths
from lxml import etree

from svglue2 import Components, svg_string

from svg import svg_string_to_pil

from rect import Rect, Point, Size


def preview(svg, path=None, name=None):
    path = path or "/mnt/c/Users/Med/Desktop/previews"
    name = name or generate_slug(2)
    png_path = f"{path}/{name}.png"
    svg_path = f"{path}/{name}.svg"
    ss = svg_string(svg)
    with open(svg_path, "w") as f:
        f.write(ss)
    return svg_string_to_pil(ss).save(png_path)


import cli
ap = cli.deck_plugins["apogee"]


fire = ap.ability(
    "Fire!",
    provides={"thermal": 10},
    cooldown=1,
    costs={"battery": 5},
    ability_text=(
        "Just shoot at the guy, this is only long because I want to test "
        "the text splitting"
    ),
)


some_kw = ap.keyword("hi")


laser_cannon = ap.module(
    "Laser Cannon",
    "Weapon",
    "Seeker",
    abilities=[fire],
    tier=1,
)


preview(laser_cannon, name="laser-cannon")

