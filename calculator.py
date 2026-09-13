import 

class Calculator:
    def __init__(self, expression):
        self.expression = expression
    
    @property
    def expression():
        return self._expression
    
# property and setter, to update expression only through the string check
    @expression.setter
    def expression()
        if not isinstance(expression, str):
            raise TypeError("expression must be string")

    def set_expression(self, expression)
        self._root = Parser(expression).parse()

    def evaluate(self)
        return self._root.evaluate()


# How do setters work exactly