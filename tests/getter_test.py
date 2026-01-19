import pytest
import pandas as pd
import numpy as np

from suntzu.getter import Getter  
@pytest.fixture
def intiate_dataframe():

    df = pd.DataFrame({
        "A": [160, 2, 3],
        "B": [1.0, 2.0, 3.0],
        "C": ["a", "b", "a"],
    })
    return df
@pytest.mark.parametrize(
    "col_min, col_max, expected",
    [
        (-100, 100, "int8"),
        (-128, 127, "int8"),
        (-200, 200, "int16"),
        (-32768, 32767, "int16"),
        (-50000, 50000, "int32"),
        (-2147483648, 2147483647, "int32"),
        (-3000000000, 3000000000, "int64"),
    ]
)
def test_best_int_type(col_min, col_max, expected):
    assert Getter.get_best_int(col_min, col_max) == expected
@pytest.mark.parametrize(
    "col_min, col_max, expected",
    [
        (0.0, 100.0, "float16"),
        (np.finfo(np.float16).min, np.finfo(np.float16).max, "float16"),
        (np.finfo(np.float32).min, np.finfo(np.float32).max, "float32"),
        (-1e40, 1e40, "float64"),
    ]
)
def test_best_float_type(col_min, col_max, expected):
    assert Getter.get_best_float(col_min, col_max) == expected
def test_get_best_dtypes(intiate_dataframe):
    expected_outputs = ["int16", "float16", "category"]
    i = 0
    for col in intiate_dataframe.columns:
        assert Getter.get_best_dtype(intiate_dataframe, col) == expected_outputs[i]
        i += 1
def test_get_max_value(intiate_dataframe):
    expected_outputs = [160, 3.0, "a"]
    i = 0
    for col in intiate_dataframe.columns:
        assert Getter.get_max_value(intiate_dataframe, col) == expected_outputs[i]
        i += 1
def test_get_min_value(intiate_dataframe):
    expected_outputs = [2, 1.0, "b"]
    i = 0
    for col in intiate_dataframe.columns:
        assert Getter.get_min_value(intiate_dataframe, col) == expected_outputs[i]
        i += 1