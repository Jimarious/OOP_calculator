from re import findall, fullmatch
from .nodes import _Operation, _Number, _Negation

FLOAT = r"\d+\.\d+"
INT = r"\d+"


class _Parser:
    def __init__(self, expression):
        self._tokens = findall(rf"{FLOAT}|{INT}|[*/+\-()]|\S", expression)
        self._token_idx = 0

    def _peek(self):
        if self._token_idx < len(self._tokens):
            return self._tokens[self._token_idx]
        return None

    def _take(self):
        token = self._peek()
        if token != None:
            self._token_idx += 1
            return token
        raise ValueError("expression ends in +,-,*,/ or (")
        # raised in _parse_atom: +-*/ from 1st call or ( from 2nd top down

    def parse(self):
        if self._peek() is None:
            raise ValueError("expression is empty")
        root = self._parse_sum()
        if self._peek() is not None:
            raise ValueError(f"expression contained {self._peek()!r}")
        return root

    def _parse_sum(self):
        node = self._parse_product()
        while (operator := self._peek()) in ['+','-']:
            self._token_idx += 1
            node = _Operation(operator, node, self._parse_product())
        return node

    def _parse_product(self):
        node = self._parse_atom()
        while (operator := self._peek()) in ['*','/']:
            self._token_idx += 1
            node = _Operation(operator, node, self._parse_atom())
        return node

    def _parse_negation(self):
        print("_parse_negation:", self._tokens, self._token_idx)
        return _Negation(self._parse_atom())

    def _parse_atom(self):
        if (token := self._take()) == '-': return self._parse_negation()
        if token == '(':
            node = self._parse_sum()
            if self._take() == ')': return node
            raise ValueError("expression missing closing )")
        else:
            if fullmatch(FLOAT, token):return _Number(float(token))
            if fullmatch(INT, token): return _Number(int(token))
            raise ValueError(f"in expression expected number or (, got {token!r}")

