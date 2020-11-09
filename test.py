from MathSheets.helpers import Integer
from MathSheets.core import Expression

import pprint
import sympy as sp
import pylatex
from sympy.parsing.sympy_parser import parse_expr


i = Integer().non_zero()
x = Expression('{}*x + {}', [i, i])
y = Expression('{}*e**{}', [i, x])
y = Expression('{}*e**{}', [x, y])
y.rebuild()

pprint.pprint(y.asdict())
eqtn = parse_expr(str(y))


geo = {"top":"3.5cm","bottom":"3.5cm", "left":"3.7cm",
       "right":"4.7cm", "columnsep":"30pt"}
qPaper = pylatex.Document(geometry_options=geo)
qPaper.append(pylatex.NoEscape(r'\twocolumn'))
LaTeX = sp.latex(eqtn)
qPaper.append(pylatex.Math(data=LaTeX, escape=False))
qPaper.generate_pdf('output\\test')