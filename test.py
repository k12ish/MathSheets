import pprint
import copy
import sympy as sp
import pylatex
from sympy.parsing.sympy_parser import parse_expr

import MathSheets.expressions
sim = MathSheets.expressions.simple


def ret_eqtn():
    base = copy.copy(sim.pick())
    for i in range(2):
        pprint.pprint(base.asdict())
        base.substitute(copy.copy(sim.pick()))
        base.rebuild()
    return str(base)


geo = {"top":"3.5cm","bottom":"3.5cm", "left":"3.7cm",
       "right":"4.7cm", "columnsep":"30pt"}
qPaper = pylatex.Document(geometry_options=geo)
qPaper.append(pylatex.NoEscape(r'\twocolumn'))
for i in range(100):
    eqtn = parse_expr(ret_eqtn())
    LaTeX = sp.latex(eqtn)
    qPaper.append(pylatex.Math(data=LaTeX, escape=False))
qPaper.generate_pdf('output\\test')
