import copy
import random
from MathSheets.core import Value


class OneCopyFrom(Value):
    """docstring for OneCopyFrom"""

    def __init__(self, *values):
        self.values = values

    def __str__(self):
        return self.pick()

    def pick(self):
        choice = random.choice(self.values)
        if callable(choice):
            return choice()
        if isinstance(choice, Value):
            return copy.copy(choice)
        return OneCopyFrom(*choice).pick()


from sympy import latex


def log_to_ln(func):
    def inner(*args, **kwargs):
        ret_string = func(*args, **kwargs)
        ret_string = ret_string.replace('\\log', '\\ln')
        return ret_string
    return inner


sympy_to_latex = log_to_ln(latex)


from sympy.parsing.sympy_parser import parse_expr

string_to_sympy = parse_expr
