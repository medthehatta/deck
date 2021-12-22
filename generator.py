import os

import sheets


class Generator:

    @staticmethod
    def gsheet(sheet_id):

        def _gsheet(method):
            method.__gsheet = sheet_id
            return method

        return _gsheet

    def __init__(self, prefix=None):
        self.prefix = prefix or os.path.dirname(os.path.abspath(__file__))

    def relpath(self, path):
        return os.path.join(self.prefix, path)

    def render(self, sheets_client):
        return {
            func.__name__: [
                func(x) for x in
                sheets.entries(sheets_client, sheets.gsheet(url))
            ]
            for (func, url) in self.sheet_mapping().items()
        }

    def sheet_mapping(self):
        return {
            getattr(self, method): getattr(getattr(self, method), "__gsheet")
            for method in dir(self)
            if (
                hasattr(self, method) and
                hasattr(getattr(self, method), "__gsheet")
            )
        }
