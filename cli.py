import importlib
import json
import pkgutil

import click

from deck import Deck
from deck import Tokens
from mancer_tts import tts_deck
from mancer_tts import tts_deck_urls
from mancer_tts import tts_tokens
from mancer_tts import tts_token_urls
import tts


@click.group()
def cli():
    """Generate cards for game prototypes."""
    pass


def emit_deck_json(deck):
    return tts.game(tts_deck(deck))


def emit_deck_urls(deck):
    return tts_deck_urls(deck)


def url_maker_command(deck):

    def _card_maker():
        print(json.dumps(emit_deck_urls(deck)))

    return click.command()(_card_maker)


def json_maker_command(deck):

    def _card_maker():
        print(json.dumps(emit_deck_json(deck)))

    return click.command()(_card_maker)


def json_file_maker_command(deck):

    @click.command()
    @click.argument("outfile", type=click.File("w"))
    def _card_maker(outfile: click.File):
        result = emit_deck_json(deck)
        json.dump(result, outfile)

    return _card_maker


def group(name):
    return click.group(name)(lambda: None)


def attach_command(parent, command, name=None):
    if name:
        command.name = name
        parent.add_command(command, name=name)
    else:
        parent.add_command(command)
    return command


def populate_output_type(name, cmd):
    top = attach_command(cli, group(name))

    for (gamename, plugin) in deck_plugins.items():
        candidates = ((x, getattr(plugin, x)) for x in dir(plugin))
        decks = (
            (deckname, deck) for (deckname, deck) in candidates
            if isinstance(deck, Deck)
        )

        game_group = attach_command(top, group(gamename))

        for (deckname, deck) in decks:
            attach_command(game_group, cmd(deck), name=deckname)


plugins = ["deck_despair", "deck_barcrawl", "deck_bard"]


deck_plugins = {
    name.replace("deck_", ""): importlib.import_module(name)
    for name in plugins
}


group_cmds = {
    "json": json_maker_command,
    "json-file": json_file_maker_command,
    "urls": url_maker_command,
}


for (name, cmd) in group_cmds.items():
    populate_output_type(name, cmd)


if __name__ == "__main__":
    cli()
