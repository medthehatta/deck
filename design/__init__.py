from dataclasses import dataclass
from functools import wraps
from itertools import cycle

from entity_helpers import split_to_multiple_fields
from svg import empty_svg_string
from svg import interpolate_svg_to_string
from util import prefix


relpath = prefix(__file__)


def fill(n=0):

    def _fill():
        return empty_svg_string()

    _fill.__is_fill = True
    _fill.__size = n
    if n:
        _fill.__name__ = f"fill_min_{n}"
    else:
        _fill.__name__ = "fill"

    return _fill


def __size(obj):
    return getattr(obj, "__size", 1)


def __is_fill(obj):
    return hasattr(obj, "__is_fill")


def distribute(items, size, favor_left=True):
    taken = sum(__size(x) for x in items)
    missing = size - taken

    if missing < 0:
        raise ValueError(
            f"Can only fit {size} items, but demanded {taken}"
        )

    if fills := [x for x in items if __is_fill(x)]:
        fill_order = cycle(reversed(fills)) if favor_left else cycle(fills)
        while missing > 0:
            fill = next(fill_order)
            fill.__size += 1
            missing -= 1

    result = {}
    index = 0
    for item in items:
        if item in fills:
            index += __size(item)
            continue
        else:
            result[index] = item
            index += __size(item)

    return result


def _interpose_fill(items):
    for item in items[:-1]:
        yield item
        yield fill()
    # Don't yield a fill after the last item
    yield items[-1]


def interpose_fill(items):
    return list(_interpose_fill(items))


def row_layout(*rows):
    # Config
    layout_template = "row-layout.svg"
    total_rows = 7

    row_positions = distribute(
        rows,
        size=total_rows,
        # Favor putting elements on earlier rows and blank space on later rows
        favor_left=True,
    )

    replacements = {
        f"row{__size(item)}_{pos}": item()
        for (pos, item) in row_positions.items()
    }

    return interpolate_svg_to_string(
        filepath=relpath(layout_template),
        svg_replacements=replacements,
    )


# Use kwargs to configure...
def rows(num_rows):

    # A decorator...
    def _wrapper(func):

        # That returns a function...
        def _wrapped(*args, **kwargs):

            # Which is identical to the wrapped one, if it is already
            # configured with the rows (to prevent breakage if there is
            # accidental double-decoration)
            if hasattr(func, "__size"):
                return func

            # Or which is almost the same...
            else:

                # ...except it:
                # (1) is made into a thunk so it evaluates lazily,
                # (2) the thunk gets a "__size" attribute added to it, saying
                # how many rows tall it is.  Now row_layout() can check the
                # number of rows the function consumes, THEN evaluate it to
                # SVG.
                @wraps(func)
                def _inner():
                    return func(*args, **kwargs)
                _inner.__size = num_rows

                return _inner

        return _wrapped

    return _wrapper


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
    replacements = {f"r{i}": rect for (i, rect) in rects.items()}
    return interpolate_svg_to_string(
        filepath=relpath("rows-1-five-rects.svg"),
        svg_replacements=replacements,
    )


def five_rects_centered_1(rect_list):
    dist = distribute([fill(), *rect_list, fill()], size=5)
    return five_rects_1(dist)


def five_rects_left_1(rect_list):
    dist = distribute([*rect_list, fill()], size=5)
    return five_rects_1(dist)


def five_rects_right_1(rect_list):
    dist = distribute([fill(), *rect_list], size=5)
    return five_rects_1(dist)


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
    replacements = {f"r{i}": rect for (i, rect) in rects.items()}
    return interpolate_svg_to_string(
        filepath=relpath("rows-2-five-rects.svg"),
        svg_replacements=replacements,
    )


def five_rects_centered_2(rect_list):
    dist = distribute([fill(), *rect_list, fill()], size=5)
    return five_rects_2(dist)


def five_rects_left_2(rect_list):
    dist = distribute([*rect_list, fill()], size=5)
    return five_rects_2(dist)


def five_rects_right_2(rect_list):
    dist = distribute([fill(), *rect_list], size=5)
    return five_rects_2(dist)


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

