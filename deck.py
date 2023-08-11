import os
from dataclasses import dataclass
import sys

from svg import svg_string_to_pil
import tts
import layout


class Deck:

    def __init__(self, face, back, source, name=None, scale=1.0):
        self.face = face
        self.back = back
        self.source = source
        self.name = name
        self.scale = scale

    def _face(self, record):
        return self.face(record)

    def _back(self, record):
        return self.back(record)

    def preview_face(self):
        return self._face(self.source()[0])

    def preview_raw_face(self):
        return self.face(self.source()[0])

    def render(self):
        records = self.source()
        return {
            "faces": [self._face(record) for record in records],
            "backs": [self._back(record) for record in records],
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

    def sheet_urls(self, uploader):
        rendered = self.render()
        pils = tts.make_deck_pils(
            face_pils=rendered["faces"],
            back_pils=rendered["backs"],
        )
        front_url = uploader([pils["faces"]])[0]
        back_url = uploader([pils["backs"]])[0]
        return {
            "faces": front_url,
            "backs": back_url,
        }

    def tts_json(self, uploader):
        rendered = self.render()
        names = self.names()
        num = len(rendered["faces"])
        pils = tts.make_deck_pils(
            face_pils=rendered["faces"],
            back_pils=rendered["backs"],
        )
        front_url = uploader([pils["faces"]])[0]
        back_url = uploader([pils["backs"]])[0]
        return tts.deck(
            front_url,
            back_url,
            num_cards=num,
            card_names=names,
            scale=self.scale,
        )


class Tokens:

    def __init__(self, face, source, name=None, scale=1.0):
        self.face = face
        self.source = source
        self.name = name
        self.scale = scale

    def _face(self, record):
        return self.face(record)

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
        pils = self.render()
        names = self.names()
        urls = uploader(pils)
        return tts.bag_of([
            tts.token(
                url,
                nickname=name,
                scale=self.scale,
            )
            for (name, url) in zip(names, urls)
        ])


class SvgDeck(Deck):

    def _face(self, record):
        return svg_string_to_pil(self.face(record))

    def _back(self, record):
        return svg_string_to_pil(self.back(record))


class SvgTokens(Tokens):

    def _face(self, record):
        return svg_string_to_pil(self.face(record))
