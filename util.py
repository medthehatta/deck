from pathlib import Path


def prefix(path):
    prefix_ = Path(path).resolve().parent

    def _relative(subpath):
        return str(prefix_ / subpath)

    return _relative
