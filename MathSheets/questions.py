import copy
import pylatex
from MathSheets.expressions import simple
from MathSheets.constants import Integer
from sympy.parsing.sympy_parser import parse_expr
from sympy import diff, simplify, trigsimp
from sympy.matrices import Matrix


from sympy import latex


def log_to_ln(func):
    def inner(*args, **kwargs):
        ret_string = func(*args, **kwargs)
        ret_string = ret_string.replace('\\log', '\\ln')
        return ret_string
    return inner


latex = log_to_ln(latex)


class Question:
    """docstring for Question"""

    def __init__(self, num_questions):
        self.num = num_questions

    def __init_subclass__(cls, *args, **kwargs):
        assert hasattr(cls, "write")
        return super().__init_subclass__(*args, **kwargs)


class EquationListQuestion(Question):

    def __init_subclass__(cls, *args, **kwargs):
        assert hasattr(cls, "_build_questions_answers")
        assert callable(cls._build_questions_answers)
        assert hasattr(cls, "_question_title")
        assert hasattr(cls, "_question_prompt")
        assert hasattr(cls, "_answer_title")
        assert hasattr(cls, "_answer_prompt")
        return super().__init_subclass__(*args, **kwargs)

    def write(self, qPaper, aPaper):
        questions, answers = self._build_questions_answers()
        with qPaper.create(pylatex.Section(self._question_title)):
            if self._question_prompt:
                qPaper.append(self._question_prompt)
            qPaper.add_numbered_equations(questions)

        with aPaper.create(pylatex.Section(self._answer_title)):
            if self._answer_prompt:
                aPaper.append(self._answer_prompt)
            aPaper.add_numbered_equations(answers)


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


from sympy.matrices.common import NonInvertibleMatrixError


class MatrixInverse(EquationListQuestion):
    """docstring for MatrixInverse"""

    _question_title = "Matrices"
    _question_prompt = "Calculate the inverse of the following:"

    _answer_title = "Matrices"
    _answer_prompt = ""

    def _build_questions_answers(self):
        questions, answers = [], []
        # We make twice as many questions than required
        for i in range(self.num * 2):
            mat = self._new_expr()
            try:
                answers.append(mat.inv())
                questions.append(mat)
            # Ignore any errors
            except NonInvertibleMatrixError:
                pass

        questions = list(map(latex, questions))
        answers = list(map(latex, answers))

        # Crudely select matrices with a 'nicer' inverse
        def criteria(n):
            return len(n[0]) + len(n[1])

        zipped = list(zip(questions, answers))
        zipped.sort(key=criteria)
        questions = [i[0] for i in zipped][:self.num]
        answers = [i[1] for i in zipped][:self.num]
        return questions, answers

    def _new_expr(self):
        i = Integer().in_range(-9,9)
        nums = [int(str(i)) for item in range(9)]
        return Matrix(3,3, nums)
