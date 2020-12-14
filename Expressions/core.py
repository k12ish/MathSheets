from sympy.parsing.sympy_parser import parse_expr
from dataclasses import dataclass, asdict
from dacite import from_dict
import random


class Value:
    """ The fundamental unit of expressions

       Value objects denote anything that could go inside an equation.
       Eg.
       - The variable 'x'
       - The integer '3'
       - The expression 'x + 3'

       All objects are defined to have a string representation
       which can be parsed by sympy
    """

    def __init_subclass__(cls, *args, **kwargs):
        assert hasattr(cls, "__str__")
        return super().__init_subclass__(*args, **kwargs)

    def into_sympy(self):
        return parse_expr(str(self))


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


class Constant(Value):
    """docstring for Constant"""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass


@dataclass
class Expression(Value):
    """Expressions objects represents maths expressions"""
    text: str
    _list: list

    def __post_init__(self):
        assert self.check()

    def __str__(self) -> str:
        return self.text.format(*self._list)

    def check(self) -> bool:
        if self.text.count("{}") == len(self._list):
            return True
        return False

    def into_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict):
        return from_dict(data_class=Expression, data=data)

    def rebuild(self) -> None:
        """substitutes subexpressions, removing nesting

        On rebuild, nested expressions get merged into the parent object

        This Expression:             |  Is rebuilt to become:

        Expression('e^{}',           |
          [Expression('{}{}',        |  Expression('e^({}{})',
             [Integer(), Variable()] |    [Integer(), Variable()]
            )                        |  )
          ]                          |
        )

        For each child expression (child) within parent._list,
          - recursively rebuild child
          - replace the corresponding '{}' in parent.text with
            '(' + child.text + ')'
          - remove the child and insert the elements from child._list
            into parent._list
        """

        assert self.check()
        new_subs = []
        new_list = []

        for item in self._list:
            if isinstance(item, Expression):
                item.rebuild()
                new_subs.append('(' + item.text + ')')
                new_list.extend(item._list)
            else:
                new_subs.append("{}")
                new_list.append(item)

        text = self.text.split("{}")
        new_text = text + new_subs
        new_text[::2] = text
        new_text[1::2] = new_subs
        self.text = ''.join(new_text)
        self._list = new_list

    def substitute(self, exp, replacee=Variable()):
        assert isinstance(exp, Value)
        assert isinstance(replacee, Value)
        self._list = [exp if v == replacee else v for v in self._list]
        self.rebuild()
        return self

    def __add__(self, other):
        self.text = '(' + self.text + ') + (' + other.text + ')'
        self._list.extend(other._list)

    def __sub__(self, other):
        self.text = '(' + self.text + ') - (' + other.text + ')'
        self._list.extend(other._list)

    def __mul__(self, other):
        self.text = '(' + self.text + ')*(' + other.text + ')'
        self._list.extend(other._list)

    def __div__(self, other):
        self.text = '(' + self.text + ')/(' + other.text + ')'
        self._list.extend(other._list)
