import hashlib
from importlib import reload
from io import BytesIO
import json
import os

import tts


def mancer_pils(pils):
    urls = []
    for pil in pils:
        buffered = BytesIO()
        pil.save(buffered, format="PNG")
        x = hashlib.sha1(buffered.getvalue()).hexdigest()
        path = f"/var/www/files/deck/{x}.png"
        if not os.path.isfile(path):
            with open(path, "wb") as f:
                pil.save(f)
        urls.append(f"https://files.mancer.in/deck/{x}.png")

    return urls


def tts_tokens(tokens):
    pils = tokens.render()
    names = tokens.names()
    urls = mancer_pils(pils)
    return tts.bag_of([
        tts.token(url, nickname=name) for (name, url) in zip(names, urls)
    ])


def tts_token_urls(tokens):
    pils = tokens.render()
    names = tokens.names()
    return mancer_pils(pils)


def tts_deck(deck):
    rendered = deck.render()
    names = deck.names()
    num = len(rendered["faces"])
    pils = tts.make_deck_pils(
        face_pils=rendered["faces"],
        back_pils=rendered["backs"],
    )
    front_url = mancer_pils([pils["faces"]])[0]
    back_url = mancer_pils([pils["backs"]])[0]
    return tts.deck(front_url, back_url, num_cards=num, card_names=names)


def tts_deck_urls(deck):
    rendered = deck.render()
    num = len(rendered["faces"])
    pils = tts.make_deck_pils(
        face_pils=rendered["faces"],
        back_pils=rendered["backs"],
    )
    front_url = mancer_pils([pils["faces"]])[0]
    back_url = mancer_pils([pils["backs"]])[0]
    return {
        "faces": front_url,
        "backs": back_url,
    }


def dump_tts_game(objects, path):
    with open(path, "w") as f:
        json.dump(tts.game(objects), f)
