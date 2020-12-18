from MathSheets.utils import equation_list_to_latex
from enum import Enum, auto
import pylatex


class Exam:
    """Exam objects store the relevant questions and answers"""

    def __init__(self):
        geo = {"top":"3.5cm","bottom":"3.5cm", "left":"3.7cm",
               "right":"4.5cm", "columnsep":"30pt"}
        self.q_paper = MathDoc(geometry_options=geo)
        self.q_paper.append(pylatex.NoEscape(r'\twocolumn'))
        self.a_paper = MathDoc(geometry_options=geo)

    def add_questions(self, *args):
        assert all((isinstance(item, Question) for item in args))
        for item in args:
            item.write(self.q_paper, self.a_paper)

    def export(self, filename='output\\test'):
        self.q_paper.generate_pdf(filename + '_questions')
        self.a_paper.generate_pdf(filename + '_answers')


class EquationEnvironment(pylatex.base_classes.Environment):
    """docstring for EquationEnvironment"""
    _latex_name = 'equation'
    packages = [pylatex.package.Package('amsmath')]


class MathDoc(pylatex.Document):
    """docstring for Paper"""

    def add_numbered_equations(self, eqtns):
        for item in eqtns:
            with self.create(EquationEnvironment()) as env:
                env.append(pylatex.NoEscape(item))

    def add_equations(self, eqtns):
        for item in eqtns:
            self.append(pylatex.Math(data=item, escape=False))


class Question:
    """docstring for Question"""

    def __init__(self, num_questions):
        self.num = num_questions

    def __init_subclass__(cls, *args, **kwargs):
        assert hasattr(cls, "write")
        return super().__init_subclass__(*args, **kwargs)


class EquationListQuestion(Question):
    """Questions which are lists of equations
    Subclasses require:
        _build_questions_answers  (callable)
        _question_title
        _answer_title
        _question_prompt
        _answer_prompt


    including a `new_expr()` method is advised for ease of monkey patching

    _build_questions_answers returns a (questions, answers) pair
    (questions, answers) must be lists of strings/sympy/expressions
    all elements in these lists must have the same type
    """
    def __init_subclass__(cls, *args, **kwargs):
        assert hasattr(cls, "_build_questions_answers")
        assert callable(cls._build_questions_answers)
        assert hasattr(cls, "_topic")
        assert hasattr(cls, "_prompt")
        return super().__init_subclass__(*args, **kwargs)

    def write(self, q_paper, a_paper):
        questions, answers = self._build_questions_answers()
        questions = equation_list_to_latex(questions)
        answers = equation_list_to_latex(answers)

        with q_paper.create(pylatex.Section(str(self._topic))):
            q_paper.append(self._prompt)
            q_paper.add_numbered_equations(questions)

        with a_paper.create(pylatex.Section("")):
            a_paper.add_numbered_equations(answers)


class Prompts(Enum):
    """docstring for Prompts"""
    SIMPLIFY = auto()
    EXPAND = auto()
    CALCULATE = auto()
    DIFFERENTIATE = auto()
    INTEGRATE = auto()

    def __str__(self):
        return self.name.capitalize() + ' the following:'

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class Topics(Enum):
    """docstring for Topic"""

    MATRICES = auto()
    CALCULUS = auto()
    ALGEBRA = auto()
    GEOMETRY = auto()

    def __str__(self):
        return self.name.capitalize()

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
