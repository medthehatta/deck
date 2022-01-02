from svglib.svglib import SvgRenderer
from lxml import etree
from reportlab.graphics import renderPM


def svg_interpolator(path):

    with open(path) as f:
        template = f.read()

    def _interpolate(record):
        svg = template.format(**record)
        return svg_string_to_pil(svg)

    return _interpolate


def file_interpolator(path):

    with open(path) as f:
        template = f.read()

    def _interpolate(record):
        return template.format(**record)

    return _interpolate


def constant_svg(path):
    with open(path) as f:
        svg_data = f.read()
    pil = svg_string_to_pil(svg_data)
    return lambda _: pil


def svg_string_to_pil(svg):
    root = etree.fromstring(svg.encode("utf-8"))
    doc = SvgRenderer("").render(root)
    return renderPM.drawToPIL(doc)

