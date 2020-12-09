import pylatex
from MathSheets.questions import Question


class EquationEnvironment(pylatex.base_classes.Environment):
    """docstring for EquationEnvironment"""
    _latex_name = 'equation'
    packages = [pylatex.package.Package('amsmath')]


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
    """Exam objects store the relevant questions and answers"""

    def __init__(self):
        geo = {"top":"3.5cm","bottom":"3.5cm", "left":"3.7cm",
               "right":"4.5cm", "columnsep":"30pt"}
        self.q_paper = Paper(geometry_options=geo)
        self.q_paper.append(pylatex.NoEscape(r'\twocolumn'))
        self.a_paper = Paper(geometry_options=geo)

    def add_questions(self, *args):
        assert all((isinstance(item, Question) for item in args))
        for item in args:
            item.write(self.q_paper, self.a_paper)

    def export(self, filename='output\\test'):
        self.q_paper.generate_pdf(filename + '_questions')
        self.a_paper.generate_pdf(filename + '_answers')
