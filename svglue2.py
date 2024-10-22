from uuid import uuid4
from copy import deepcopy

from lxml import etree
from svgpathtools import svg2paths

from rect import Rect
from rect import Point
from rect import Size


SVG_NS = "http://www.w3.org/2000/svg"
INKSCAPE_NS = "http://www.inkscape.org/namespaces/inkscape"


namespaces = {
    "svg": "http://www.w3.org/2000/svg",
    "inkscape": "http://www.inkscape.org/namespaces/inkscape"
}


class Components:

    def __init__(self, tpls, prefix):
        self.tpls = tpls
        self.prefix = prefix

    @classmethod
    def from_svg_file(cls, path, prefix="deck", bbox_label="bbox"):
        with open(path) as f:
            svgtree = etree.parse(f)
        (paths, attrs) = svg2paths(path)
        bboxes = {
            atr["id"]: p.bbox()
            for (p, atr) in zip(paths, attrs)
        }

        components = svgtree.xpath(
            (
                f"//svg:g[@inkscape:groupmode='layer' and "
                f"@inkscape:label[starts-with(., '{prefix}:')]]"
            ),
            namespaces=namespaces,
        )

        tpls = {}
        for component in components:
            raw_name = component.xpath("@inkscape:label", namespaces=namespaces)[0]
            name = raw_name.replace(f"{prefix}:", "")
            bbox_rect_matches = component.xpath(
                f"svg:rect[@inkscape:label='{prefix}:{bbox_label}']",
                namespaces=namespaces,
            )
            if not bbox_rect_matches:
                raise ValueError(f"Could not find bbox rect in component {name}")
            elif len(bbox_rect_matches) > 1:
                match_s = " ".join(b.attrib["id"] for b in bbox_rect_matches)
                raise ValueError(f"Found multiple bbox rects in component {name}: {match_s}")
            bbox_rect = bbox_rect_matches[0]
            bbox_rect.getparent().remove(bbox_rect)
            bbox = bboxes[bbox_rect.attrib["id"]]
            (minx, maxx, miny, maxy) = bbox
            width = maxx - minx + 1
            height = maxy - miny + 1
            props = {
                "viewBox": f"{minx} {miny} {width} {height}",
                "width": str(width),
                "height": str(height),
            }
            tpls[name] = etree.Element("svg", props)
            # Remove from outer svg
            component.getparent().remove(component)
            # Add to this new svg
            tpls[name].append(component)

        return cls(tpls=tpls, prefix=prefix)

    def instantiate(
        self,
        tpl,
        text_replacements=None,
        svg_replacements=None,
        rect_replacements=None,
    ):
        text_replacements = text_replacements or {}
        svg_replacements = svg_replacements or {}
        rect_replacements = rect_replacements or {}

        tree = deepcopy(self.tpls[tpl])

        for (s, r) in svg_replacements.items():
            found = tree.xpath(f"//svg:rect[@inkscape:label='{self.prefix}:{s}']", namespaces=namespaces)
            for f in found:
                p = f.getparent()
                r.attrib["width"] = f.attrib["width"]
                r.attrib["height"] = f.attrib["height"]
                r.attrib["x"] = f.attrib["x"]
                r.attrib["y"] = f.attrib["y"]
                p.remove(f)
                p.append(r)

        for (t, r) in text_replacements.items():
            found = tree.xpath(f"//svg:tspan[text()[contains(., '{{{t}}}')]]", namespaces=namespaces)
            for f in found:
                f.text = f.text.format(**text_replacements)

        for (outer, (repl_func, svgs)) in rect_replacements.items():
            found = tree.xpath(f"//svg:rect[@inkscape:label='{self.prefix}:{outer}']", namespaces=namespaces)
            for f in found:
                p = f.getparent()
                f_rect = Rect.from_anchor_size(
                    "topleft",
                    Point(float(f.attrib["x"]), float(f.attrib["y"])),
                    Size(float(f.attrib["width"]), float(f.attrib["height"])),
                )
                p.remove(f)
                rect_seq = repl_func(f_rect)
                for (inner, svg) in zip(rect_seq, svgs):
                    svg.attrib["width"] = str(inner.width)
                    svg.attrib["height"] = str(inner.height)
                    svg.attrib["x"] = str(inner.anchor("topleft").x)
                    svg.attrib["y"] = str(inner.anchor("topleft").y)
                    p.append(svg)

        # Walk the tree and reset all the ids
        with_ids = tree.xpath("//*[@id]", namespaces=namespaces)
        for with_id in with_ids:
            with_id.attrib["id"] = str(uuid4())

        return tree


def svg_string(tree):
    return etree.tostring(tree, encoding=str)
    # svgtree.getroot().append(tree)
    # return etree.tostring(svgtree, encoding=str)
