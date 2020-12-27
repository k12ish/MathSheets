from MathSheets.exam import Exam
from MathSheets.questions import Differentiate, MatrixInverse
from MathSheets.questions import ExpandCubic


exam = Exam()
exam.add_questions(
    Differentiate(10),
    Differentiate(10),
    MatrixInverse(10),
    ExpandCubic(10)
)
exam.export()
