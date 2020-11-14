
# geo = {"top":"3.5cm","bottom":"3.5cm", "left":"3.7cm",
#        "right":"4.5cm", "columnsep":"30pt"}
# qPaper = pylatex.Document(geometry_options=geo)
# qPaper.append(pylatex.NoEscape(r'\twocolumn'))

from MathSheets.exam import Exam
from MathSheets.questions import Differenciate

exam = Exam()
exam.add_questions(Differenciate(20))
exam.export()
