import pytest
from calculator import Calculator
import sys


@pytest.fixture()
def calculator():
    return Calculator("2 + 3 * 4")


@pytest.mark.parametrize("expression, expected", [
    ("003.50", 3.5),
    ("24 / ( \t(10 - 4)/ 3\n)", pytest.approx(12)), # / converts to float
    ("2 * (3 + (4 * 5)) - 6 / 2", pytest.approx(43)),
    ("-0.2 * 0.3", pytest.approx(-0.06)),
    ("-(2 + 0.3)", pytest.approx(-2.3)),
    ("2--3", 5),
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


def test_failed_update_preserves_state(calculator):
    with pytest.raises(ValueError):
        calculator.expression = "1 +"
    assert (calculator.expression, calculator.calculate()) == ("2 + 3 * 4", 14)


def test_python_code_is_rejected_without_creating_a_file(tmp_path):
    path = tmp_path / "should_not_exist.txt"
    expression = f"__import__('pathlib').Path({str(path)!r}).touch()"
    with pytest.raises(ValueError):
        Calculator(expression)
    assert not path.exists()


@pytest.mark.parametrize("expression", [
    "(" * (sys.getrecursionlimit()+1) + "1" + ")" * (sys.getrecursionlimit()+1),
    "+".join(["1"] * (sys.getrecursionlimit()+1)),
    ], ids=["parentheses", "operators"])
@pytest.mark.xfail(
    raises=RecursionError, strict=True,
    reason="Recursive parsing/evaluation exceeds Python's recursion limit",
)
def test_very_deep_expressions(expression):
    Calculator(expression).calculate()
