import os
from dataclasses import dataclass
import sys


@dataclass
class Deck:

    face: callable
    back: callable
    source: callable

    def _face(self, record):
        return self.face(record)

    def _back(self, record):
        return self.back(record)

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
