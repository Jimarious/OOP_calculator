from abc import ABC, abstractmethod


class _Node(ABC): # not required for polymorphism
    @abstractmethod
    def evaluate(self):
        pass


class _Number(_Node):
    def __init__(self, value):
        # Already handled by Parser, just to showcase the catch with isinstance
        # type(value) not in {int, float}: would have removed the need to check for bool
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError("_Number <- non numeric value")
        self._value = value

    def evaluate(self):
        return self._value


class _Operation(_Node):
    def __init__(self, operator, node1, node2):
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
            case '*':
                return left * right
            case '/':
                return left / right


class _Negation(_Node):
    def __init__(self, node):
        self._node = node

    def evaluate(self):
        return -self._node.evaluate()