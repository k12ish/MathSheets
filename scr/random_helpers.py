import random


class Integer:
    """docstring for Integer"""

    def __init__(self):
        self.upper = 10
        self.lower = -10
        self.discard = set()

    def in_range(self, upper, lower):
        assert isinstance(upper, int)
        assert isinstance(lower, int)
        self.upper = upper
        self.lower = lower
        return self

    def non_zero(self):
        self.discard.add(0)

    def remove(self, iterable):
        self.discard = self.discard.union(iterable)

    def pick(self):
        if self.discard:
            valid = set(range(self.lower, self.upper))
            valid = valid.intersection(self.discard)
            return random.choice(valid)
        return random.randint(self.lower, self.upper)

    def __str__(self):
        return str(self.pick())
