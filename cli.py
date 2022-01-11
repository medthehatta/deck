import importlib
import pkgutil
import json

import click

from generator import Deck
import tts


@click.group()
def cli():
    """Generate cards for game prototypes."""
    pass


def emit_deck(rendered):
    return tts.game(tts.make_deck(**tts.mplex_face_back(rendered)))


def emit_urls(rendered):
    return tts.make_deck_urls(**tts.mplex_face_back(rendered))


def url_maker_command(deck):

    def _card_maker():
        rendered = deck.render()
        print(json.dumps(emit_urls(rendered)))

    return click.command()(_card_maker)


def json_maker_command(deck):

    def _card_maker():
        rendered = deck.render()
        print(json.dumps(emit_deck(rendered)))

    return click.command()(_card_maker)


def json_file_maker_command(deck):

    @click.command()
    @click.argument("outfile", type=click.File("w"))
    def _card_maker(outfile: click.File):
        rendered = deck.render()
        result = emit_deck(rendered)
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
