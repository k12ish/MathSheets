from MathSheets.core import Value
import random


class Integer(Value):
    """docstring for Integer"""

    def __init__(self, upper=None, lower=None):
        self.upper = 10
        self.lower = -10
        if upper is not None:
            assert isinstance(upper, int)
            self.upper = upper
        if lower is not None:
            assert isinstance(lower, int)
            self.lower = lower

        self.discard = set()

    def in_range(self, upper, lower):
        assert isinstance(upper, int)
        assert isinstance(lower, int)
        self.upper = upper
        self.lower = lower
        return self

    def non_zero(self):
        self.discard.add(0)
        return self

    def remove(self, iterable):
        self.discard = self.discard.union(iterable)
        return self

    def pick(self):
        if self.discard:
            valid = set(range(self.lower, self.upper))
            valid = valid.difference(self.discard)
            return random.sample(valid, 1)[0]
        return random.randint(self.lower, self.upper)

    def __str__(self):
        return str(self.pick())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass
