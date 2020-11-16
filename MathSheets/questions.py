import copy
import pylatex
from MathSheets.expressions import simple
from MathSheets.constants import Integer
from sympy.parsing.sympy_parser import parse_expr
from sympy import diff
from sympy import latex, simplify, trigsimp
from sympy.matrices import Matrix


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


class Differenciate(Question):
    """docstring for Differenciate"""

    def write(self, qPaper, aPaper):
        questions, answers = self._build_questions_answers()
        prompt = "Differenciate the following equations:"
        with qPaper.create(pylatex.Section('Differenciation')):
            qPaper.append(prompt)
            qPaper.add_numbered_equations(questions)

        prompt = ""
        with aPaper.create(pylatex.Section(prompt)):
            aPaper.add_numbered_equations(answers)

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


class MatrixInverse(Question):
    """docstring for MatrixInverse"""

    def write(self, qPaper, aPaper):
        questions, answers = self._build_questions_answers()
        prompt = "Find the inverse of the following matrices:"
        with qPaper.create(pylatex.Section('Matrices')):
            qPaper.append(prompt)
            print(questions)
            qPaper.add_numbered_equations(questions)

        prompt = ""
        with aPaper.create(pylatex.Section(prompt)):
            aPaper.add_numbered_equations(answers)

    def _build_questions_answers(self):
        questions, answers = [], []
        for i in range(self.num * 2):
            mat = self._new_expr()
            try:
                answers.append(mat.inv())
                questions.append(mat)
            except sympy.matrices.common.NonInvertibleMatrixError:
                pass

        questions = list(map(latex, questions))
        answers = list(map(simplify, answers))
        answers = list(map(latex, answers))

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
