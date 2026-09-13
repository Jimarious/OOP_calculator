from abc import ABC, abstractmethod
import math

class Node(ABC):
    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def postfix(self):
        pass

    @abstractmethod
    def preorder(self):
        pass

class Number(Node):
    def __init__(self, value):
        # (bool is child of int)
        # type(value) not in {int, float}: would have removed the need to check for bool
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError("Number <- non numeric value")
        if not math.isfinite(value):
            raise ValueError("Number <- +-inf or nan")
        self._value = value

    def evaluate(self):
        return self._value


class BinaryOperation(Node):
    def __init__(self, operator, node1, node2):
        # errors in checklist form:
        if not isinstance(node1, Node) or not isinstance(node2, Node):
            raise TypeError("Invalid Operand Type")
        if not isinstance(operator, str):
            raise TypeError("operator <- not a string")
        if operator not in "+-*x/^" or len(operator) != 1:
            raise ValueError("operator <- not +,-,*,x,/ or ^")
        self._operator = operator
        self._node1 = node1
        self._node2 = node2

    def evaluate(self):
        left = self._node1.evaluate()
        right = self._node2.evaluate()
        match self._operator:
            case '+':
                return left + right
            case '-':
                return left - right
            case '*' | 'x':
                return left * right
            case '/':
                return left / right
            case '^':
                return left ** right




# TODO: Maybe find more edge cases for the original tests or automate them further