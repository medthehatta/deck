from entity_helpers import split_to_multiple_fields
from layout import portrait_cards_on_letter
from pdf import merge_pils_to_pdf
import sheets
from sheets import gsheet
from svg import svg_interpolator


def card(record):
    # Name, Despair, Morale, Survival, Special
    card_tpl = "cards.svg"
    special_data = split_to_multiple_fields(
        record["Special"],
        field_name="Special",
        chars_per=25,
        max_lines=7,
    )
    new_record = {**record, **special_data}
    return svg_interpolator(card_tpl)(new_record)


def spell(record):
    # Name, Reagent 1, Reagent 2, Reagent 3, Reagent 4, Reagent 5, Flavor
    card_tpl = "spell.svg"
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
    return svg_interpolator(card_tpl)(new_record)


def threat(record):
    # Name, Rating, Penalty, Reward 1 - Reward 4
    # If we only have Reward 1 but no other rewards, it is a "single-reward"
    # type threat
    if record["Reward 1"] and not record["Reward 2"]:
        return single_reward_threat(record)
    elif record["Reward 1"] and record["Reward 2"]:
        return multi_reward_threat(record)
    else:
        # This is for empty entries
        return single_reward_threat(record)


def single_reward_threat(record):
    # Name, Rating, Penalty, Reward 1
    card_tpl = "threats-1reward.svg"
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
    return svg_interpolator(card_tpl)(new_record)


def multi_reward_threat(record):
    # Name, Rating, Penalty, Reward 1, Reward 2, Reward 3, Reward 4
    card_tpl = "threats-4reward.svg"
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
    return svg_interpolator(card_tpl)(new_record)


def sheet_mapping():
    return {
        threat: gsheet("1_FvRdix-Ax7CjWtHCcB0zjaNkSP-vO_72CWD508FUJQ"),
        spell: gsheet("1bci7naIabjSt-_53mzf7gE6nT36aF6VQLSkHarFfij4"),
        card: gsheet("17kjLV9fPps12wCQGm9GVjGhs9gszPbe4Uqsn35MJ9ro"),
    }


def render(client):
    return {
        func.__name__: [func(x) for x in sheets.entries(client, url)]
        for (func, url) in sheet_mapping().items()
    }


def pdf_sample(client, output_path):
    # Join all the card types
    rendered = sum(render(client).values(), [])
    # Merge to one PDF
    return merge_pils_to_pdf(
        portrait_cards_on_letter(rendered),
        output_path,
    )
