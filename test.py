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
    return str(base)


geo = {"top":"3.5cm","bottom":"3.5cm", "left":"3.7cm",
       "right":"4.5cm", "columnsep":"30pt"}
qPaper = pylatex.Document(geometry_options=geo)
qPaper.append(pylatex.NoEscape(r'\twocolumn'))


for i in range(20):
    env = qPaper.create(
        pylatex.Alignat(aligns=1, numbering=True, escape=False)
    )
    with env as env:
        env.append(sp.latex(parse_expr(ret_eqtn())) + '\n\\\\')
        env.append(sp.latex(parse_expr(ret_eqtn())) + '\n\\\\')
        env.append(sp.latex(parse_expr(ret_eqtn())) + '\n\\\\')
        env.append(sp.latex(parse_expr(ret_eqtn())) + '\n\\\\')
        env.append(sp.latex(parse_expr(ret_eqtn())))

qPaper.generate_pdf('output\\test')
