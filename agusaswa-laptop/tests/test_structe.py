'''This module is for testing.'''
import structe
import pytest 

def test_store_correct_inp() -> None:
    '''This is for testing that the line load is stored.'''
    testing_dicts = structe.store_load("DL1_line","dead", "line", 50)
    assert testing_dicts["name"] == "DL1_line"
    assert testing_dicts["nature"] == "dead"
    assert testing_dicts["load_type"] == "line"
    assert testing_dicts["load_val"] == 50


def test_store_wrong_nature_par() -> None:
    with pytest.raises(ValueError):
        structe.store_load("DL1_line","wind", "line", 100)

def test_store_wrong_load_type_par() -> None:
    with pytest.raises(ValueError):
        structe.store_load("DL1_line","imposed", "triangular", 100)

def test_store_wrong_load_value_type() -> None:
    with pytest.raises(TypeError):
        structe.store_load("DL1_line","imposed", "point", "one hundred")

def test_store_negative_load_value_type() -> None:
    with pytest.raises(ValueError) as error:
        structe.store_load("DL1_line","imposed", "point", -20)
    assert str(error.value) == "Invalid input value! Value cannot be negative."

if __name__ == "__main__":
    pytest.main(["-vv"])