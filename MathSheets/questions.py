from MathSheets.expressions import simple, Poly
from MathSheets.exam import EquationListQuestion
from MathSheets.utils import string_to_sympy
from MathSheets.constants import Integer
from sympy import diff, simplify
from sympy.matrices import Matrix
from sympy.matrices.common import NonInvertibleMatrixError


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
            answers.append(simplify(diff(expr, symbol)))
        return questions, answers

    def _new_expr(self):
        base = simple.pick()
        for i in range(2):
            base.substitute(simple.pick())
        return string_to_sympy(str(base))


class MatrixInverse(EquationListQuestion):
    """docstring for MatrixInverse"""

    _question_title = "Matrices"
    _question_prompt = "Calculate the inverse of the following:"

    _answer_title = "Matrices"
    _answer_prompt = ""

    def _build_questions_answers(self):
        questions, answers = [], []
        # We make as many questions as required
        while len(questions) < self.num:
            mat = self._new_expr()
            try:
                answers.append(mat.inv())
                questions.append(mat)
            # Ignore any errors that come up in the process
            except NonInvertibleMatrixError:
                pass
        return questions, answers

    def _new_expr(self):
        i = Integer().in_range(-9,9)
        nums = [int(str(i)) for item in range(9)]
        return Matrix(3,3, nums)


class Simplify(EquationListQuestion):
    """docstring for Simplify"""

    _question_title = "Simplification"
    _question_prompt = "Simplify the following:"

    _answer_title = "Simplification"
    _answer_prompt = ""

    def _build_questions_answers(self):
        pass

    def _new_expr(self):
        return Poly.linear()
