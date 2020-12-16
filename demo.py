from MathSheets.exam import Exam
from MathSheets.questions import Differentiate, MatrixInverse, SimplifyPolynomial


exam = Exam()
exam.add_questions(
    Differentiate(20),
    MatrixInverse(10),
    SimplifyPolynomial(10)
)
exam.export()
