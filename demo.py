from MathSheets.exam import Exam
from MathSheets.questions import Differentiate, MatrixInverse, ExpandPolynomial


exam = Exam()
exam.add_questions(
    Differentiate(10),
    MatrixInverse(10),
    ExpandPolynomial(10)
)
exam.export()
