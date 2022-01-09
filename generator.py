import os
from dataclasses import dataclass
import sys


@dataclass
class Deck:

    face: callable
    back: callable
    source: callable

    def render(self):
        records = self.source()
        return {
            "faces": [self.face(record) for record in records],
            "backs": [self.back(record) for record in records],
        }

    def render_faces(self):
        return [self.face(record) for record in self.source()]

    def render_backs(self):
        return [self.back(record) for record in self.source()]
