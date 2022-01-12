from functools import wraps
import random


class RandomValue:
    pass


class StochasticValue(RandomValue):

    def __init__(self, choices):
        self.choices = choices

    def reify(self, rng=None):
        rng = rng or random.Random()
        return rng.choice(self.choices)


class StochasticRange(RandomValue):

    def __init__(self, low, high):
        self.low = low
        self.high = high

    def reify(self, rng=None):
        rng = rng or random.Random()
        return rng.randint(self.low, self.high)


class FunctionEvaluation(RandomValue):

    def __init__(self, func):
        self.func = func

    def reify(self, rng=None):
        rng = rng or random.Random()
        return self.func(rng)


def rval(x):
    return lift(lambda y: y)(x)


def choice(options):
    return StochasticValue(options)


def intrange(low, high):
    return StochasticRange(low, high)


# TODO: This is a little weird, I think there's probably a more elegant way to
# do this
def multiply(x, times=1):
    return FunctionEvaluation(
        lambda rng: [rval(x).reify(rng) for _ in range(rval(times).reify(rng))]
    )


def lift(func):

    @wraps(func)
    def _lifted(*args, **kwargs):

        def _resulting(rng):
            unlifted_args = [recursive_apply(rng, arg) for arg in args]
            unlifted_kwargs = {
                k: recursive_apply(rng, v) for (k, v) in kwargs.items()
            }
            return func(*unlifted_args, **unlifted_kwargs)

        return FunctionEvaluation(_resulting)

    return _lifted


def recursive_apply(rng, data):

    if isinstance(data, dict):
        r = {k: recursive_apply(rng, v) for (k, v) in data.items()}
        return type(data)(r)

    elif isinstance(data, (list, tuple)):
        r = [recursive_apply(rng, x) for x in data]
        return type(data)(r)

    elif isinstance(data, RandomValue):
        return data.reify(rng)

    else:
        return data
