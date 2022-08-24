import pytest
from app.calculator import Calculator

@pytest.mark.parametrize("numbers, expected_value", [([1,2,3],6), ([2,4,6], 48), ([1,1,1,1], 1), ([0], 0)])
def test_multiply_method(numbers, expected_value):
    result = Calculator.multiply(numbers)
    assert result == expected_value