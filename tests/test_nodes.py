import pytest
from calculator import Operation, Node, Number


@pytest.mark.parametrize(
    ("node", "value"),
    [
        (Number(5), 5),
        (Operation("+", Number(2), Number(3)), 5),
        (
            Operation("*", Operation("+", Number(2), Number(3)), Number(4)),
            20,
        ),
    ],
)
def test_polymorphic_node_interface(node: Node, value):
    # Evaluation works for every concrete node type.
    assert node.evaluate() == value


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_number_rejects_non_finite_values(value):
    with pytest.raises(ValueError, match="inf"):
        Number(value)


@pytest.mark.parametrize("value", [True, False, "3", None, 1j])
def test_number_rejects_non_numeric_values(value):
    with pytest.raises(TypeError):
        Number(value)


@pytest.mark.parametrize("operator", ["%", "**", "", "add"])
def test_operation_rejects_unknown_operator(operator):
    with pytest.raises(ValueError, match="operator"):
        Operation(operator, Number(1), Number(2))


@pytest.mark.parametrize("left,right", [(1, Number(2)), (Number(1), None)])
def test_operation_requires_node_children(left, right):
    with pytest.raises(TypeError, match="Node"):
        Operation("+", left, right)


@pytest.mark.parametrize("attribute", ["operator", "left", "right"])
def test_operation_properties_are_read_only(attribute):
    operation = Operation("+", Number(1), Number(2))
    with pytest.raises(AttributeError):
        setattr(operation, attribute, None)
    assert operation.evaluate() == 3


@pytest.mark.parametrize("operator", ["+", "*", "/"])
def test_non_finite_results_are_rejected(operator):
    right = Number(1e-308 if operator == "/" else 1e308)
    with pytest.raises(ArithmeticError):
        Operation(operator, Number(1e308), right).evaluate()


def test_new_node_subclass_works_without_changing_binary_operation():
    class Answer(Node):
        def evaluate(self) -> float:
            return 42.0

    operation = Operation("+", Answer(), Number(1))
    assert operation.evaluate() == 43



# TODO: Remake