import os
import sys

import sheets


class Generator:

    @staticmethod
    def gsheet(sheet_id, tab="Sheet 1"):

        def _gsheet(method):
            method._gsheet = sheet_id
            method._gsheet_tab = tab
            return method

        return _gsheet

    def __init__(self, prefix=None):
        clsfile = sys.modules[self.__class__.__module__].__file__
        self.prefix = prefix or os.path.dirname(os.path.abspath(clsfile))

    def relpath(self, path):
        return os.path.join(self.prefix, path)

    def render_deck(self, sheets_client, func_name):
        func_names = [func.__name__ for func in self.sheet_mapping()]
        matches = [
            (func, (url, tab))
            for (func, (url, tab)) in self.sheet_mapping().items()
            if func.__name__ == func_name
        ]
        if len(matches) == 0:
            raise LookupError(f"No {func_name} in {func_names}")
        elif len(matches) > 1:
            raise LookupError(f"Ambiguous {func_name} in {func_names}")
        else:
            (func, (url, tab)) = matches[0]
            return [
                func(x) for x in
                sheets.entries(sheets_client, sheets.gsheet(url), sheet=tab)
            ]

    def render_all(self, sheets_client):
        return {
            func.__name__: [
                func(x) for x in
                sheets.entries(sheets_client, sheets.gsheet(url))
            ]
            for (func, url) in self.sheet_mapping().items()
        }

    def sheet_mapping(self):
        return {
            getattr(self, method): (
                getattr(getattr(self, method), "_gsheet"),
                getattr(getattr(self, method), "_gsheet_tab")
            )
            for method in dir(self)
            if (
                hasattr(self, method) and
                hasattr(getattr(self, method), "_gsheet")
            )
        }
