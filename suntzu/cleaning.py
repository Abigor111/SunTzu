from .statistics import Statistics
import pandas as pd
class Cleaning(pd.DataFrame):
    """
    The `Cleaning` class is a subclass of the `pd.DataFrame` class in the pandas library. It provides various methods for cleaning and transforming data in a DataFrame.


    Main functionalities:
    - Capitalizing, converting to lowercase, and converting to uppercase the column names of a DataFrame.
    - Removing specified characters from the column names of a DataFrame.
    - Rounding the numerical values in specified columns of a DataFrame.
    - Removing specified characters from the values in specified columns of a DataFrame.
    - Capitalizing, converting to lowercase, and converting to uppercase the string values in specified columns of a DataFrame.
    - Removing rows with missing values from a DataFrame.
    - Interpolating missing values in a DataFrame.
    - Forward filling missing values in a DataFrame.
    - Splitting values in a column of a DataFrame into multiple columns.
    - Backward filling missing values in a DataFrame.
    - Filling missing values in a DataFrame with the mean, maximum, or minimum value of each column.

    Methods:
    - capitalize_cols_name(cols=None): Capitalizes the column names of the DataFrame.
    - lower_cols_name(cols=None): Converts the column names of the DataFrame to lowercase.
    - upper_cols_name(cols=None): Converts the column names of the DataFrame to uppercase.
    - remove_cols_character(cols=None, characters=['_'], add_new_character=False, new_character=" "): Removes specified characters from the column names of the DataFrame.
    - round_rows_value(cols=None, decimals=2): Rounds the numerical values in specified columns of the DataFrame to a specified number of decimal places.
    - remove_rows_character(cols=None, characters=[','], add_new_character=False, new_character=" "): Removes specified characters from the values in the specified columns of the DataFrame.
    - capitalize_rows_string(cols=None): Capitalizes the string values in the specified columns of the DataFrame.
    - lower_rows_string(cols=None): Converts the string values in specified columns of the DataFrame to lowercase.
    - upper_rows_string(cols=None): Converts the string values in specified columns of the DataFrame to uppercase.
    - remove_rows_with_missing_values(cols=None): Removes rows with missing values from the DataFrame.
    - interpolate_rows_with_missing_values(cols=None): Interpolates missing values in the DataFrame by filling them with interpolated values.
    - foward_fill_rows_with_missing_values(cols=None): Forward fills missing values in the DataFrame by filling the missing values with the last known non-null value in the column.
    - split_rows_string(col, new_cols, separator=",", delete_col=True, save_remain=True): Splits the values in a specified column of the DataFrame into multiple columns based on a separator.
    - backward_fill_rows_with_missing_values(cols=None): Fills missing values in the DataFrame by backward filling them with the last valid value in each column.
    - fill_rows_with_missing_values_mean(cols=None, decimals=2): Fills missing values in the DataFrame with the mean value of the respective column.
    - fill_rows_with_missing_values_max(cols=None): Fills missing values in the DataFrame with the maximum value of each column.
    - fill_rows_with_missing_values_min(cols=None): Fills missing values in the DataFrame with the minimum value of each column.
    """
    def capitalize_cols_name(self, cols = None):
        """
        Capitalizes the column names of the DataFrame.

        Parameters:
            cols (list, optional): List of column names to be capitalized. If None, all columns will be capitalized. Defaults to None.

        Returns:
            pandas.DataFrame: DataFrame with capitalized column names.
        """
        if cols is None:
            cols = self.columns
        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        dataframe = self.copy()
        dataframe = self.rename(columns=dict(zip(cols, map(str.capitalize, cols))))
        return dataframe
    def lower_cols_name(self, cols = None):
        """
        Converts the column names of the DataFrame to lowercase.

        Parameters:
            cols (list, optional): List of column names to be converted. If None, all columns will be converted. Defaults to None.

        Returns:
            pandas.DataFrame: DataFrame with lowercase column names.
        """
        if cols is None:
            cols = self.columns
        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        dataframe = self.copy()
        dataframe = self.rename(columns=dict(zip(cols, map(str.lower, cols))))
        return dataframe
    def upper_cols_name(self, cols=None):
        """
        Convert the column names of a DataFrame to uppercase.

        Args:
            cols (list, optional): A list of column names to be converted to uppercase. If not provided, all column names will be converted.

        Raises:
            ValueError: If any of the specified column names are not present in the DataFrame.

        Returns:
            pandas.DataFrame: The DataFrame with the column names converted to uppercase.
        """
        if cols is None:
            cols = self.columns
        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        dataframe = self.copy()
        dataframe = self.rename(columns=dict(zip(cols, map(str.upper, cols))))
        return dataframe
    def remove_cols_character(self, cols=None, characters=['_'], add_new_character=False, new_character=" "):
        """
        Remove specified characters from the column names of a DataFrame.

        Args:
            cols (list, optional): List of column names to be processed. If None, all columns will be processed. Defaults to None.
            characters (list, optional): List of characters to be removed from the column names. Defaults to ['_'].
            add_new_character (bool, optional): If True, a new character will be added in place of the removed character. Defaults to False.
            new_character (str, optional): The new character to be added in place of the removed character. Defaults to " " (space).

        Returns:
            pandas.DataFrame: DataFrame with the specified characters removed or replaced from the column names.
        """
        if cols is None:
            cols = self.columns
        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        new_columns = {}
        for col in cols:
            new_col = col 
            for character in characters:
                for idx, letter in enumerate(col):
                    if letter.lower() == character.lower():  
                        new_col = new_col[:idx] + new_character + new_col[idx+1:] if add_new_character else new_col[:idx] + new_col[idx+1:]
            new_columns[col] = new_col
        dataframe = self.copy()
        dataframe = self.rename(columns=new_columns)
        return dataframe
    def round_rows_value(self, cols=None, decimals=2):
        """
        Round the numerical values in specified columns of a DataFrame to a specified number of decimal places.

        Args:
            cols (list, optional): List of column names to be processed. If None, all columns will be processed. Defaults to None.
            decimals (int, optional): The number of decimal places to round the numerical values to. Defaults to 2.

        Returns:
            pandas.DataFrame: DataFrame with the specified numerical values rounded to the specified number of decimal places.
        """
        if cols is None:
            cols = self.columns
        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        numerical_cols = [col for col in cols if Statistics.get_dtypes(self, [col], False) not in ["categorical", "bool", "object"]]
        dataframe = self.copy()
        dataframe[numerical_cols] = self[numerical_cols].applymap(lambda x: round(x, decimals) if isinstance(x, (int, float)) else x)
        return dataframe
    def remove_rows_character(self, cols=None, characters=[','], add_new_character=False, new_character=" "):
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
        dataframe = self.copy()
        for col in cols:
            if col in self.columns:
                for idx, value in enumerate(self[col]):
                    if isinstance(value, str):
                        new_value = value
                        for character in characters:
                            for idx_char, letter in enumerate(new_value):
                                if letter.lower() == character.lower():
                                    new_value = new_value[:idx_char] + new_character + new_value[idx_char+1:] if add_new_character else new_value[:idx_char] + new_value[idx_char+1:]
                        dataframe.at[idx, col] = new_value    
        return dataframe
    def capitalize_rows_string(self, cols = None):
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
        dataframe = self.copy()
        dataframe[cols] = self[cols].applymap(lambda x: x.capitalize() if isinstance(x, str) else x)
        return dataframe
    def lower_rows_string(self, cols=None):
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
        dataframe = self.copy()
        dataframe[cols] = self[cols].applymap(lambda x: x.lower() if isinstance(x, str) else x)
        return dataframe
    def upper_rows_string(self, cols=None):
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
        dataframe = self.copy()
        dataframe[cols] = self[cols].applymap(lambda x: x.upper() if isinstance(x, str) else x)
        return dataframe
    def remove_rows_with_missing_values(self, cols=None):
        """
        Remove rows with missing values from the DataFrame.

        Args:
            cols (list, optional): A list of column names. If provided, only the rows with missing values in the specified columns will be removed. If not provided, all rows with missing values will be removed.

        Returns:
            pandas.DataFrame: The DataFrame with rows containing missing values removed.
        """
        dataframe = self.copy()
        if cols is None:
            dataframe = self.dropna(axis=0)
        else:
            dataframe = self.dropna(subset=cols)
        return dataframe
    def interpolate_rows_with_missing_values(self, cols=None):
        """
        Interpolates missing values in a DataFrame by filling them with interpolated values.

        Args:
            cols (list, optional): A list of column names to interpolate missing values. If not provided, all columns will be processed.

        Returns:
            pandas.DataFrame: DataFrame with missing values interpolated.

        Raises:
            ValueError: If any of the specified columns are not present in the DataFrame.
        """
        dataframe = self.copy()
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
                dataframe[col] = self[col].fillna(self[col].mode()[0])
            else:
                dataframe[col] = self[col].interpolate()
        return dataframe
    def foward_fill_rows_with_missing_values(self, cols = None):
        """
        Forward fill missing values in a DataFrame by filling the missing values with the last known non-null value in the column.

        Args:
            cols (list, optional): A list of column names to forward fill missing values. If not provided, all columns will be processed.

        Returns:
            pandas.DataFrame: DataFrame with missing values forward filled.
        """
        dataframe = self.copy()
        if cols is None:
            dataframe = self.ffill()
        else:
            dataframe = self.ffill(subset=cols)
        return dataframe
    def split_rows_string(self, col, new_cols, separator=",", delete_col=True, save_remain=True):
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
        dataframe = self.copy()
        split_result = dataframe[col].str.split(separator, expand=True)
        split_result = split_result.fillna('')
        for i, new_col in enumerate(new_cols):
            if i == 0:
                dataframe[new_col] = split_result[i]
            else:
                if save_remain:
                    dataframe[new_col] = split_result.loc[:, i:].apply(lambda x: separator.join(x), axis=1)
        if delete_col:
            dataframe = dataframe.drop([col], axis=1)
        else:
            dataframe[col] = split_result[len(new_cols)]
        return dataframe
    def backward_fill_rows_with_missing_values(self, cols = None):
        """
        Fill missing values in a DataFrame by backward filling them with the last valid value in each column.

        Args:
            cols (list, optional): A list of column names. If provided, only the missing values in the specified columns will be filled. If not provided, missing values in all columns will be filled.

        Returns:
            pandas.DataFrame: The DataFrame with missing values filled by backward filling with the last valid value in each column.
        """
        dataframe = self.copy()
        if cols is None:
            dataframe = self.bfill()
        else:
            dataframe = self.bfill(subset=cols)
        return dataframe
    def fill_rows_with_missing_values_mean(self, cols=None, decimals=2):
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
        dataframe = self.copy()
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
                dataframe[col] = self[col].fillna(self[col].mode()[0])
            else:
                dataframe[col] = self[col].fillna(round(self[col].mean(), decimals))
        return dataframe
    def fill_rows_with_missing_values_max(self, cols = None):
        """
        Fills missing values in a DataFrame with the maximum value of each column.

        Args:
            cols (list, optional): List of column names to fill missing values. If None, all columns will be processed.

        Returns:
            pandas.DataFrame: DataFrame with missing values filled using the maximum value of each column.

        Raises:
            ValueError: If any of the specified columns are not present in the DataFrame.
        """
        dataframe = self.copy()
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
                dataframe[col] = self[col].fillna(self[col].mode()[0])
            else:
                dataframe[col] = self[col].fillna(self[col].max())
        return dataframe
    def fill_rows_with_missing_values_min(self, cols=None):
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
        dataframe = self.copy()
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
                value = self[col].value_counts()
                value = value.index[-1]
                dataframe[col] = self[col].fillna(value)
            else:
                dataframe[col] = self[col].fillna(self[col].min())
        return dataframe