from MathSheets.exam import Exam
from MathSheets.questions import Differenciate
from MathSheets.questions import MatrixInverse


exam = Exam()
exam.add_questions(
    Differenciate(20),
    MatrixInverse(10)
)
exam.export()
