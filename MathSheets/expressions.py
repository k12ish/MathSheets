from dataclasses import dataclass, asdict
from MathSheets.core import Value, Variable, OneFrom
from MathSheets.constants import Integer


@dataclass
class Expression(Value):
    """docstring for Expression"""
    text: str
    _list: list

    def __str__(self) -> str:
        return self.text.format(*self._list)

    def check(self) -> bool:
        if self.text.count("{}") == len(self._list):
            return True
        return False

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

    def asdict(self) -> dict:
        return asdict(self)

    def substitute(self, exp, replacee=Variable()):
        assert isinstance(exp, Value)
        assert isinstance(replacee, Value)

        self._list = [exp if isinstance(v, type(replacee)) else v
                      for v in self._list]
        return self


v = Variable()
i = Integer().non_zero()

exp = Expression('e**{}', [v])
ln = Expression('ln({})', [v])

lin = Expression('{}*{} + {}', [i, v, i])
inv = Expression('1/{}', [v])

sin = Expression('sin({})', [v])
cos = Expression('cos({})', [v])
tan = Expression('tan({})', [v])

sec = Expression('sec({})', [v])
cot = Expression('cot({})', [v])
cosec = Expression('cosec({})', [v])


simple = OneFrom(
    exp, ln, inv, sin, cos, tan, sec, cot, cosec, lin
)
