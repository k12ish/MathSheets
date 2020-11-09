from dataclasses import dataclass, asdict


class Value:
    """The fundamental unit of expressions
    """

    def __init_subclass__(cls, *args, **kwargs):
        assert hasattr(cls, "__str__")
        return super().__init_subclass__(*args, **kwargs)


class Constant(Value):
    """docstring for Constant"""

    pass


class Variable(Value):
    """docstring for Variable"""

    pass


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
