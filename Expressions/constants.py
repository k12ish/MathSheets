from Expressions.core import Value
import random


class Constant(Value):
    """docstring for Constant"""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass


class Integer(Constant):
    """docstring for Integer"""

    def __init__(self, upper=None, lower=None):
        self.upper, self.lower = 10, -10
        if upper is not None:
            assert isinstance(upper, int)
            self.upper = upper
        if lower is not None:
            assert isinstance(lower, int)
            self.lower = lower

        assert self.upper > self.lower
        self.discard = set()

    def in_range(self, lower, upper):
        assert isinstance(upper, int)
        assert isinstance(lower, int)
        self.upper = upper
        self.lower = lower
        assert self.upper > self.lower
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
