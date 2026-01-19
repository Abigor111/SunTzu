import pandas as pd
import pytest

from suntzu.errors import check_if_columns_exist, ColumnNotExists
def test_check_if_column_exists():
    df = pd.DataFrame({
        "Name":  ["Alan"],
        "Age": 11,
        "Height(cm)": 1.76,
    })
    check_if_columns_exist(df, ["Name", "Age"])
    with pytest.raises(ColumnNotExists):
        check_if_columns_exist(df, ["Age", "Salary"])
    check_if_columns_exist(df, ["Name", "Age", "Height(cm)"])
