from pyjexl.operators import binary_operators
from pyjexl.parser import BinaryExpression, JEXLVisitor, Literal


def op(operator):
    return binary_operators[operator]


def test_literal():
    assert JEXLVisitor().parse('1') == Literal(1.0)


def test_binary_expression():
    assert JEXLVisitor().parse('1+2') == BinaryExpression(
        operator=op('+'),
        left=Literal(1),
        right=Literal(2)
    )


def test_binary_expression_priority_right():
    assert JEXLVisitor().parse('2+3*4') == BinaryExpression(
        operator=op('+'),
        left=Literal(2),
        right=BinaryExpression(
            operator=op('*'),
            left=Literal(3),
            right=Literal(4),
        )
    )


def test_binary_expression_priority_left():
    assert JEXLVisitor().parse('2*3+4') == BinaryExpression(
        operator=op('+'),
        left=BinaryExpression(
            operator=op('*'),
            left=Literal(2),
            right=Literal(3),
        ),
        right=Literal(4)
    )


def test_binary_expression_encapsulation():
    assert JEXLVisitor().parse('2+3*4==5/6-7') == BinaryExpression(
        operator=op('=='),
        left=BinaryExpression(
            operator=op('+'),
            left=Literal(2),
            right=BinaryExpression(
                operator=op('*'),
                left=Literal(3),
                right=Literal(4)
            ),
        ),
        right=BinaryExpression(
            operator=op('-'),
            left=BinaryExpression(
                operator=op('/'),
                left=Literal(5),
                right=Literal(6)
            ),
            right=Literal(7)
        )
    )
