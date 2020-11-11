import random


class Value:
    """The fundamental unit of expressions"""

    def __init_subclass__(cls, *args, **kwargs):
        assert hasattr(cls, "__str__")
        return super().__init_subclass__(*args, **kwargs)


class Variable(Value):
    """docstring for Variable"""

    def __str__(self):
        return 'x'


class OneFrom(Value):

    def __init__(self, *values):
        self.values = values

    def __str__(self):
        return self.pick()

    def pick(self):
        choice = random.choice(self.values)
        if isinstance(choice, Value):
            return choice
        return OneFrom(*choice).pick()
