import glob
import importlib
import json
import os
import pkgutil
import sys

import click

from deck import Deck
from deck import Tokens
from mancer import mancer_pils
from util import prefix
import tts


relpath = prefix(__file__)


@click.group()
def cli():
    """Generate cards for game prototypes."""
    pass


def emit_deck_json(deck):
    return tts.game(deck.tts_json(uploader=mancer_pils))


def emit_deck_urls(deck):
    return deck.sheet_urls(uploader=mancer_pils)


def emit_token_json(token):
    return tts.game(token.tts_json(uploader=mancer_pils))


def emit_token_urls(token):
    return token.image_urls(uploader=mancer_pils)


def url_maker_command(deck):

    if isinstance(deck, Deck):
        emitter = deck.sheet_urls
    elif isinstance(deck, Tokens):
        emitter = deck.image_urls
    else:
        raise TypeError(f"Unrecognized type: {type(deck)}")

    def _card_maker():
        print(json.dumps(emitter(uploader=mancer_pils)))

    return click.command()(_card_maker)


def json_maker_command(deck):

    if isinstance(deck, Deck):
        emitter = emit_deck_json
    elif isinstance(deck, Tokens):
        emitter = emit_token_json
    else:
        raise TypeError(f"Unrecognized type: {type(deck)}")

    def _card_maker():
        print(json.dumps(emitter(deck)))

    return click.command()(_card_maker)


def json_file_maker_command(deck):

    if isinstance(deck, Deck):
        emitter = emit_deck_json
    elif isinstance(deck, Tokens):
        emitter = emit_token_json
    else:
        raise TypeError(f"Unrecognized type: {type(deck)}")

    @click.command()
    @click.argument("outfile", type=click.File("w"))
    def _card_maker(outfile: click.File):
        result = emitter(deck)
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
            if isinstance(deck, (Deck, Tokens))
        )

        game_group = attach_command(top, group(gamename))

        for (deckname, deck) in decks:
            attach_command(game_group, cmd(deck), name=deckname)


deck_dir = relpath("../decks")


sys.path.append(deck_dir)
plugins = [
    os.path.basename(os.path.dirname(name))
    for name in glob.glob(os.path.join(deck_dir, "*", "__init__.py"))
]


deck_plugins = {
    name: importlib.import_module(name)
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
