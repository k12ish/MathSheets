import pylatex


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
    Eg:
    class Simplify(EquationListQuestion):
        _question_title = "Simplification"
        _question_prompt = "Simplify the following:"
        _answer_title = "Simplification"
        _answer_prompt = ""
        def _build_questions_answers(self):
            pass
        def _new_expr(self):
            pass
    """
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
