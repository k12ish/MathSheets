import copy
from Expressions.expressions import simple, Poly
from Expressions.constants import Integer
from sympy import diff, simplify, trigsimp, expand
from sympy.matrices import Matrix
from sympy.matrices.common import NonInvertibleMatrixError
from MathSheets.exam import EquationListQuestion


class Differentiate(EquationListQuestion):
    """docstring for Differentiate"""
    _question_title = "Differentiation"
    _question_prompt = "Differentiate the following expressions:"

    _answer_title = "Differentiation"
    _answer_prompt = ""

    def _build_questions_answers(self):
        questions, answers = [], []
        for i in range(self.num):
            expr = self._new_expr()
            symbol = expr.free_symbols.pop()
            questions.append(expr)
            answers.append(trigsimp(simplify(diff(expr, symbol))))
        return questions, answers

    def _new_expr(self):
        base = copy.copy(simple.pick())
        for i in range(2):
            base.substitute(copy.copy(simple.pick()))
        return base.into_sympy()


class ExpandPolynomial(EquationListQuestion):
    """docstring for ExpandPolynomial"""
    _question_title = ""
    _question_prompt = "Expand the following expressions:"

    _answer_title = ""
    _answer_prompt = ""

    def _build_questions_answers(self):
        questions, answers = [], []
        for i in range(self.num):
            expr = self._new_expr()
            questions.append(expr)
            answers.append(simplify(expand(expr)))
        return questions, answers

    def _new_expr(self):
        return Poly.of_degree(3).into_sympy()


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
        return questions, answers

    def _new_expr(self):
        i = Integer().in_range(-9,9)
        nums = [int(str(i)) for item in range(9)]
        return Matrix(3,3, nums)
