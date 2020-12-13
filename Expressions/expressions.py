from Expressions.core import Variable, OneFrom, Expression
from Expressions.constants import Integer


class Trig:
    """docstring for Trig"""

    @staticmethod
    def sin(v=Variable()):
        return Expression('sin({})', [v])

    @staticmethod
    def cos(v=Variable()):
        return Expression('cos({})', [v])

    @staticmethod
    def tan(v=Variable()):
        return Expression('tan({})', [v])

    @staticmethod
    def sec(v=Variable()):
        return Expression('sec({})', [v])

    @staticmethod
    def cot(v=Variable()):
        return Expression('cot({})', [v])

    @staticmethod
    def csc(v=Variable()):
        return Expression('csc({})', [v])

    @staticmethod
    def standard():
        return (Trig.sin(), Trig.cos(), Trig.tan())

    @staticmethod
    def all():
        return (Trig.sin(), Trig.cos(), Trig.tan(),
                Trig.csc(), Trig.sec(), Trig.cot())

    @staticmethod
    def reciprocal():
        return (Trig.csc(), Trig.sec(), Trig.cot())


class Poly:
    """docstring for Poly"""
    @staticmethod
    def linear(v=Variable(), i=Integer().non_zero()):
        return Expression('{}*{} + {}', [i, v, i])

    @staticmethod
    def quadratic(v=Variable(), i=Integer().non_zero()):
        return Expression('{}*({})**2 + {}*({}) + {}', [i, v, i, v, i])


v = Variable()
i = Integer().non_zero()

exp = Expression('e**{}', [v])
ln = Expression('ln({})', [v])

lin = Expression('{}*{} + {}', [i, v, i])
expon = Expression('({})**{}', [v, i])
inv = Expression('1/{}', [v])

simple = OneFrom(
    exp, ln, inv, *Trig.standard(), lin, Trig.reciprocal(), expon
)
