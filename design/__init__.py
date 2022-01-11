from dataclasses import dataclass
from functools import wraps

from entity_helpers import split_to_multiple_fields
from svg import empty_svg_string
from svg import interpolate_svg_to_string
from util import prefix


relpath = prefix(__file__)


def rows(num_rows):

    def _wrapper(func):

        @wraps(func)
        def _wrapped(*args, **kwargs):

            def _inner():
                return func(*args, **kwargs)
            _inner.rows = num_rows

            return _inner

        return _wrapped

    return _wrapper


def row_layout(*rows):
    replacements = {}
    current = 0

    for row in rows:
        try:
            height = row.rows
        except AttributeError:
            print(f"No height for {row}")
            height = 1
        replacements[f"row{height}_{current}"] = row()
        current += 1

    return interpolate_svg_to_string(
        filepath=relpath("row-layout.svg"),
        svg_replacements=replacements,
    )


def spacer(n):

    def _spacer():
        return empty_svg_string()

    _spacer.rows = n

    return _spacer


@rows(1)
def centered_text_1(text):
    return interpolate_svg_to_string(
        filepath=relpath("rows-1-centered-text.svg"),
        text_replacements={"center_text": text},
    )


@rows(1)
def centered_multi_text_1(text):
    record = split_to_multiple_fields(
        text,
        field_name="center_text",
        chars_per=55,
        max_lines=3,
    )
    return interpolate_svg_to_string(
        filepath=relpath("rows-1-center-multi-text.svg"),
        text_replacements=record,
    )



@rows(1)
def text_left_right_1(left="", right=""):
    return interpolate_svg_to_string(
        filepath=relpath("rows-1-left-right-text.svg"),
        text_replacements={"left_text": left, "right_text": right},
    )


@rows(1)
def edges_twothirds_1(left=None, middle=None, right=None):
    left = left or empty_svg_string()
    middle = middle or empty_svg_string()
    right = right or empty_svg_string()
    return interpolate_svg_to_string(
        filepath=relpath("rows-1-edges-twothirds.svg"),
        svg_replacements={"r0": left, "r1": middle, "r2": right},
    )


@rows(1)
def five_rects_1(rects):
    replacements = dict(zip((f"r{i}" for i in range(5)), rects))
    return interpolate_svg_to_string(
        filepath=relpath("rows-1-five-rects.svg"),
        svg_replacements=replacements,
    )


def onefifth_centered_text_1(text):
    return interpolate_svg_to_string(
        filepath=relpath("rows-1-onefifth-centered-text.svg"),
        text_replacements={"center_text": text},
    )


def twothirds_centered_text_1(text):
    return interpolate_svg_to_string(
        filepath=relpath("rows-1-twothirds-centered-text.svg"),
        text_replacements={"center_text": text},
    )


@rows(2)
def centered_text_2(text):
    return interpolate_svg_to_string(
        filepath=relpath("rows-2-centered-text.svg"),
        text_replacements={"center_text": text},
    )


@rows(2)
def centered_multi_text_2(text):
    record = split_to_multiple_fields(
        text,
        field_name="center_text",
        chars_per=60,
        max_lines=8,
    )
    return interpolate_svg_to_string(
        filepath=relpath("rows-2-center-multi-text.svg"),
        text_replacements=record,
    )


@rows(2)
def text_left_right_2(left="", right=""):
    return interpolate_svg_to_string(
        filepath=relpath("rows-2-left-right-text.svg"),
        text_replacements={"left_text": left, "right_text": right},
    )


@rows(2)
def five_rects_2(rects):
    replacements = dict(zip((f"r{i}" for i in range(5)), rects))
    return interpolate_svg_to_string(
        filepath=relpath("rows-2-five-rects.svg"),
        svg_replacements=replacements,
    )


@rows(3)
def rect_left_right_3(left, right):
    return interpolate_svg_to_string(
        filepath=relpath("rows-3-left-right-rect.svg"),
        svg_replacements={"r0": left, "r1": right},
    )


@rows(3)
def ten_rects_3(top_rects=None, bottom_rects=None):
    top_rects = top_rects or []
    bottom_rects = bottom_rects or []
    tops = dict(zip((f"r0{i}" for i in range(5)), top_rects))
    bottoms = dict(zip((f"r1{i}" for i in range(5)), bottom_rects))
    replacements = {**tops, **bottoms}
    return interpolate_svg_to_string(
        filepath=relpath("rows-3-ten-rects.svg"),
        svg_replacements=replacements,
    )


def half_multi_text_3(text):
    record = split_to_multiple_fields(
        text,
        field_name="caption",
        chars_per=30,
        max_lines=12,
    )
    return interpolate_svg_to_string(
        filepath=relpath("rows-3-half-multi-text.svg"),
        text_replacements=record,
    )


def half_triple_text_3(top="", middle="", bottom=""):
    record = {
        "top_text": top,
        "mid_text": middle,
        "bot_text": bottom,
    }
    return interpolate_svg_to_string(
        filepath=relpath("rows-3-half-text3.svg"),
        text_replacements=record,
    )

