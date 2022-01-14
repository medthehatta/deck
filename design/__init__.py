from dataclasses import dataclass
from functools import wraps
from itertools import cycle

from entity_helpers import split_to_multiple_fields
from svg import empty_svg_string
from svg import interpolate_svg_to_string
from util import prefix


relpath = prefix(__file__)


def __size(obj):
    if isinstance(obj, Sized):
        return obj.size
    else:
        return 1


def __is_fill(obj):
    return isinstance(obj, Fill)


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
            fill.size += 1
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


class Sized:

    def __init__(self, inner, size=1):
        self.size = size
        if isinstance(inner, type(self)):
            self.inner = inner.inner
        else:
            self.inner = inner


class Fill(Sized):

    def __init__(self, size=0):
        self.size = size
        self.inner = None


def fill(n=0):
    return Fill(size=n)


def centered_text_1(text):
    return interpolate_svg_to_string(
        filepath=relpath("rows-1-centered-text.svg"),
        text_replacements={"center_text": text},
    )


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



def text_left_right_1(left="", right=""):
    return interpolate_svg_to_string(
        filepath=relpath("rows-1-left-right-text.svg"),
        text_replacements={"left_text": left, "right_text": right},
    )


def edges_twothirds_1(left=None, middle=None, right=None):
    left = left or empty_svg_string()
    middle = middle or empty_svg_string()
    right = right or empty_svg_string()
    return interpolate_svg_to_string(
        filepath=relpath("rows-1-edges-twothirds.svg"),
        svg_replacements={"r0": left, "r1": middle, "r2": right},
    )


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


def five_overlapping_rects_1(rects):
    replacements = {f"r{i}": rect for (i, rect) in rects.items()}
    return interpolate_svg_to_string(
        filepath=relpath("rows-1-five-overlapping-rects.svg"),
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


def centered_text_2(text):
    return interpolate_svg_to_string(
        filepath=relpath("rows-2-centered-text.svg"),
        text_replacements={"center_text": text},
    )


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


def text_left_right_2(left="", right=""):
    return interpolate_svg_to_string(
        filepath=relpath("rows-2-left-right-text.svg"),
        text_replacements={"left_text": left, "right_text": right},
    )


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


def rect_left_right_3(left, right):
    return interpolate_svg_to_string(
        filepath=relpath("rows-3-left-right-rect.svg"),
        svg_replacements={"r0": left, "r1": right},
    )


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
