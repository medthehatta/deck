from entity_helpers import split_to_multiple_fields
from game_icons import colored_svg as game_icon
from deck import Deck
from sheets import google_sheet_reader
from sheets import gsheet
from svg import constant_svg
from svg import interpolate_svg
from util import prefix


relpath = prefix(__file__)


def make_card(record):
    # Name, Despair, Morale, Survival, Special
    special_data = split_to_multiple_fields(
        record["Special"],
        field_name="Special",
        chars_per=25,
        max_lines=7,
    )
    new_record = {**record, **special_data}
    return interpolate_svg(
        filepath=relpath("cards.svg"),
        text_replacements=new_record,
    )


def make_spell(record):
    # Name, Reagent 1, Reagent 2, Reagent 3, Reagent 4, Reagent 5, Flavor
    flavor_data = split_to_multiple_fields(
        record["Flavor"],
        field_name="Flavor",
        chars_per=40,
        max_lines=5,
    )
    reagent_abbrev = {
        r: record[r][:2].title()
        for r in record
        if r.startswith("Reagent")
    }
    new_record = {**record, **flavor_data, **reagent_abbrev}
    return interpolate_svg(
        filepath=relpath("spell.svg"),
        text_replacements=new_record,
    )


def make_threat(record):
    # Name, Rating, Penalty, Reward 1 - Reward 4 If we only have Reward 1 but
    # no other rewards, it is a "single-reward" type threat
    if record["Reward 1"] and not record["Reward 2"]:
        return single_reward_threat(record)
    elif record["Reward 1"] and record["Reward 2"]:
        return multi_reward_threat(record)
    else:
        # This is for empty entries
        return single_reward_threat(record)


def single_reward_threat(record):
    # Name, Rating, Penalty, Reward 1
    penalty_data = split_to_multiple_fields(
        record["Penalty"],
        field_name="Penalty",
        chars_per=25,
        max_lines=4,
    )
    reward_data = split_to_multiple_fields(
        record["Reward 1"],
        field_name="Reward",
        chars_per=25,
        max_lines=2,
    )
    new_record = {**record, **penalty_data, **reward_data}
    return interpolate_svg(
        filepath=relpath("threats-1reward.svg"),
        text_replacements=new_record,
    )


def multi_reward_threat(record):
    # Name, Rating, Penalty, Reward 1, Reward 2, Reward 3, Reward 4
    penalty_data = split_to_multiple_fields(
        record["Penalty"],
        field_name="Penalty",
        chars_per=25,
        max_lines=4,
    )
    reward_abbrev = {
        r: record[r][:2].title()
        for r in record
        if r.startswith("Reward")
    }
    new_record = {**record, **penalty_data, **reward_abbrev}
    return interpolate_svg(
        filepath=relpath("threats-4reward.svg"),
        text_replacements=new_record,
    )


card_sheet = gsheet("17kjLV9fPps12wCQGm9GVjGhs9gszPbe4Uqsn35MJ9ro")
spell_sheet = gsheet("1bci7naIabjSt-_53mzf7gE6nT36aF6VQLSkHarFfij4")
threat_sheet = gsheet("1_FvRdix-Ax7CjWtHCcB0zjaNkSP-vO_72CWD508FUJQ")


cards = Deck(
    face=make_card,
    back=constant_svg(relpath("back.svg")),
    source=google_sheet_reader(card_sheet),
)


spells = Deck(
    face=make_spell,
    back=constant_svg(relpath("back.svg")),
    source=google_sheet_reader(spell_sheet),
)


threats = Deck(
    face=make_threat,
    back=constant_svg(relpath("threats-back.svg")),
    source=google_sheet_reader(threat_sheet),
)
