from entity_helpers import split_to_multiple_fields
from game_icons import colored_svg as game_icon
from generator import Deck
from sheets import google_sheet_reader
from sheets import gsheet
from svg import constant_svg
from svg import interpolate_svg
from util import prefix


relpath = prefix(__file__)


def make_face(record):
    quote_data = split_to_multiple_fields(
        record["Quote"],
        field_name="Quote",
        chars_per=50,
        max_lines=2,
    )
    trade_data = split_to_multiple_fields(
        record["Trade"],
        field_name="Trade",
        chars_per=50,
        max_lines=2,
    )
    text_replacements = {**record, **quote_data, **trade_data}
    return interpolate_svg(
        filepath=relpath("card.svg"),
        text_replacements=text_replacements,
    )


def make_bar(record):
    # Name, Symbol 1, Symbol 2, Symbol 3
    trash_can = game_icon(
        "delapouite/trash-can",
        color_code="00e000",
    )
    door = game_icon(
        "delapouite/window-bars",
        color_code="8b4513",
    )
    spray = game_icon(
        "lorc/spray",
        color_code="e00000",
    )
    # The keys here are the "ordinal" for the emojis.  It's easier to use
    # these numbers than to put literal emojis into the code
    icon = {
        128682: door,
        128994: trash_can,
        127982: spray,
    }

    # (The ord() is to convert emojis to the ordinal codes in our lookup table)
    icon_replacements={
        "symbol_1": icon[ord(record["Symbol 1"])],
        "symbol_2": icon[ord(record["Symbol 2"])],
        "symbol_3": icon[ord(record["Symbol 3"])],
    }

    # Put in a quick hack for ampersands: SVG wants ampersands to be "&amp;",
    # but the records may contain literal ampersands
    fixed_record = {k: v.replace("&", "&amp;") for (k, v) in record.items()}

    return interpolate_svg(
        filepath=relpath("bar.svg"),
        text_replacements=fixed_record,
        svg_replacements=icon_replacements,
    )


sheet = gsheet("1XN0Ur3K78uLolLrH6LqK2vo12xWWesgfSsliXKpDp0U")


green = Deck(
    face=make_face,
    back=constant_svg(relpath("back_green.svg")),
    source=google_sheet_reader(sheet, "Green"),
)


yellow = Deck(
    face=make_face,
    back=constant_svg(relpath("back_yellow.svg")),
    source=google_sheet_reader(sheet, "Yellow"),
)


red = Deck(
    face=make_face,
    back=constant_svg(relpath("back_red.svg")),
    source=google_sheet_reader(sheet, "Red"),
)


bars = Deck(
    face=make_bar,
    back=constant_svg(relpath("bar_back.svg")),
    source=google_sheet_reader(sheet, "Bars"),
)
