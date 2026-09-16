import pytest
from calculator import Calculator
import sys


@pytest.fixture
def deep_expressions():
    n = sys.getrecursionlimit()
    return "(" * n + "1" + ")" * n, "+".join(["1"] * n)


@pytest.mark.parametrize("expression, expected", [
    ("003.50", 3.5),
    ("24 / ( \t(10 - 4)/ 3\n)", pytest.approx(12)), # / converts to float
    ("2 * (3 + (4 * 5)) - 6 / 2", pytest.approx(43)),
    ("-0.2 * 0.3", pytest.approx(-0.06)),
    ("-(2 + 0.3)", pytest.approx(-2.3)),
    ("2--3", 5),
    # float => problem, int: arbitrary precision
    ("9007199254740993 - 9007199254740992", 1), 
])
def test_calculate(expression, expected):
    assert Calculator(expression).calculate() == expected


@pytest.mark.parametrize("expression", [
    "", " \t\n", "()", "(", ")", "(1 + 2", "1 + 2)",
    "2 3", "2(3)", "(2)(3)", "1 +", "*1", "1 + * 2",
    "1 ** 2", "2 % 3", ".5", "5.", "1.2.3",
    "abc", "1 + 2xyz", "1\x00+2",
])
def test_invalid_syntax_is_rejected(expression):
    with pytest.raises(ValueError):
        Calculator(expression)


def test_failed_update_preserves_state():
    with pytest.raises(ValueError):
        calculator = Calculator("2 + 3 * 4")
        calculator.expression = "1 +"
    assert (calculator.expression, calculator.calculate()) == ("2 + 3 * 4", 14)


xfail = pytest.mark.xfail(raises=RecursionError, strict=True)
@pytest.mark.parametrize("i, calculate", [
    pytest.param(0, False, marks=xfail, id="parentheses"),
    pytest.param(0, True,  marks=xfail, id="parentheses-calculate"),
    pytest.param(1, False,              id="operators"),
    pytest.param(1, True,  marks=xfail, id="operators-calculate"),
])
def test_very_deep_expressions(deep_expressions, i, calculate):
    calculator = Calculator(deep_expressions[i])
    if calculate:
        calculator.calculate()