
class Value:
    """ The fundamental unit of expressions

       Value objects denote anything that could go inside an equation.
       Eg.
       - The variable 'x'
       - The integer '3'
       - The expression 'x + 3'

       All objects are defined to have a string representation
       which can be parsed by sympy
    """

    def __init_subclass__(cls, *args, **kwargs):
        assert hasattr(cls, "__str__")
        return super().__init_subclass__(*args, **kwargs)


class Variable(Value):
    """docstring for Variable"""

    def __init__(self, letter=None):
        self.letter = letter

    def __str__(self):
        if self.letter:
            return self.letter
        return 'x'

    def __eq__(self, other):
        if isinstance(other, Variable):
            return any([
                None in {self.letter, other.letter},
                self.letter == other.letter
            ])
        return False
