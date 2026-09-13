from nodes import Number, BinaryOperation

def test_evaluate():
    result_calculator = BinaryOperation('*',
        BinaryOperation('+', Number(2), Number(3)),
        BinaryOperation('-', Number(10), Number(4))
    ).evaluate()

    result_control = (2 + 3) * (10 - 4)
    assert result_calculator == result_control


"""
evaluate:
+  -  *  x  /  ^

tree traversal:
postfix()
preorder()

validation:
Number("hello")           -> error
Number(float("inf"))      -> error
BinaryOperation("%", ...) -> error
BinaryOperation("+", 1, Number(2)) -> error
"""

"""
while(1) {
    # mathematical in, not python
    if c in whitespace: continue
    if c in {+,-,...}: list <- list + c
    if c in int
}
"""