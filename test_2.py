"""
import pytest
from calculator import Calculator

@pytest.fixture
def calculator():
    return Calculator("...").calculate()

# write a parametrize and check floats and precision
@pytest.mark.parametrize(("expression", "value"), [
    ("0.2+0.3",pytest.approx(0.5))
    ])
2^

"""
# write some invalid syntax

# state after failed update

# demonstrate_fixture_session

# test_python_code_is_rejected_without_creating_a_file

# TODO: What with does exactly