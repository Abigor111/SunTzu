from typing import Optional
from .statistics import Statistics
import pandas as pd # type: ignore
class Cleaning(pd.DataFrame):
    def capitalize_cols_name(self: pd.DataFrame, cols: pd.Series = None):
        """
        Capitalizes the column names of the DataFrame.

        Parameters:
            cols (list, optional): List of column names to be capitalized. If None, all columns will be capitalized. Defaults to None.

        Returns:
            pandas.DataFrame: DataFrame with capitalized column names.
        """
        # Check if the 'cols' parameter is None
        if cols is None:
            # If 'cols' is None, set it to the DataFrame's columns
            cols = self.columns
        else:
            # If 'cols' is not None, check if it contains columns that are not in the DataFrame
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                # If there are missing columns, raise a ValueError
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        # Create a copy of the DataFrame
        # Rename the columns of the DataFrame
        self = self.rename(columns=dict(zip(cols, map(str.capitalize, cols))))
        # Return the renamed DataFrame
        return self
    def lower_cols_name(self: pd.DataFrame, cols:pd.Series = None) -> pd.DataFrame:
        """
        Converts the column names of the DataFrame to lowercase.

        Parameters:
            cols (list, optional): List of column names to be converted. If None, all columns will be converted. Defaults to None.

        Returns:
            pandas.DataFrame: DataFrame with lowercase column names.
        """
        # Check if the 'cols' parameter is None
        if cols is None:
            # If 'cols' is None, set it to the DataFrame's columns
            cols = self.columns
        else:
            # If 'cols' is not None, find the columns that are not in the DataFrame
            missing_cols = set(cols) - set(self.columns)
            # If there are missing columns, raise a ValueError
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        # Create a copy of the DataFrame
        # Rename the columns in the DataFrame to lowercase
        self = self.rename(columns=dict(zip(cols, map(str.lower, cols))))
        # Return the DataFrame
        return self
    def upper_cols_name(self: pd.DataFrame, cols: pd.Series=None)  -> pd.DataFrame:
        """
        Convert the column names of a DataFrame to uppercase.

        Args:
            cols (list, optional): A list of column names to be converted to uppercase. If not provided, all column names will be converted.

        Raises:
            ValueError: If any of the specified column names are not present in the DataFrame.

        Returns:
            pandas.DataFrame: The DataFrame with the column names converted to uppercase.
        """
        # Check if the 'cols' parameter is None
        if cols is None:
            # If 'cols' is None, set it to the DataFrame's columns
            cols = self.columns
        else:
            # If 'cols' is not None, find the columns that are not in the DataFrame
            missing_cols = set(cols) - set(self.columns)
            # If there are missing columns, raise a ValueError
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        # Copy the DataFrame
        # Rename the columns to be uppercase
        self = self.rename(columns=dict(zip(cols, map(str.upper, cols))))
        # Return the modified DataFrame
        return self
    def remove_cols_character(self: pd.DataFrame, cols: pd.Series=None, characters: str | list =['_'], add_new_character: bool =False, new_character: str =" ") -> pd.DataFrame:
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
        # If no columns are specified, use all columns
        if cols is None:
            cols = self.columns
        # If columns are specified, check if they exist in the DataFrame
        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        # Create a dictionary to store the new column names
        new_columns = {}
        # Loop through each column
        for col in cols:
            # Create a new column name by replacing the specified characters with the new character
            new_col = col 
            for character in characters:
                for idx, letter in enumerate(col):
                    if letter.lower() == character.lower():  
                        new_col = new_col[:idx] + new_character + new_col[idx+1:] if add_new_character else new_col[:idx] + new_col[idx+1:]
            # Store the new column name in the dictionary
            new_columns[col] = new_col
        # Create a copy of the DataFrame
        # Rename the columns in the DataFrame
        self = self.rename(columns=new_columns)
        # Return the modified DataFrame
        return self
    def round_rows_value(self: pd.DataFrame, cols: pd.Series=None, decimals: int =2) -> pd.DataFrame:
        """
        Round the numerical values in specified columns of a DataFrame to a specified number of decimal places.

        Args:
            cols (list, optional): List of column names to be processed. If None, all columns will be processed. Defaults to None.
            decimals (int, optional): The number of decimal places to round the numerical values to. Defaults to 2.

        Returns:
            pandas.DataFrame: DataFrame with the specified numerical values rounded to the specified number of decimal places.
        """
        # Check if the 'cols' parameter is None, and if so, set it to the DataFrame's columns
        if cols is None:
            cols = self.columns
        # Check if any of the columns in 'cols' is not present in the DataFrame
        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        # Create a list of numerical columns by checking if the data type of each column in 'cols' is not categorical, boolean, or object
        numerical_cols = [col for col in cols if Statistics.get_dtypes(self, [col], False) not in ["categorical", "bool", "object"]]
        # Create a copy of the DataFrame
        # Apply the round function to the numerical columns
        self[numerical_cols] = self[numerical_cols].applymap(lambda x: round(x, decimals) if isinstance(x, (int, float)) else x)
        # Return the modified DataFrame
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
        # Check if the 'cols' parameter is None, if it is, set it to the DataFrame's columns
        if cols is None:
            cols = self.columns
        # Otherwise, check if the columns in 'cols' are present in the DataFrame
        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                # If any columns are missing, raise a ValueError
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        # Create a copy of the DataFrame
        # Iterate through the columns in 'cols'
        for col in cols:
            # If the column is present in the DataFrame
            if col in self.columns:
                # Iterate through the rows in the column
                for idx, value in enumerate(self[col]):
                    # If the value is a string
                    if isinstance(value, str):
                        # Create a new value by replacing the characters in the string with the new character
                        new_value = value
                        for character in characters:
                            for idx_char, letter in enumerate(new_value):
                                # If the letter is lowercase
                                if letter.lower() == character.lower():
                                    # Replace the letter with the new character
                                    new_value = new_value[:idx_char] + new_character + new_value[idx_char+1:] if add_new_character else new_value[:idx_char] + new_value[idx_char+1:]
                        # Set the new value in the DataFrame
                        self.at[idx, col] = new_value    
        # Return the modified DataFrame
        return self
    def capitalize_rows_string(self: pd.DataFrame, cols: Optional[pd.Series] = None)  -> pd.DataFrame:
        """
        Capitalizes the string values in the specified columns.

        Args:
            cols (list): List of column names to capitalize. If None, all columns will be capitalized.

        Returns:
            DataFrame: The DataFrame with capitalized string values in the specified columns.
        """
        # Check if the 'cols' parameter is None, and if not, check if it contains columns that are not present in the DataFrame
        if cols is None:
            # If 'cols' is None, set it to the DataFrame's columns
            cols = self.columns
        else:
            # Create a set of the columns in the 'cols' parameter
            missing_cols = set(cols) - set(self.columns)
            # If there are missing columns, raise a ValueError
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        # Create a copy of the DataFrame
        # Iterate through the columns in the 'cols' parameter
        for col in cols:
            # Check if the column is a string
            if isinstance(col, str):
                # If so, apply the capitalize function to the column
                self[col] = self[col].apply(lambda x: x.capitalize() if isinstance(x, str) else x)
        # Return the modified DataFrame
        return self
    def lower_rows_string(self: pd.DataFrame, cols: pd.Series=None) -> pd.DataFrame:
        """
        Convert the string values in specified columns of a DataFrame to lowercase.

        Args:
            cols (list, optional): List of column names to be processed. If None, all columns will be processed.

        Returns:
            pandas.DataFrame: DataFrame with the specified string values converted to lowercase.
        """
        # Check if the 'cols' parameter is None, and if not, check if it contains columns that are not present in the DataFrame
        if cols is None:
            # If 'cols' is None, set it to the DataFrame's columns
            cols = self.columns
        else:
            # Create a set of the columns in the 'cols' parameter
            missing_cols = set(cols) - set(self.columns)
            # If there are missing columns, raise a ValueError
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        # Create a copy of the DataFrame
        # Iterate through the columns in the 'cols' parameter
        for col in cols:
            # Check if the column is a string
            if isinstance(col, str):
                # If so, apply the lower() method to the column
                self[col] = self[col].applymap(lambda x: x.lower() if isinstance(x, str) else x)
        # Return the modified DataFrame
        return self
    def upper_rows_string(self: pd.DataFrame, cols: pd.Series=None)  -> pd.DataFrame:
        """
        Convert the string values in specified columns of a DataFrame to uppercase.

        Args:
            cols (list, optional): List of column names to be processed. If None, all columns will be processed.

        Returns:
            pandas.DataFrame: DataFrame with the specified string values converted to uppercase.
        """
        # Check if the 'cols' parameter is None, and if not, check if it contains columns that are not present in the DataFrame
        if cols is None:
            # If 'cols' is None, set it to the DataFrame's columns
            cols = self.columns
        else:
            # Create a set of the columns in the 'cols' parameter
            missing_cols = set(cols) - set(self.columns)
            # If there are missing columns, raise a ValueError
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        # Create a copy of the DataFrame
        # Iterate through the columns in the 'cols' parameter
        for col in cols:
            # Check if the column is a string
            if isinstance(col, str):
                # If so, apply the upper() method to the column
                self[col] = self[col].applymap(lambda x: x.upper() if isinstance(x, str) else x)
        # Return the modified DataFrame
        return self
    def remove_rows_with_missing_values(self: pd.DataFrame, cols: pd.Series=None) -> pd.DataFrame:
        """
        Remove rows with missing values from the DataFrame.

        Args:
            cols (list, optional): A list of column names. If provided, only the rows with missing values in the specified columns will be removed. If not provided, all rows with missing values will be removed.

        Returns:
            pandas.DataFrame: The DataFrame with rows containing missing values removed.
        """
        # Create a copy of the original dataframe
        # If no columns are specified, drop rows with NaN values
        if cols is None:
            self = self.dropna(axis=0)
        # Otherwise, drop rows with NaN values in the specified columns
        else:
            self = self.dropna(subset=cols)
        # Return the modified dataframe
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
        # If no columns are specified, use all columns
        if cols is None:
            cols = self.columns
        # If columns are specified, check if they exist in the DataFrame
        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        # Iterate through each column
        for col in cols:
            # Get the data type of the column
            dtype: list = Statistics.get_dtypes(self, [col], False)
            dtype = str(dtype[0])     
            # If the column is categorical, boolean, or object, fill missing values with the mode
            if dtype in ["categorical", "bool", "object"]:
                self[col] = self[col].fillna(self[col].mode()[0])
            # Otherwise, interpolate missing values
            else:
                self[col] = self[col].interpolate()
        # Return the modified DataFrame
        return self
    def foward_fill_rows_with_missing_values(self: pd.DataFrame, cols: pd.Series = None)  -> pd.DataFrame:
        """
        Forward fill missing values in a DataFrame by filling the missing values with the last known non-null value in the column.

        Args:
            cols (list, optional): A list of column names to forward fill missing values. If not provided, all columns will be processed.

        Returns:
            pandas.DataFrame: DataFrame with missing values forward filled.
        """
        # Create a copy of the original dataframe
        # If no columns are specified, fill the entire dataframe using ffill
        if cols is None:
            self = self.ffill()
        # Otherwise, fill only the specified columns using ffill
        else:
            self = self.ffill(subset=cols)
        # Return the modified dataframe
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
        # Create a copy of the original dataframe
        # Split the string column into multiple columns based on the separator
        split_result = self[col].str.split(separator, expand=True)
        # Fill in any NaN values with an empty string
        split_result = split_result.fillna('')
        # Iterate through each new column name and add it to the dataframe
        for i, new_col in enumerate(new_cols):
            if i == 0:
                # If it's the first column, add the split result directly
                self[new_col] = split_result[i]
            else:
                # If it's not the first column, add the remaining columns
                if save_remain:
                    self[new_col] = split_result.loc[:, i:].apply(lambda x: separator.join(x), axis=1)
        # If delete_col is True, delete the original column
        if delete_col:
            self = self.drop([col], axis=1)
        else:
            # Otherwise, add the last column of the split result to the original column
            self[col] = split_result[len(new_cols)]
        # Return the modified dataframe
        return self
    def backward_fill_rows_with_missing_values(self: pd.DataFrame, cols: pd.Series = None) -> pd.DataFrame:
        """
        Fill missing values in a DataFrame by backward filling them with the last valid value in each column.

        Args:
            cols (list, optional): A list of column names. If provided, only the missing values in the specified columns will be filled. If not provided, missing values in all columns will be filled.

        Returns:
            pandas.DataFrame: The DataFrame with missing values filled by backward filling with the last valid value in each column.
        """
        # Create a copy of the original dataframe
        # If no columns are specified, fill the dataframe in backwards
        if cols is None:
            self = self.bfill()
        # Otherwise, fill the specified columns in backwards
        else:
            self = self.bfill(subset=cols)
        # Return the modified dataframe
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
        # If no columns are specified, use all columns
        if cols is None:
            cols = self.columns
        # If columns are specified, check if they exist in the DataFrame
        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        # Iterate through each column
        for col in cols:
            # Get the data type of the column
            dtype = Statistics.get_dtypes(self, [col], False)
            dtype = str(dtype[0])
            # If the column is categorical, boolean, or object, fill missing values with the mode
            if dtype in ["categorical", "bool", "object"]:
                self[col] = self[col].fillna(self[col].mode()[0])
            # Otherwise, fill missing values with the mean
            else:
                self[col] = self[col].fillna(round(self[col].mean(), decimals))
        # Return the modified DataFrame
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
        # Create a copy of the original DataFrame
        # If no columns are specified, use all columns
        if cols is None:
            cols = self.columns
        # If columns are specified, check if they exist in the DataFrame
        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        # Iterate through each column
        for col in cols:
            # Get the data type of the column
            dtype = Statistics.get_dtypes(self, [col], False)
            dtype = str(dtype[0])
            # If the column is categorical, numerical, or object, fill missing values with the mode
            if dtype in ["categorical", "bool", "object"]:
                self[col] = self[col].fillna(self[col].mode()[0])
            # If the column is numerical, fill missing values with the max
            else:
                self[col] = self[col].fillna(self[col].max())
        # Return the filled DataFrame
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
        # Create a copy of the original DataFrame
        # If no columns are specified, use all columns
        if cols is None:
            cols = self.columns
        # If columns are specified, check if they exist in the DataFrame
        else:
            missing_cols = set(cols) - set(self.columns)
            if missing_cols:
                raise ValueError(f"The following columns are not present in the DataFrame: {missing_cols}")
        # Iterate through each column
        for col in cols:
            # Get the data type of the column
            dtype = Statistics.get_dtypes(self, [col], False)
            dtype = str(dtype[0])
            # If the column is categorical, object, or bool, fill missing values with the most frequent value
            if dtype in ["categorical", "bool", "object"]:
                value = self[col].value_counts()
                value = value.index[-1]
                self[col] = self[col].fillna(value)
            # Otherwise, fill missing values with the minimum value
            else:
                self[col] = self[col].fillna(self[col].min())
        # Return the new DataFrame
        return self