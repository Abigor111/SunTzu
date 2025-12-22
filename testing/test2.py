# my_flavor.py

import pandas_flavor as pf

@pf.register_dataframe_method
def row_by_value(df, col, value):
    """Slice out row from DataFrame by a value."""
    return df[df[col] == value].squeeze()