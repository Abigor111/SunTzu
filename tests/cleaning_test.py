import pytest
import pandas as pd

from suntzu.cleaning import Cleaning
from suntzu.getter import Getter

@pytest.fixture
def intiate_dataframe():
    df = pd.DataFrame({
        "nAmE": ["John", "Roderick", "Anne", "Kevin"],
        "aGE": [25.36123, 29.62313, 30.1484, 40.57161],
        "Favourite_Sport": ["football", "tennis", "football", "football"],
        "HasAJob": ["yes", "no", "yes", "yes"],
        "IsMarried": [pd.NA, "yes", "yes", "no"],
        "IncomeInMilions": [4, 5, 6, 11]
    })
    return df

@pytest.mark.parametrize(
    "cols, action, expected_output",
    [
        # capitalize
        (None, "capitalize", ["Name", "Age", "Favourite_sport", "Hasajob", "Ismarried", "Incomeinmilions"]),
        (["aGE"], "capitalize", ["Age"]),
        (["nAmE", "aGE"], "capitalize", ["Name", "Age"]),

        # upper
        (None, "upper", ["NAME", "AGE", "FAVOURITE_SPORT", "HASAJOB", "ISMARRIED", "INCOMEINMILIONS"]),
        (["aGE"], "upper", ["AGE"]),
        (["nAmE", "aGE"], "upper", ["NAME", "AGE"]),

        # lower
        (None, "lower", ["name", "age", "favourite_sport", "hasajob", "ismarried", "incomeinmilions"]),
        (["aGE"], "lower", ["age"]),
        (["nAmE", "aGE"], "lower", ["name", "age"]),
    ]
)
def test_transform_cols_name(intiate_dataframe, cols, action, expected_output):
    result = Cleaning.transform_cols_name(intiate_dataframe, cols, action)
    assert set(expected_output).issubset(result.columns)
@pytest.mark.parametrize(
    "decimals, expected_output",
    [
        (1, [25.4, 29.6, 30.1, 40.6]),
        (2, [25.36, 29.62, 30.15, 40.57]),
        (3, [25.361, 29.623, 30.148, 40.572])
    ]
)
def test_round_rows_value(intiate_dataframe, decimals, expected_output):
    result = Cleaning.round_rows_value(intiate_dataframe, ["aGE"], decimals)
    assert result["aGE"].to_list() == expected_output

def test_convert_float_cols_to_int(intiate_dataframe):
    result = Cleaning.convert_float_cols_to_int(intiate_dataframe, ["aGE"])
    assert result["aGE"].to_list() == [25, 30, 30, 41]
    assert "int" in result["aGE"].dtype.name

def test_convert_to_best_dtypes(intiate_dataframe):
    
    total_usage_before = Getter.get_total_memory_usage(intiate_dataframe, "kb")
    df = Cleaning.convert_float_cols_to_int(intiate_dataframe, ["aGE"])
    result = Cleaning.convert_to_best_dtypes(df, ["aGE"])
    total_usage_after = Getter.get_total_memory_usage(result, "kb")
    assert total_usage_before > total_usage_after
    
def test_convert_binary_to_bool(intiate_dataframe):
    result = Cleaning.convert_binary_to_bool(intiate_dataframe, "HasAJob", false_value="no", true_value="yes")
    assert result["HasAJob"].to_list() == [True, False, True, True]
    
    
def test_cleaning(intiate_dataframe):
    total_usage_before = Getter.get_total_memory_usage(intiate_dataframe, "kb")
    df = Cleaning.round_rows_value(intiate_dataframe, ["aGE"], 1)
    assert df["aGE"].to_list() == [25.4, 29.6, 30.1, 40.6]
    
    df = Cleaning.convert_binary_to_bool(df, "HasAJob", false_value="no", true_value="yes")
    assert df["HasAJob"].to_list() == [True, False, True, True]
    
    df = Cleaning.convert_float_cols_to_int(df, ["aGE"])
    assert df["aGE"].to_list() == [25, 30, 30, 41]
    assert "int" in df["aGE"].dtype.name
    
    df = Cleaning.convert_float_cols_to_int(df, ["aGE"])
    df = Cleaning.convert_to_best_dtypes(df, ["aGE"])
    total_usage_after = Getter.get_total_memory_usage(df, "kb")
    assert total_usage_before > total_usage_after