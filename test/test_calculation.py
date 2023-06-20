import pytest
from app.calculation import add

@pytest.mark.parametrize("num1,num2,expected",[(2,3,5),(8,9,17),(12,6,18)])
def test_add(num1,num2,expected):
    print("testing add function")
    assert add(num1,num2) == expected
    