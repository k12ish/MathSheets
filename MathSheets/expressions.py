from MathSheets.core import Value, Variable
from MathSheets.utils import OneCopyFrom
from MathSheets.constants import Integer
from dataclasses import dataclass, asdict
from dacite import from_dict


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

    def asdict(self) -> dict:
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


class Trig:
    """docstring for Trig"""

    @staticmethod
    def sin():
        return Expression('sin({})', [Variable()])

    @staticmethod
    def cos():
        return Expression('cos({})', [Variable()])

    @staticmethod
    def tan():
        return Expression('tan({})', [Variable()])

    @staticmethod
    def sec():
        return Expression('sec({})', [Variable()])

    @staticmethod
    def cot():
        return Expression('cot({})', [Variable()])

    @staticmethod
    def csc():
        return Expression('csc({})', [Variable()])

    @staticmethod
    def standard():
        return (Trig.sin, Trig.cos, Trig.tan)

    @staticmethod
    def reciprocal():
        return (Trig.csc, Trig.sec, Trig.cot)

    @staticmethod
    def all():
        return (Trig.sin, Trig.cos, Trig.tan,
                Trig.csc, Trig.sec, Trig.cot)


class Poly:
    """docstring for Poly"""
    @staticmethod
    def linear(v=Variable(), i=Integer().non_zero()):
        return Expression('{}*{} + {}', [i, v, i])

    @staticmethod
    def quadratic(v=Variable(), i=Integer().non_zero()):
        return Expression('{}*({})**2 + {}*({}) + {}', [i, v, i, v, i])


v = Variable()
i = Integer().non_zero()

exp = Expression('e**{}', [v])
ln = Expression('ln({})', [v])

lin = Expression('{}*{} + {}', [i, v, i])
expon = Expression('({})**{}', [v, i])
inv = Expression('1/{}', [v])


simple = OneCopyFrom(
    exp, ln, inv, *Trig.standard(), lin, Trig.reciprocal(), expon
)
