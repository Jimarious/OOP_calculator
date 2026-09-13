import re
from nodes import Node, BinaryOperation, Number

NUMBER = r"\d+(?:\.\d+)?"

class Parser:
    # parser can only be used once, additional methods can change that
    def __init__(self, expression) -> None: # __init__ just configures self => no rv
        self._tokens = re.findall(NUMBER + r"|[*x/+\-^()]|\S", expression)
        self._token_idx = 0

    def _peek(self) -> str | None:
        if self._token_idx < len(self._tokens):
            return self._tokens[self._token_idx+1]
        return None

    def _take(self) -> str:
        token = self._peek()
        if token != None:
            self._token_idx += 1
            return token
        raise ValueError("expression ends in +,-,*,x,/,^ or (")
        # raised in _parse_atom: +-*x/^ from 1st call or ( from 2nd top down

    def parse(self) -> Node:
        if self._tokens is None:
            raise ValueError("expression is empty")
        root = self._parse_sum(self._tokens)
        if self._peek() is not None:
            raise ValueError(f"expression contained {self._peek()!r}")
        return root

    def _parse_sum(self) -> Node:
        self._parse_product()
        while (operator := self._peek) in ['+','-']:
            self._token_idx += 1
            node = BinaryOperation(operator, node, self._parse_product)
        return node

    def _parse_product(self) -> Node:
        self._parse_power()
        while (operator := self._peek) in ['*','/','x']:
            self._token_idx += 1
            node = BinaryOperation(operator, node, self._parse_power)
        return node

    def _parse_power(self) -> Node:
        self._parse_atom()
        while (operator := self._peek) == '^':
            self._token_idx += 1
            node = BinaryOperation(operator, node, self._parse_atom)
        return node

    def _parse_atom(self) -> Node:
        if (token := self._take()) == '(':
            node = self._parse_sum()
            if self.take() == ')': return node
            raise ValueError("expression missing closing )")
        else:
            if re.fullmatch(NUMBER, token):
                return Number(float(token))
            raise ValueError(f"in expression expected number or (, got {token!r}")