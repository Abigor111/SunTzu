import pandas as pd
import numpy as np

from .errors import *

class Getter:
    # function to boost cleaning
    def get_best_int(col_min: int, col_max: int) -> str:
        """
        Determines the smallest integer type capable of representing a range of values.

        Args:
            col_min (int): The minimum value in the range.
            col_max (int): The maximum value in the range.

        Returns:
            str: The name of the smallest integer type that can accommodate all values 
                in the range. Possible returns are "int8", "int16", "int32", or "int64".

        Examples:
            >>> from suntzu import Getter
            >>> Getter.get_best_int(-50, 100)
            'int8'
            >>> Getter.get_best_int(-200, 30000)
            'int16'
            >>> Getter.get_best_int(-50000, 100000)
            'int32'
            >>> Getter.get_best_int(-5000000000, 5000000000)
            'int64'
        """

        if col_min >= -128 and col_max <= 127:
            return "int8"
        elif col_min >= -32768 and col_max <= 32767:
            return "int16"
        elif col_min >= -2147483648 and col_max <= 2147483647:
            return "int32"
        else:
            return "int64"
    
    def get_best_float(col_min: float, col_max: float) -> str:
        """
        Determines the most memory-efficient floating-point type capable of representing 
        a range of values.

        Args:
            col_min (float): The minimum value in the range.
            col_max (float): The maximum value in the range.

        Returns:
            str: The name of the smallest floating-point type that can accommodate all values 
                in the range. Possible returns are "float16", "float32", or "float64".

        Examples:
        >>> from suntzu import Getter
        >>> Getter.get_best_float(0.1, 100.0)
        'float16'
        >>> Getter.get_best_float(-1e5, 1e5)
        'float32'
        >>> Getter.get_best_float(-1e40, 1e40)
        'float64'
        """
        if col_min >= np.finfo(np.float16).min and col_min <= np.finfo(np.float16).max:
            return "float16"
        elif col_max >= np.finfo(np.float32).min and col_max <= np.finfo(np.float32).max:
            return "float32"
        else:
            return "float64"
        
    def get_dtype(self, col: str) -> str:
        return self[col].dtype.name
    
    def get_best_dtype(self: pd.DataFrame, col: pd.Series) -> str:
        dtype = Getter.get_dtype(self, col) # returns int || float || category || bool
        col_min = self[col].min()
        col_max = self[col].max()
        if dtype == "int":
            dtype = Getter.get_best_int(col_min, col_max)
        elif dtype == "float":
            dtype = Getter.get_best_float(col_min, col_max)
        return dtype
    
    # statistics functions
    def get_max_value(self: pd.DataFrame, col: pd.Series) -> int | str:
        """
        Returns the maximum value of a DataFrame column, handling different data types appropriately.

        Args:
            col (pd.Series): The column of the DataFrame to inspect.

        Returns:
            int | str: 
                - For numeric columns, returns the maximum value.
                - For categorical or boolean columns, returns the most frequent value (mode).

        Raises:
            MixedDtypeError: If the column contains mixed types or null values.

        Examples:
            >>> from suntzu import Getter
            >>> import pandas as pd
            >>> df = pd.DataFrame({'a': [1, 3, 2], 'b': [True, False, True], 'c': ['x', 'y', 'x']})
            >>> Getter.get_max_value(df, 'a')
            3
            >>> Getter.get_max_value(df, 'b')
            True
            >>> Getter.get_max_value(df, 'c')
            'x'
        """

        dtype = Getter.get_dtype(self, col)
        try:
            if not dtype in ["categorical", "bool"]:
                value = self[col].max()
            else:
                value = self[col].mode()[0]
        except TypeError:
            raise MixedDtypeError(f"Column '{col}' contains mixed types (e.g., str + float) or null values. Please try cleaning it.")

        return value
    def get_min_value(self: pd.DataFrame, col: pd.Series) -> int | str:
        """
        Returns the minimum value of a DataFrame column, handling different data types appropriately.

        Args:
            col (pd.Series): The column of the DataFrame to inspect.

        Returns:
            int | str: 
                - For numeric columns, returns the minimum value.
                - For categorical or boolean columns, returns the least frequent value.

        Raises:
            MixedDtypeError: If the column contains mixed types or null values.

        Examples:
            >>> from suntzu import Getter
            >>> import pandas as pd
            >>> df = pd.DataFrame({'a': [1, 3, 2], 'b': [True, False, True], 'c': ['x', 'y', 'x']})
            >>> Getter.get_min_value(df, 'a')
            1
            >>> Getter.get_min_value(df, 'b')
            False
            >>> Getter.get_min_value(df, 'c')
            'y'
        """

        dtype = Getter.get_dtype(self, col)
        try:
            if not dtype in ["categorical", "bool"]:
                value = self[col].min()
            else:
                value = self[col].value_counts()[-1]
        except TypeError:
            raise MixedDtypeError(f"Column '{col}' contains mixed types (e.g., str + float) or null values. Please try cleaning it.")

        return value
    def get_nulls_count(self, col: pd.Series) -> int:
        """
        Counts the number of null values in a specific DataFrame column.

        Args:
            col (pd.Series): The column to check for null values.

        Returns:
            int: The number of null values in the column.

        Examples:
            >>> from suntzu import Getter
            >>> import pandas as pd
            >>> df = pd.DataFrame({'a': [1, None, 2], 'b': [None, None, True]})
            >>> Getter.get_nulls_count(df, 'a')
            1
            >>> Getter.get_nulls_count(df, 'b')
            2
        """
        return self[col].isnull().sum()
    def get_unique_values(self, col: str) -> int:
        """
        Returns the number of unique values in a specific DataFrame column.

        Args:
            col (str): The name of the column to inspect.

        Returns:
            int: The count of unique values in the column.

        Examples:
            >>> from suntzu import Getter
            >>> import pandas as pd
            >>> df = pd.DataFrame({'a': [1, 2, 2], 'b': ['x', 'y', 'x', 'z']})
            >>> Getter.get_unique_values(df, 'a')
            2
            >>> Getter.get_unique_values(df, 'b')
            3
        """

        return self[col].nunique()
