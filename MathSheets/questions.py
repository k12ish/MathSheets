import copy
from MathSheets.expressions import simple
from MathSheets.constants import Integer
from sympy.parsing.sympy_parser import parse_expr
from sympy import diff, simplify, trigsimp
from sympy.matrices import Matrix
from sympy.matrices.common import NonInvertibleMatrixError
from MathSheets.exam import EquationListQuestion
from sympy import latex


def log_to_ln(func):
    def inner(*args, **kwargs):
        ret_string = func(*args, **kwargs)
        ret_string = ret_string.replace('\\log', '\\ln')
        return ret_string
    return inner


latex = log_to_ln(latex)


class Differenciate(EquationListQuestion):
    """docstring for Differenciate"""
    _question_title = "Differenciation"
    _question_prompt = "Differenciate the following expressions:"

    _answer_title = "Differenciation"
    _answer_prompt = ""

    def _build_questions_answers(self):
        questions, answers = [], []
        for i in range(self.num):
            expr = self._new_expr()
            symbol = expr.free_symbols.pop()
            questions.append(expr)
            answers.append(trigsimp(simplify(diff(expr, symbol))))
        questions = list(map(latex, questions))
        answers = list(map(latex, answers))
        return questions, answers

    def _new_expr(self):
        base = copy.copy(simple.pick())
        for i in range(2):
            base.substitute(copy.copy(simple.pick()))
        return parse_expr(str(base))


class MatrixInverse(EquationListQuestion):
    """docstring for MatrixInverse"""

    _question_title = "Matrices"
    _question_prompt = "Calculate the inverse of the following:"

    _answer_title = "Matrices"
    _answer_prompt = ""

    def _build_questions_answers(self):
        questions, answers = [], []
        while len(questions) < self.num:
            mat = self._new_expr()
            try:
                answers.append(mat.inv())
                questions.append(mat)
            # Ignore any errors
            except NonInvertibleMatrixError:
                pass

        questions = list(map(latex, questions))
        answers = list(map(latex, answers))

        return questions, answers

    def _new_expr(self):
        i = Integer().in_range(-9,9)
        nums = [int(str(i)) for item in range(9)]
        return Matrix(3,3, nums)
