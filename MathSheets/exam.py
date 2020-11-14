import pylatex
from MathSheets.questions import Question


class EquationEnvironment(pylatex.base_classes.Environment):
    """docstring for EquationEnvironment"""
    _latex_name = 'equation'


class Paper(pylatex.Document):
    """docstring for Paper"""

    def add_numbered_equations(self, eqtns):
        for item in eqtns:
            with self.create(EquationEnvironment()) as env:
                env.append(pylatex.NoEscape(item))

    def add_equations(self, eqtns):
        for item in eqtns:
            self.append(pylatex.Math(data=item, escape=False))


class Exam:
    """docstring for Exam"""

    def __init__(self):
        self.q_paper = Paper()
        self.q_paper.append(pylatex.NoEscape(r'\twocolumn'))
        self.a_paper = Paper()

    def add_questions(self, *args):
        assert all((isinstance(item, Question) for item in args))
        for item in args:
            item.write(self.q_paper, self.a_paper)

    def export(self, filename='output\\test'):
        self.q_paper.generate_pdf(filename + '_questions')
        self.a_paper.generate_pdf(filename + '_answers')
