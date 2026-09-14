import pytest

from calculator import Calculator


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("1 + 2", 3),
        ("5 - 2", 3),
        ("3 * 4", 12),
        ("8 / 2", 4),
        ("2 + 3 * 4", 14),       # precedence
        ("(2 + 3) * 4", 20),     # parentheses
        ("2.5 + 0.5", 3),        # decimals
    ],
)
def test_basic_calculations(expression, expected):
    result = Calculator(expression).calculate()
    assert result == pytest.approx(expected)


def test_expression_must_be_string():
    with pytest.raises(TypeError, match="expression must be string"):
        Calculator(123)


def test_expression_can_be_updated():
    calculator = Calculator("1 + 1")

    calculator.expression = "10 / 2"

    assert calculator.calculate() == 5


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        Calculator("1 / 0").calculate()