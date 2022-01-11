from svglib.svglib import SvgRenderer
from lxml import etree
from reportlab.graphics import renderPM

from svglue import render_svg_string


def svg_interpolator(path):

    with open(path) as f:
        template = f.read()

    def _interpolate(record):
        svg = template.format(**record)
        return svg_string_to_pil(svg)

    return _interpolate


def file_svg_interpolator(path):
    """Like file_interpolator, but inserts entire SVGs instead of strings."""

    def _interpolate(record):
        return render_svg_string(file=path, replacements=record)

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


def interpolate_svg_to_string(
    filepath=None,
    string=None,
    text_replacements=None,
    svg_replacements=None,
):
    if not filepath and not string:
        raise TypeError("Need to provide either 'filepath' or 'string'")

    if filepath and not string:
        with open(filepath, "r") as f:
            string = f.read()

    text_interpolated_string = string.format(**text_replacements)
    return render_svg_string(
        src=text_interpolated_string.encode("utf-8"),
        replacements=svg_replacements,
    )


def interpolate_svg(
    filepath=None,
    string=None,
    text_replacements=None,
    svg_replacements=None,
):
    return svg_string_to_pil(
        interpolate_svg_to_string(
            filepath=filepath,
            string=string,
            text_replacements=text_replacements,
            svg_replacements=svg_replacements,
        )
    )


def svg_string_to_pil(svg):
    root = etree.fromstring(svg.encode("utf-8"))
    doc = SvgRenderer("").render(root)
    return renderPM.drawToPIL(doc)
