import pytest

from calculator import Calculator
from calculator.nodes import _Negation, _Node, _Number, _Operation
from calculator.parser import _Parser


@pytest.fixture
def calculator():
    return Calculator("2 + 3 * 4")


@pytest.mark.parametrize("expression, expected", [
    ("003.50", 3.5),
    ("20 - 5 - 3", 12),
    ("24 / 4 * 2", 12),
    ("24 / (4 / 2)", 12),
    ("2 * (3 + (4 * 5)) - 6 / 2", 43),
    ("-0.2 * 0.3", pytest.approx(-0.06)),
    ("-(2 + 0.3)", pytest.approx(-2.3)),
    ("2--3", 5),
    ("9007199254740993 - 9007199254740992", 1),
])
def test_calculate(expression, expected):
    assert Calculator(expression).calculate() == expected


@pytest.mark.parametrize("expression", [
    "", " \t\n", "()", "(", ")", "(1 + 2", "1 + 2)",
    "2 3", "2(3)", "(2)(3)", "1 +", "*1", "1 + * 2", "+2",
    "1 ** 2", "1 // 2", "2 % 3", ".5", "5.", "1.2.3", "1e3",
    "abc", "1 + spam", "1 + 2xyz", "1\x00+2",
])
def test_invalid_syntax_is_rejected(expression):
    with pytest.raises(ValueError):
        Calculator(expression)


def test_update_preserves_text_and_instance_isolation(self, calculator):
    other = Calculator("6 * 7")
    expression = " \t(10 - 4)\u00a0/ 3\n"
    calculator.expression = expression
    assert calculator.expression == expression
    assert calculator.calculate() == 2
    assert other.expression == "6 * 7"
    assert other.calculate() == 42

@pytest.mark.parametrize("value, error", [
    (None, TypeError), ("", ValueError), ("1 +", ValueError),
])
def test_failed_update_preserves_state(calculator, value, error):
    with pytest.raises(error):
        calculator.expression = value
    assert calculator.expression == "2 + 3 * 4"
    assert calculator.calculate() == 14

@pytest.mark.parametrize("expression", ["1 / 0", "1 / (2 - 2)"])
def test_division_by_zero_and_recovery(calculator, expression):
    calculator.expression = expression
    with pytest.raises(ZeroDivisionError):
        calculator.calculate()
    calculator.expression = "6 * 7"
    assert calculator.calculate() == 42


def test_calculate_reuses_parsed_tree(calculator, monkeypatch):
    def unexpected_parse():
        pytest.fail("calculate() should reuse the existing parsed expression")

    monkeypatch.setattr(_Parser, "parse", unexpected_parse)
    assert calculator.calculate() == 14
    assert calculator.calculate() == 14


def test_python_code_is_rejected_without_creating_a_file(tmp_path):
    path = tmp_path / "should_not_exist.txt"
    expression = f"__import__('pathlib').Path({str(path)!r}).touch()"
    with pytest.raises(ValueError):
        Calculator(expression)
    assert not path.exists()
