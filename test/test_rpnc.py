import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# sys.path.append('..')  # Add parent directory to Python path
from rpnc import RPNCalculator, getch

@pytest.fixture
def calculator():
    return RPNCalculator()

def test_push_and_pop(calculator):
    calculator.push(5)
    calculator.push(3)
    assert calculator.pop() == 3
    assert calculator.pop() == 5
    assert calculator.pop() == 0  # Empty stack should return 0

@pytest.mark.parametrize("a, b, op, result", [
    (5, 3, '+', 8),
    (5, 3, '-', 2),
    (5, 3, '*', 15),
    (6, 2, '/', 3),
    (2, 3, '^', 8),
    (7, 3, '%', 1)
])
def test_arithmetic_operations(calculator, a, b, op, result):
    calculator.push(a)
    calculator.push(b)
    calculator.perform_operation(op)
    assert calculator.pop() == result

def test_unary_operations(calculator):
    # Test rounding
    calculator.push(3.14159)
    calculator.perform_operation('r')
    assert calculator.pop() == 3

    # Test negation
    calculator.push(5)
    calculator.perform_operation('n')
    assert calculator.pop() == -5

def test_swap(calculator):
    calculator.push(1)
    calculator.push(2)
    calculator.swap()
    assert calculator.pop() == 1
    assert calculator.pop() == 2

def test_clear_screen(calculator, capsys):
    calculator.clear_screen()
    captured = capsys.readouterr()
    assert "\033[2J\033[H" in captured.out

def test_display(calculator, capsys):
    calculator.push(1)
    calculator.push(2)
    calculator.display()
    captured = capsys.readouterr()
    assert "2: 1" in captured.out
    assert "1: 2" in captured.out

@pytest.mark.parametrize("input_value, expected", [
    ("5", 5),
    ("3.14", 3.14),
    ("2+3j", 2+3j),
    ("invalid", None),
    ("[1,2,3]", None),
    ("1e6", 1000000.0),
    ("-7", -7),
    ("0", 0),
])
def test_push_with_various_inputs(calculator, input_value, expected):
    if expected is None:
        with pytest.raises(ValueError) as exc_info:
            calculator.push(input_value)
        assert "Invalid input" in str(exc_info.value)
    else:
        calculator.push(input_value)
        assert calculator.stack[-1] == expected

def test_run(calculator, monkeypatch):
    inputs = iter(['5', '\r', '3', '\r', '+', 'q'])
    monkeypatch.setattr('rpnc.getch', lambda: next(inputs))
    
    with pytest.raises(SystemExit):
        calculator.run()
    
    assert calculator.pop() == 8

# More tests can be added to cover all methods and edge cases

