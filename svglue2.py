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

    def __init__(self, tpls):
        self.tpls = tpls

    @classmethod
    def from_svg_file(cls, path):
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
                f"@inkscape:label[starts-with(., '=')]]"
            ),
            namespaces=namespaces,
        )

        tpls = {}
        for component in components:
            raw_name = component.xpath("@inkscape:label", namespaces=namespaces)[0]
            name = raw_name.lstrip("=!")
            bbox_rect_matches = component.xpath(
                f"svg:rect[@inkscape:label='=' or @inkscape:label='=!']",
                namespaces=namespaces,
            )
            if not bbox_rect_matches:
                raise ValueError(f"Could not find bbox rect in component {name}")
            elif len(bbox_rect_matches) > 1:
                match_s = " ".join(b.attrib["id"] for b in bbox_rect_matches)
                raise ValueError(f"Found multiple bbox rects in component {name}: {match_s}")
            bbox_rect = bbox_rect_matches[0]
            if not bbox_rect.attrib[f"{{{INKSCAPE_NS}}}label"].startswith("=!"):
                bbox_rect.getparent().remove(bbox_rect)
            else:
                bbox_rect.attrib[f"{{{INKSCAPE_NS}}}label"] = ""
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
            # Remove the transform attr, the "parent" document is no longer
            # relevant
            component.attrib["transform"] = ""
            # Remove from outer svg
            component.getparent().remove(component)
            # Add to this new svg
            tpls[name].append(component)

        return cls(tpls=tpls)

    def inst(self, tpl, replacements=None):
        replacements = replacements or {}

        text_replacements = {}
        svg_replacements = {}
        rect_replacements = {}

        for (pholder, repl) in replacements.items():
            match repl:

                case str() as text:
                    text_replacements[pholder] = text

                case int() as text:
                    text_replacements[pholder] = str(text)

                case float() as text:
                    text_replacements[pholder] = str(text)

                case list() as seq:
                    for (i, interp) in enumerate(seq, start=1):
                        if isinstance(interp, str):
                            text_replacements[f"{pholder}#{i}"] = interp
                        else:
                            svg_replacements[f"{pholder}#{i}"] = interp

                case (rect_func, list() as rect_list):
                    rect_replacements[pholder] = (rect_func, rect_list)

                case svg:
                    svg_replacements[pholder] = svg

        return self.instantiate(
            tpl,
            text_replacements,
            svg_replacements,
            rect_replacements,
        )

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
            found = tree.xpath(f"//svg:rect[@inkscape:label='={s}']", namespaces=namespaces)
            for f in found:
                p = f.getparent()
                r.attrib["width"] = f.attrib["width"]
                r.attrib["height"] = f.attrib["height"]
                r.attrib["x"] = f.attrib["x"]
                r.attrib["y"] = f.attrib["y"]
                if "transform" in f.attrib:
                    r.attrib["transform"] = f.attrib["transform"]
                p.remove(f)
                p.append(r)

        for (t, r) in text_replacements.items():
            found = tree.xpath(
                f"//svg:tspan[text()[contains(., '{{{t}}}')]]",
                namespaces=namespaces,
            )
            for f in found:
                f.text = f.text.format(**text_replacements)

        for (outer, (repl_func, svgs)) in rect_replacements.items():
            found = tree.xpath(
                f"//svg:rect[@inkscape:label='={outer}']",
                namespaces=namespaces,
            )
            for f in found:
                p = f.getparent()
                f_rect = Rect.from_anchor_size(
                    "topleft",
                    Point(float(f.attrib["x"]), float(f.attrib["y"])),
                    Size(float(f.attrib["width"]), float(f.attrib["height"])),
                )
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

        # Remove anything with a label that begins with `=`, that was a
        # placeholder
        placeholders = tree.xpath(
            "//svg:rect[@inkscape:label[starts-with(., '=')]]",
            namespaces=namespaces,
        )
        for p in placeholders:
            p.getparent().remove(p)

        return tree


def svg_string(tree):
    return etree.tostring(tree, encoding=str)
