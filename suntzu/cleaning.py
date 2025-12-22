import pandas as pd

from typing import Optional

from .statistics import Statistics
from .getter import Getter
from .errors import *

class Cleaning(pd.DataFrame):
    def capitalize_cols_name(self, cols: list[str] = None):
        if cols is None:
            cols = self.columns
        else:

            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                raise ColumnNotExists(f"The following columns are not present in the DataFrame: {missing_cols}")

        self = self.rename(columns=dict(zip(cols, map(str.capitalize, cols))))

        return self
    def lower_cols_name(self, cols:list[str] = None):
        if cols is None:

            cols = self.columns
        else:

            missing_cols = set(cols) - set(self.df.columns)

            if missing_cols:
                raise ColumnNotExists(f"The following columns are not present in the DataFrame: {missing_cols}")

        self = self.rename(columns=dict(zip(cols, map(str.lower, cols))))

        return self
    def upper_cols_name(self, cols: list[str]=None):

        if cols is None:

            cols = self.columns
        else:

            missing_cols = set(cols) - set(self.columns)

            if missing_cols:
                raise ColumnNotExists(f"The following columns are not present in the DataFrame: {missing_cols}")

        self = self.rename(columns=dict(zip(cols, map(str.upper, cols))))

        return self

    def round_rows_value(self, cols:list[str], decimals: int =1):

        if cols is None:
            cols = self.columns

        numerical_cols = []
        for col in cols:
            if col not in list(self.columns):
                raise ColumnNotExists("Column {col} doesnt exists. Please provide columns that are in the dataframe")
            dtype = Getter.get_dtype(self, col)
            # only appends if the col is float
            if dtype is "float": 
                numerical_cols.append(col)

        self[numerical_cols] = self[numerical_cols].applymap(lambda x: round(x, decimals))

        return self
    def remove_rows_character(self: pd.DataFrame, cols:pd.Series=None, characters: str | list=[','], add_new_character: bool =False, new_character: str=" ") -> pd.DataFrame:
        """
        Removes specified characters from the values in the specified columns of a DataFrame.

        Args:
            cols (list, optional): List of column names to be processed. If None, all columns will be processed. Defaults to None.
            characters (list, optional): List of characters to be removed from the values in the specified columns. Defaults to [','].
            add_new_character (bool, optional): If True, adds a new character in place of the removed character. Defaults to False.
            new_character (str, optional): The new character to be added if add_new_character is True. Defaults to " ".

        Returns:
            pandas.DataFrame: DataFrame with the specified characters removed from the values in the specified columns.
        """

        if cols is None:
            cols = self.columns

        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:

                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")

        for col in cols:

            if col in self.columns:

                for idx, value in enumerate(self[col]):

                    if isinstance(value, str):

                        new_value = value
                        for character in characters:
                            for idx_char, letter in enumerate(new_value):

                                if letter.lower() == character.lower():

                                    new_value = new_value[:idx_char] + new_character + new_value[idx_char+1:] if add_new_character else new_value[:idx_char] + new_value[idx_char+1:]

                        self.at[idx, col] = new_value    

        return self
    def capitalize_rows_string(self: pd.DataFrame, cols: Optional[pd.Series] = None)  -> pd.DataFrame:
        """
        Capitalizes the string values in the specified columns.

        Args:
            cols (list): List of column names to capitalize. If None, all columns will be capitalized.

        Returns:
            DataFrame: The DataFrame with capitalized string values in the specified columns.
        """

        if cols is None:

            cols = self.columns
        else:

            missing_cols = set(cols) - set(self.columns)

            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")

        for col in cols:

            if isinstance(col, str):

                self[col] = self[col].apply(lambda x: x.capitalize() if isinstance(x, str) else x)

        return self
    def lower_rows_string(self: pd.DataFrame, cols: pd.Series=None) -> pd.DataFrame:
        """
        Convert the string values in specified columns of a DataFrame to lowercase.

        Args:
            cols (list, optional): List of column names to be processed. If None, all columns will be processed.

        Returns:
            pandas.DataFrame: DataFrame with the specified string values converted to lowercase.
        """

        if cols is None:

            cols = self.columns
        else:

            missing_cols = set(cols) - set(self.columns)

            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")

        for col in cols:

            if isinstance(col, str):

                self[col] = self[col].applymap(lambda x: x.lower() if isinstance(x, str) else x)

        return self
    def upper_rows_string(self: pd.DataFrame, cols: pd.Series=None)  -> pd.DataFrame:
        """
        Convert the string values in specified columns of a DataFrame to uppercase.

        Args:
            cols (list, optional): List of column names to be processed. If None, all columns will be processed.

        Returns:
            pandas.DataFrame: DataFrame with the specified string values converted to uppercase.
        """

        if cols is None:

            cols = self.columns
        else:

            missing_cols = set(cols) - set(self.columns)

            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")

        for col in cols:

            if isinstance(col, str):

                self[col] = self[col].applymap(lambda x: x.upper() if isinstance(x, str) else x)

        return self
    def remove_rows_with_missing_values(self: pd.DataFrame, cols: pd.Series=None) -> pd.DataFrame:
        """
        Remove rows with missing values from the DataFrame.

        Args:
            cols (list, optional): A list of column names. If provided, only the rows with missing values in the specified columns will be removed. If not provided, all rows with missing values will be removed.

        Returns:
            pandas.DataFrame: The DataFrame with rows containing missing values removed.
        """

        if cols is None:
            self = self.dropna(axis=0)

        else:
            self = self.dropna(subset=cols)

        return self
    def interpolate_rows_with_missing_values(self: pd.DataFrame, cols: pd.Series=None) -> pd.DataFrame:
        """
        Interpolates missing values in a DataFrame by filling them with interpolated values.

        Args:
            cols (list, optional): A list of column names to interpolate missing values. If not provided, all columns will be processed.

        Returns:
            pandas.DataFrame: DataFrame with missing values interpolated.

        Raises:
            ValueError: If any of the specified columns are not present in the DataFrame.
        """

        if cols is None:
            cols = self.columns

        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")

        for col in cols:

            dtype: list = Statistics.get_dtypes(self, [col], False)
            dtype = str(dtype[0])

            if dtype in ["categorical", "bool", "object"]:
                self[col] = self[col].fillna(self[col].mode()[0])

            else:
                self[col] = self[col].interpolate()

        return self
    def foward_fill_rows_with_missing_values(self: pd.DataFrame, cols: pd.Series = None)  -> pd.DataFrame:
        """
        Forward fill missing values in a DataFrame by filling the missing values with the last known non-null value in the column.

        Args:
            cols (list, optional): A list of column names to forward fill missing values. If not provided, all columns will be processed.

        Returns:
            pandas.DataFrame: DataFrame with missing values forward filled.
        """

        if cols is None:
            self = self.ffill()

        else:
            self = self.ffill(subset=cols)

        return self
    def split_rows_string(self: pd.DataFrame, col: pd.Series, new_cols: str, separator: str =",", delete_col: bool =True, save_remain: bool=True)  -> pd.DataFrame:
        """
        Split the values in a specified column of a DataFrame into multiple columns based on a separator.

        Args:
            col (str): The name of the column to be split.
            new_cols (list): A list of new column names to store the split values.
            separator (str, optional): The separator used to split the values. Defaults to ",".
            delete_col (bool, optional): If True, the original column will be deleted. Defaults to True.
            save_remain (bool, optional): If True, the remaining values after splitting will be saved in a new column. Defaults to True.

        Returns:
            pandas.DataFrame: The DataFrame with the specified column split into multiple columns.
        """

        split_result = self[col].str.split(separator, expand=True)

        split_result = split_result.fillna('')

        for i, new_col in enumerate(new_cols):
            if i == 0:

                self[new_col] = split_result[i]
            else:

                if save_remain:
                    self[new_col] = split_result.loc[:, i:].apply(lambda x: separator.join(x), axis=1)

        if delete_col:
            self = self.drop([col], axis=1)
        else:

            self[col] = split_result[len(new_cols)]

        return self
    def backward_fill_rows_with_missing_values(self: pd.DataFrame, cols: pd.Series = None) -> pd.DataFrame:
        """
        Fill missing values in a DataFrame by backward filling them with the last valid value in each column.

        Args:
            cols (list, optional): A list of column names. If provided, only the missing values in the specified columns will be filled. If not provided, missing values in all columns will be filled.

        Returns:
            pandas.DataFrame: The DataFrame with missing values filled by backward filling with the last valid value in each column.
        """

        if cols is None:
            self = self.bfill()

        else:
            self = self.bfill(subset=cols)

        return self
    def fill_rows_with_missing_values_mean(self: pd.DataFrame, cols: pd.Series=None, decimals: int=2) -> pd.DataFrame:
        """
        Fills missing values in a DataFrame with the mean value of the respective column.

        Args:
            cols (list, optional): List of column names to fill missing values. If None, all columns will be processed. Defaults to None.
            decimals (int, optional): The number of decimal places to round the mean value to. Defaults to 2.

        Returns:
            pandas.DataFrame: DataFrame with missing values filled using the mean value of the respective column.

        Raises:
            ValueError: If any of the specified columns are not present in the DataFrame.
        """

        if cols is None:
            cols = self.columns

        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")

        for col in cols:

            dtype = Statistics.get_dtypes(self, [col], False)
            dtype = str(dtype[0])

            if dtype in ["categorical", "bool", "object"]:
                self[col] = self[col].fillna(self[col].mode()[0])

            else:
                self[col] = self[col].fillna(round(self[col].mean(), decimals))

        return self
    def fill_rows_with_missing_values_max(self: pd.DataFrame, cols: pd.Series = None) -> pd.DataFrame:
        """
        Fills missing values in a DataFrame with the maximum value of each column.

        Args:
            cols (list, optional): List of column names to fill missing values. If None, all columns will be processed.

        Returns:
            pandas.DataFrame: DataFrame with missing values filled using the maximum value of each column.

        Raises:
            ValueError: If any of the specified columns are not present in the DataFrame.
        """

        if cols is None:
            cols = self.columns

        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")

        for col in cols:

            dtype = Statistics.get_dtypes(self, [col], False)
            dtype = str(dtype[0])

            if dtype in ["categorical", "bool", "object"]:
                self[col] = self[col].fillna(self[col].mode()[0])

            else:
                self[col] = self[col].fillna(self[col].max())

        return self
    def fill_rows_with_missing_values_min(self: pd.DataFrame, cols: pd.Series=None)  -> pd.DataFrame:
        """
        Fills missing values in a DataFrame with the minimum value of each column.
        If a column has a categorical, boolean, or object data type, the missing values are filled with the most frequent value in that column.

        Args:
            cols (list, optional): A list of column names to fill missing values. If not provided, all columns will be processed.

        Returns:
            pandas.DataFrame: DataFrame with missing values filled using the minimum value of each column.

        Raises:
            ValueError: If any of the specified columns are not present in the DataFrame.
        """

        if cols is None:
            cols = self.columns

        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")

        for col in cols:

            dtype = Getter.get_dtypes(self, [col], False)
            dtype = str(dtype[0])

            if dtype in ["categorical", "bool", "object"]:
                value = self[col].value_counts()
                value = value.index[-1]
                self[col] = self[col].fillna(value)

            else:
                self[col] = self[col].fillna(self[col].min())

        return self
    def get_memory_insights(self: pd.DataFrame, transpose: bool =False):
        dataframe: pd.DataFrame = []  
        for col in self.columns:  
            col_info: list[str] = [  
                col,  
                Getter.get_dtypes(self, [col]),  
                Getter.get_best_dtype(self, [col]),  
                f"{Getter.get_memory_usage(self, [col], False)} kb",  
                f"{Getter.get_memory_usage_percentage(self, [col], False)}%",  
                Statistics.get_nulls_count(self, [col], False),  
                f"{Statistics.get_null_percentage(self, [col], False)}%",  
                list(Statistics.get_num_of_unique_values(self, [col], False).values())[0],  
            ]
            dataframe.append(col_info)  

        column_names: list[str] = [  
            'Column',  
            'Dtype',  
            'Recommend_Dtype',  
            'Memory',  
            'Memory_Percentage',  
            'Missing_Values',  
            'Percentage_of_Missing_Values',  
            'Distinct_Values'  
        ]
        dataframe = pd.DataFrame(dataframe, columns=column_names)  
        if transpose:  
            Getter.transpose_dataframe(dataframe) 
        display(dataframe)
    def get_best_dtypes(self: pd.DataFrame, cols: list[pd.Series] =None, convert: bool =False, show_df: bool =True) -> pd.DataFrame:

        if cols is None:
            cols = self.columns

        if show_df:
            best_dypes = [] 
            dataframe1: pd.DataFrame = Getter.get_cols_dtypes(self, show_df=True)

        if len(cols) == 1:
            return Getter.get_best_dtype(self, cols)
        for col in cols:
            try:
                dtype = Getter.get_best_dtype(self, col)
                if show_df:
                    col_info = [col, dtype]
                    best_dypes.append(col_info)
                if convert:
                    self[col] = self[col].astype(dtype)

            except Exception as e:
                print(f"Error on processing columm {col}: {e}")

        if convert:
            if show_df:
                dataframe1 = Getter.get_cols_dtypes(self, show_df=True)
                dataframe = pd.DataFrame(best_dypes, columns=["Column_Name", "Best_Dtype"])
                dataframe = dataframe1.merge(dataframe, how="inner", on="Column_Name")
                display(dataframe)
            return self
        elif show_df:
            dataframe1 = Getter.get_cols_dtypes(self, show_df=True)
            dataframe = pd.DataFrame(best_dypes, columns=["Column_Name", "Best_Dtype"])
            dataframe = dataframe1.merge(dataframe, how="inner", on="Column_Name")
            display(dataframe)
    
    def get_memory_usage(self: pd.DataFrame, cols: list[pd.Series]=None, show_df: bool =False, unit: str ="kb", use_deep: bool=True):

        assert unit in self.supported_bytes, f"{unit} not supported. Units supported is bytes(b), kilobytes(kb) and megabytes(mb)."

        if cols is None:
            cols = self.columns
            
        if show_df:
            dataframe: pd.DataFrame = []

        conversion_factors = {
            "kb": 1024,
            "mb": 1024**2,
            "b": 1
        }
        conversion_factor = conversion_factors[unit]
        if len(cols) == 1:
            return self[cols].memory_usage(deep=use_deep)
        for col in cols:

            memory_usage = self[col].memory_usage(deep=use_deep)

            value = round(memory_usage / conversion_factor, 2)

            total += value   

            if show_df:
                col_info = [col, value]
                dataframe.append(col_info)   

        if show_df:
            collums = ["Col_Name", f"Memory_Usage({unit})"]
            dataframe = pd.DataFrame(dataframe, columns=collums)
            display(dataframe)


    def get_memory_usage_percentage(self: pd.DataFrame, cols: list[pd.Series]=None, unit: str="kb", show_df:bool =False, use_deep:bool =True):

        assert unit in self.supported_bytes, f"{unit} not supported. Units supported is bytes(b), kilobytes(kb) and megabytes(mb)."
        
        total_usage = Getter.get_memory_usage(self, unit=unit, use_deep=use_deep)
        if len(cols) == 1:
            return round(self[cols].memory_usage(deep=use_deep)/total_usage, 2)
        if cols is None:

            cols = self.columns

        if show_df:
            dataframe: pd.DataFrame = []
            collumns = ["Col_Name", f"Percentage_of_Memory_Usage({unit})"]




        for col in cols:

            col_usage = Getter.get_memory_usage(self, [col],unit=unit, use_deep=use_deep)

            value = round((col_usage/total_usage) * 100, 2)
            
            if show_df:
                col_info = [col, f"{value}%"]
                dataframe.append(col_info)

        if show_df:
            dataframe.append(["Total", f"{total_usage}%"])
            dataframe = pd.DataFrame(dataframe, columns=collumns)
            display(dataframe)