from pathlib import Path


def prefix(path):
    prefix_ = Path(path).resolve().parent

    def _relative(subpath):
        return str(prefix_ / subpath)

    return _relative


def partition_all(num, seq):
    acc = []
    for (i, s) in enumerate(seq):
        if i != 0 and i % num == 0:
            yield tuple(acc)
            acc = []
        acc.append(s)

    if acc:
        yield tuple(acc)
