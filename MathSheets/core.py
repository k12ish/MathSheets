import random
import pylatex


class Value:
    """The fundamental unit of expressions"""

    def __init_subclass__(cls, *args, **kwargs):
        assert hasattr(cls, "__str__")
        return super().__init_subclass__(*args, **kwargs)


class Variable(Value):
    """docstring for Variable"""

    def __init__(self, letter=None):
        self.letter = letter

    def __str__(self):
        if self.letter:
            return self.letter
        return 'x'

    def __eq__(self, other):
        if isinstance(other, Variable):
            return any([
                None in {self.letter, other.letter},
                self.letter == other.letter
            ])
        return False


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
