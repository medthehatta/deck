import os
from dataclasses import dataclass
import sys

from svg import to_pil
import tts
import layout
from util import partition_all


class Deck:

    def __init__(self, face, back, source=None, name=None, scale=1.0):
        self.face = face if callable(face) else (lambda _: face)
        self.back = back if callable(back) else (lambda _: back)
        self.source = source or (lambda: [None])
        self.name = name if callable(name) else (lambda _: name)
        self.scale = scale

    def _face(self, record):
        return to_pil(self.face(record))

    def _back(self, record):
        return to_pil(self.back(record))

    def preview_face(self):
        return self._face(self.source()[0])

    def preview_raw_face(self):
        return self.face(self.source()[0])

    def render(self):
        records = self.source()
        fbs = [
            (self._face(record), self._back(record))
            for record in records
        ]
        return {
            "faces": [f for (f, b) in fbs],
            "backs": [b for (f, b) in fbs],
        }

    def render_faces(self):
        return [self._face(record) for record in self.source()]

    def render_backs(self):
        return [self._back(record) for record in self.source()]

    def names(self):
        records = self.source()
        if self.name is None:
            return ["" for _ in records]
        else:
            return [self.name(record) for record in records]

    def portrait_on_letter(self, uploader):
        sheets = layout.portrait_cards_on_letter(self.render_faces())
        return uploader(sheets)

    def oversize_portrait_on_letter(self, uploader):
        sheets = layout.layout_on_sheets_by_size(
            self.render_faces(),
            sheet_x=11,
            sheet_y=8.5,
            card_x=3.5,
            card_y=2.5,
        )
        return uploader(sheets)

    def sheet_urls(self, uploader):
        rendered = self.render()
        names = self.names()
        faces = rendered["faces"]
        backs = rendered["backs"]
        num = len(faces)
        front_sheet_pils = layout.layout_on_sheets_by_counts(
            faces,
            num_width=10,
            num_height=7,
        )
        back_sheet_pils = layout.layout_on_sheets_by_counts(
            backs,
            num_width=10,
            num_height=7,
        )
        front_urls = uploader(front_sheet_pils)
        back_urls = uploader(back_sheet_pils)
        return {
            "fronts": front_urls,
            "backs": back_urls,
        }

    def tts_json(self, uploader):
        STANDARD_CARD_HEIGHT = 350
        rendered = self.render()
        names = self.names()
        faces = rendered["faces"]
        scale = faces[0].height / STANDARD_CARD_HEIGHT
        backs = rendered["backs"]
        num = len(faces)
        front_sheet_pils = layout.layout_on_sheets_by_counts(
            faces,
            num_width=10,
            num_height=7,
        )
        back_sheet_pils = layout.layout_on_sheets_by_counts(
            backs,
            num_width=10,
            num_height=7,
        )
        front_urls = uploader(front_sheet_pils)
        back_urls = uploader(back_sheet_pils)
        name_batches = list(partition_all(70, names))

        if len(front_urls) == 1:
            return tts.deck(
                front_urls[0],
                back_urls[0],
                num_cards=num,
                card_names=name_batches[0],
                scale=scale,
            )

        else:
            decks = []
            batches = zip(front_urls, back_urls, name_batches)
            for (front_url, back_url, card_names) in batches:
                num_cards = len(card_names)

                decks.append(
                    tts.deck(
                        front_url,
                        back_url,
                        num_cards=num_cards,
                        card_names=card_names,
                        scale=scale,
                    )
                )

            return tts.bag_of(decks)


class Tokens:

    def __init__(self, face, source=None, name=None, scale=1.0):
        self.face = face if callable(face) else (lambda _: face)
        self.source = source or (lambda: [None])
        self.name = name if callable(name) else (lambda _: name)
        self.scale = scale

    def _face(self, record):
        return to_pil(self.face(record))

    def preview_face(self):
        return self._face(self.source()[0])

    def preview_raw_face(self):
        return self.face(self.source()[0])

    def render(self):
        records = self.source()
        return [self._face(record) for record in records]

    def names(self):
        records = self.source()
        if self.name is None:
            return ["" for _ in records]
        else:
            return [self.name(record) for record in records]

    def image_urls(self, uploader):
        pils = self.render()
        names = self.names()
        return uploader(pils)

    def tts_json(self, uploader):
        STANDARD_CARD_HEIGHT = 350
        pils = self.render()
        names = self.names()
        urls = uploader(pils)
        if len(urls) == 1:
            return tts.token(
                urls[0],
                nickname=names[0],
                scale=pils[0].height / STANDARD_CARD_HEIGHT,
            )
        else:
            return tts.bag_of([
                tts.token(
                    url,
                    nickname=name,
                    scale=pil.height / STANDARD_CARD_HEIGHT,
                )
                for (name, url, pil) in zip(names, urls, pils)
            ])


def dbg(x):
    print(x)
    return x


SvgDeck = Deck
SvgTokens = Tokens
