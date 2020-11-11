from dataclasses import dataclass, asdict
from MathSheets.core import Value, Variable, OneFrom
from MathSheets.constants import Integer


@dataclass
class Expression(Value):
    """docstring for Expression"""
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

    def rebuild(self) -> None:
        """substitutes subexpressions, removing nesting"""

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

        self._list = [exp if isinstance(v, type(replacee)) else v
                      for v in self._list]
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


class Trig(Expression):
    """docstring for Trig"""

    @staticmethod
    def sin(self):
        return Trig('sin({})', [Variable()])

    @staticmethod
    def cos(self):
        return Trig('cos({})', [Variable()])

    @staticmethod
    def tan(self):
        return Trig('tan({})', [Variable()])

    @staticmethod
    def sec(self):
        return Trig('sec({})', [Variable()])

    @staticmethod
    def cot(self):
        return Trig('cot({})', [Variable()])

    @staticmethod
    def csc(self):
        return Trig('csc({})', [Variable()])

    @staticmethod
    def all(self):
        return (Trig.sin(), Trig.cos(), Trig.tan(),
                Trig.csc(), Trig.sec(), Trig.cot(),
                )


v = Variable()
i = Integer().non_zero()

exp = Expression('e**{}', [v])
ln = Expression('ln({})', [v])

lin = Expression('{}*{} + {}', [i, v, i])
inv = Expression('1/{}', [v])

simple = OneFrom(
    exp, ln, inv, sin, cos, tan, sec, cot, cosec, lin
)
