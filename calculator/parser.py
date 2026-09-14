from re import findall, fullmatch
from .nodes import Node, Operation, Number

NUMBER = r"\d+(?:\.\d+)?"

class Parser:
    def __init__(self, expression):
        self._tokens = findall(NUMBER + r"|[*/+\-()]|\S", expression)
        self._token_idx = 0

    def _peek(self):
        if self._token_idx < len(self._tokens):
            return self._tokens[self._token_idx+1]
        return None

    def _take(self):
        token = self._peek()
        if token != None:
            self._token_idx += 1
            return token
        raise ValueError("expression ends in +,-,*,/ or (")
        # raised in _parse_atom: +-*/ from 1st call or ( from 2nd top down

    def parse(self):
        if self._tokens is None:
            raise ValueError("expression is empty")
        root = self._parse_sum(self._tokens)
        if self._peek() is not None:
            raise ValueError(f"expression contained {self._peek()!r}")
        return root

    def _parse_sum(self):
        self._parse_product()
        while (operator := self._peek) in ['+','-']:
            self._token_idx += 1
            node = Operation(operator, node, self._parse_product)
        return node

    def _parse_product(self):
        self._parse_power()
        while (operator := self._peek) in ['*','/']:
            self._token_idx += 1
            node = Operation(operator, node, self._parse_power)
        return node

    def _parse_atom(self):
        if (token := self._take()) == '(':
            node = self._parse_sum()
            if self.take() == ')': return node
            raise ValueError("expression missing closing )")
        else:
            if fullmatch(NUMBER, token):
                return Number(float(token))
            raise ValueError(f"in expression expected number or (, got {token!r}")