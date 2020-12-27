from sympy import latex
from Expressions.core import Value


def log_to_ln(func):
    def inner(*args, **kwargs):
        ret_string = func(*args, **kwargs)
        ret_string = ret_string.replace('\\log', '\\ln')
        return ret_string
    return inner


sympy_to_latex = log_to_ln(latex)


def equation_list_to_latex(equation_list):
    if isinstance(equation_list[0], Value):
        equation_list = [item.as_sympy() for item in equation_list]
    if not isinstance(equation_list[0], str):
        equation_list = [sympy_to_latex(item) for item in equation_list]
    return equation_list
