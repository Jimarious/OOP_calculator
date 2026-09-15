from .parser import _Parser

class Calculator:
    def __init__(self, expression):
        self.expression = expression
    
    @property   # update expression only after the string check
    def expression(self):
        return self._expression
    
    @expression.setter
    def expression(self, expression):
        if not isinstance(expression, str):
            raise TypeError("expression must be string")
        self._root = _Parser(expression).parse()
        self._expression = expression

    def calculate(self):
        return self._root.evaluate()

# TODO: Maybe count recursion depth
# TODO: Is there any built in recursion depth variable you could use?