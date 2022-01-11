from dataclasses import dataclass
from functools import wraps
from itertools import cycle

from entity_helpers import split_to_multiple_fields
from svg import empty_svg_string
from svg import interpolate_svg_to_string
from util import prefix


relpath = prefix(__file__)


# Use kwargs to configure...
def rows(num_rows):

    # A decorator...
    def _wrapper(func):

        # That returns a function...
        def _wrapped(*args, **kwargs):

            # Which is identical to the wrapped one, if it is already
            # configured with the rows (to prevent breakage if there is
            # accidental double-decoration)
            if hasattr(func, "rows"):
                return func

            # Or which is almost the same...
            else:

                # ...except it:
                # (1) is made into a thunk so it evaluates lazily,
                # (2) the thunk gets a "rows" attribute added to it, saying how
                # many rows tall it is.  Now row_layout() can check the number
                # of rows the function consumes, THEN evaluate it to SVG.
                @wraps(func)
                def _inner():
                    return func(*args, **kwargs)
                _inner.rows = num_rows

                return _inner

        return _wrapped

    return _wrapper


def row_layout(*rows):
    # Config
    layout_template = "row-layout.svg"
    total_rows = 7

    replacements = {}
    current = 0

    used_rows = sum(getattr(row, "rows", 1) for row in rows)

    if used_rows > total_rows:
        raise ValueError(
            f"Too many rows!  Max is {total_rows}, but demanding {used_rows}!"
        )
    else:
        missing = total_rows - used_rows

    # Round-robin the missing rows backward through the fills if present.
    # (Backward so there is more space toward the bottom, meaning more info at
    # the top.)
    # If there are no fills, the empty bottom rows will be left empty.
    if fills := [row for row in rows if hasattr(row, "_is_fill")]:
        fills_backward = cycle(reversed(fills))
        while missing > 0:
            fill = next(fills_backward)
            fill.rows += 1
            missing -= 1

    for row in rows:
        try:
            height = row.rows
        except AttributeError:
            print(f"No height for {row}")
            height = 1
        if height == 0:
            continue
        if not hasattr(row, "_is_fill"):
            replacements[f"row{height}_{current}"] = row()
        current += height

    return interpolate_svg_to_string(
        filepath=relpath(layout_template),
        svg_replacements=replacements,
    )


def fill(n=0):

    def _fill():
        return empty_svg_string()

    _fill._is_fill = True
    _fill.rows = n
    if n:
        _fill.__name__ = f"fill_min_{n}"
    else:
        _fill.__name__ = "fill"

    return _fill


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

