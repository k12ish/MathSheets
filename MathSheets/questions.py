import copy
from Expressions.expressions import simple, Poly
from Expressions.constants import Integer
from sympy import diff, simplify, trigsimp, expand
from sympy.matrices import Matrix
from sympy.matrices.common import NonInvertibleMatrixError
from MathSheets.exam import EquationListQuestion, Prompts, Topics


class Differentiate(EquationListQuestion):
    """docstring for Differentiate"""
    _topic = Topics.CALCULUS
    _prompt = Prompts.DIFFERENTIATE

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
        return base.as_sympy()


class ExpandPolynomialABC(EquationListQuestion):
    """docstring for ExpandPolynomialABC"""
    _topic = Topics.ALGEBRA
    _prompt = Prompts.EXPAND

    def _build_questions_answers(self):
        questions, answers = [], []
        for i in range(self.num):
            expr = self._new_expr()
            questions.append(expr)
            answers.append(simplify(expand(expr)))
        return questions, answers


class ExpandCubic(ExpandPolynomialABC):
    """docstring for ExpandCubic"""

    def _new_expr(self):
        return Poly.of_degree(3).as_sympy()


class ExpandQuadratic(ExpandPolynomialABC):
    """docstring for ExpandQuadratic"""

    def _new_expr(self):
        return Poly.of_degree(2).as_sympy()


class MatrixInverse(EquationListQuestion):
    """docstring for MatrixInverse"""
    _topic = Topics.MATRICES
    _prompt = "Find the inverse of the following:"

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
