from pprint import pprint

from svgpathtools import svg2paths
from lxml import etree

from svglue2 import Components, svg_string

from svg import svg_string_to_pil

from rect import Rect, Point, Size


def tree_to_foo(tree):
    s = svg_string(tree)
    with open("/mnt/c/Users/Med/Desktop/foo.svg", "w") as f:
        f.write(s)
    svg_string_to_pil(s).save("/mnt/c/Users/Med/Desktop/foo.png")


svg_file = "/mnt/c/Users/Med/Desktop/decks/apogee/ability.svg"


c = Components.from_svg_file(svg_file)

tree = c.instantiate(
    "main",
    svg_replacements={
        "upper": c.instantiate("narrowboi", text_replacements={"text": "sup"}),
        "lower": c.instantiate("narrowboi", text_replacements={"text": "yo"}),
        "icongroup": c.instantiate(
            "icongroup",
            svg_replacements={
                "icon:1": c.instantiate("icon"),
                "icon:2": c.instantiate("icon"),
                "icon:3": c.instantiate("icon"),
            },
        ),
    },
    text_replacements={"some_text": "ehhhhhyyyyyaa"},
)


def rect_row(columns):

    def _(rect):
        return rect.subdivide(rows=1, columns=columns).iter_rows_columns()
    return _


tree2 = c.instantiate(
    "main",
    rect_replacements={
        "icongroup": (rect_row(10), [c.instantiate("icon") for _ in range(4)]),
    },
)

tree_to_foo(tree2)


