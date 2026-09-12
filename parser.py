import re
from nodes import Node, BinaryOperation

NUMBER = r"\d+(?:\.\d+)?"

class Parser:
    def __init__(self, expression):
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
        # _parse_atom: +-*x/^ from 1st call or ( from 2nd through all

    def _parse_sum(self) -> Node:
        self._parse_product()
        while (operator = self._peak) in ['+', '-']:
            self._token_idx += 1
            node = BinaryOperation(operator, node, self._parse_product)

    def _parse_product(self) -> Node:
        self._parse_power()
        while 


    def _parse_power(self) -> Node:
        self._parse_atom()

    def _parse_atom(self) -> Node:


# Q: __init__ does not return anything, right?
# TODO: What if we input an empty string to the parser?