import pandas as pd
import numpy as np
from IPython.display import display
import xarray as xr
class Statistics(pd.DataFrame):
    """
    The `Statistics` class is a subclass of the `pd.DataFrame` class in the pandas library. It provides additional methods for performing statistical analysis and data exploration on a DataFrame, such as finding maximum and minimum values, counting occurrences, calculating percentages, and generating insights about the data.

    Main functionalities:
    - Getting the data types of the columns
    - Getting the column names
    - Getting the data types of the columns as a DataFrame
    - Converting the columns to the best data type
    - Calculating the memory usage of each column
    - Calculating the memory usage percentage of each column
    - Calculating the number of null values in each column
    - Calculating the percentage of null values in each column
    - Calculating the number of unique values in each column
    - Finding maximum and minimum values in each column of a DataFrame
    - Counting occurrences of maximum and minimum values
    - Calculating the percentage of maximum and minimum values
    - Generating insights about the data, such as memory usage and number of missing values
    - Filtering the data based on specified conditions

    Methods:
    - get_dtypes(cols=None, output=True): Gets the data types of the specified columns.
    - get_cols(): Gets the column names of the DataFrame.
    - get_cols_dtypes(cols=None, get_df=True): Returns the data types of the specified columns in a DataFrame.
    - convert_cols(): Converts the columns to the best data type.
    - get_memory_usage(cols=None, output=True, get_total=True, show_df=False, unit="kb", use_deep=True, get_dict=False): Calculates the memory usage of each column.
    - get_memory_usage_percentage(cols=None, output=True, unit="kb", get_total=True, show_df=False, use_deep=True, get_dict=False): Calculates the memory usage percentage of each column.
    - get_nulls_count(cols=None, output=True, show_df=False, get_total=True, get_dict=False): Calculates the number of null values in each column.
    - get_null_percentage(cols=None, output=True, show_df=False, get_total=True, get_dict=False): Calculates the percentage of null values in each column.
    - get_num_of_unique_values(cols=None, output=True, show_df=False): Calculates the number of unique values in specified columns.
    - get_max_values(cols=None, output=True, show_df=False): Finds the maximum values or the most common values in each column of a DataFrame.
    - get_max_values_count(cols=None, output=True, show_df=False): Returns the number of occurrences of the maximum value or the most common value in each column of a DataFrame.
    - get_max_values_percentage(cols=None, output=True, show_df=False): Calculates the percentage of the maximum value or the most common value in each column of a DataFrame.
    - get_min_values(cols=None, output=True, show_df=False): Retrieves the minimum values or the less common values in each column of a DataFrame.
    - get_min_values_count(cols=None, output=True, show_df=False): Calculates the count of the minimum values or the count of the less common values in each column of a DataFrame.
    - get_min_values_percentage(cols=None, output=True, show_df=False): Calculates the percentage of the minimum value or the percentage of the less common value in each column of a DataFrame.
    - get_dataframe_mem_insight(transpose=False): Generates memory insights for each column in a given DataFrame.
    - get_dataframe_values_insight(transpose=False): Generates insights about the values in each column of a given DataFrame.
    - find(conditions, AND=True, OR=False): Filters the data in a DataFrame based on specified conditions using logical operators (AND or OR).
    - find_replace(conditions, replace_with, AND=True, OR=False): Finds rows in a DataFrame that meet certain conditions and replaces values in a specified column with a new value.
    - find_delete(conditions, AND=True, OR=False): Finds rows in the DataFrame that meet certain conditions, deletes those rows from the DataFrame, and returns the modified DataFrame.
    
    Fields:
    - The `Statistics` class inherits all the fields from the `pd.DataFrame` class, which include the columns, index, and data of the DataFrame.
    """

    def get_dtypes(self, cols=None, output=True):
        """
        Get the data types of the specified columns.

        Args:
            cols (list): List of column names. If None, all columns will be used.
            output (bool): If True, print the data types. Default is True.

        Returns:
            list: List of data types.

        """
        if cols is None:
            cols = self.columns
        if output:
            for col in cols:
                print(f"{col} dtype is {self[col].dtype.name}")
        dtypes = [self[col].dtype.name for col in cols]
        return dtypes
    def get_cols(self):
        """
        Get the column names of the DataFrame.

        Returns:
            list: A list of column names.
        """
        try:
            return self.columns.tolist()
        except Exception as e:
            print(f"Error occurred while accessing self.columns: {e}")
            return []
    def get_cols_dtypes(self, cols=None, get_df=True):
        """
        Returns the data types of the specified columns in a DataFrame.

        Args:
            cols (list, optional): A list of column names to get the data types for. If not provided, it gets the data types for all columns in the DataFrame.
            get_df (bool, optional): A boolean flag indicating whether to return the data types as a DataFrame. Default is True.

        Returns:
            If get_df is True, returns a DataFrame with the column names and their data types.
            If get_df is False, returns a dictionary with column names as keys and their corresponding data types as values.
        
        Raises:
            ValueError: If the number of columns and the number of data types do not match.
        """
        if cols is None:
            cols = self.columns
        dtypes = []
        for col in cols:
            dtypes.append(Statistics.get_dtypes(self, [col], output=False))
        if len(cols) != len(dtypes):
            raise ValueError("Number of columns and number of data types do not match.")
        cols_dtypes = {col: dtype for col, dtype in zip(cols, dtypes)}
        if get_df:
            cols_info = [[col, str(dtype).strip("[]'")] for col, dtype in zip(cols, dtypes)]
            columns_name = ["Column_Name", "Dtype"]
            dataframe = pd.DataFrame(cols_info, columns=columns_name)
            return dataframe
        return cols_dtypes
    def convert_python_type(min_value, max_value):
        """
        Convert the minimum and maximum values of a given type to the appropriate Python data type.

        Args:
            min_value: The minimum value of a given type.
            max_value: The maximum value of a given type.

        Returns:
            A tuple containing the converted min_value and max_value.

        Raises:
            ValueError: If min_value and max_value are not of the same type or if they are not of a valid numeric or boolean type.
        """
        if type(min_value) != type(max_value):
            raise ValueError("min_value and max_value must be of the same type")

        if not isinstance(min_value, (int, np.integer, float, np.floating, np.bool_, bool)):
            raise ValueError("Invalid input: min_value must be numeric or boolean.")
        if not isinstance(max_value, (int, np.integer, float, np.floating, np.bool_, bool)):
            raise ValueError("Invalid input: max_value must be numeric or boolean.")

        if isinstance((min_value, max_value), (int, np.integer)):
            return int(min_value), int(max_value)
        elif isinstance((min_value, max_value), (float, np.floating)):
            return float(min_value), float(max_value)
        elif isinstance((min_value, max_value), (np.bool_, bool)):
            return bool(min_value), bool(max_value)
        else:
            return min_value, max_value
    
    def get_best_dtypes(self, cols=None, convert=False, output=True, show_df=False):
        """
        Determines the best data type for each column in a DataFrame.

        Args:
            cols (list, optional): A list of column names. If not provided, all columns in the DataFrame will be considered.
            convert (bool, optional): Indicates whether to convert the columns to the best data type. Default is False.
            output (bool, optional): Indicates whether to print the best data type for each column. Default is True.
            show_df (bool, optional): Indicates whether to return a DataFrame with the column names and their best data types. Default is False.

        Returns:
            str or DataFrame or None: 
                - If convert and show_df parameters are False, returns the best data type for each column as a string.
                - If convert parameter is True, returns the modified DataFrame with columns converted to the best data types.
                - If show_df parameter is True, returns a DataFrame with the column names and their best data types.
                - Otherwise, returns None.

        Raises:
            Exception: If an error occurs while processing a column.
        """
        if cols is None:
            cols = self.columns
        if show_df:
            output = False
            dataframe = []
            dataframe1 = Statistics.get_cols_dtypes(self, get_df=True)
        for col in cols:
            try:
                is_numeric = pd.api.types.is_numeric_dtype(self[col])
                is_bool = pd.api.types.is_bool_dtype(self[col])
                is_integer = pd.api.types.is_integer_dtype(self[col])
                is_float = pd.api.types.is_float_dtype(self[col])

                if is_numeric:
                    col_min = self[col].min()
                    col_max = self[col].max()
                    col_min, col_max = Statistics.convert_python_type(col_min, col_max)

                    if is_bool:
                        col_dtype = "bool"
                    elif is_integer:
                        if col_min >= -128 and col_max <= 127:
                            col_dtype = "int8"
                        elif col_min >= -32768 and col_max <= 32767:
                            col_dtype = "int16"
                        elif col_min >= -2147483648 and col_max <= 2147483647:
                            col_dtype = "int32"
                        else:
                            col_dtype = "int64"
                    elif is_float:
                        if col_min >= np.finfo(np.float16).min and col_min <= np.finfo(np.float16).max:
                            col_dtype = "float16"
                        elif col_max >= np.finfo(np.float32).min and col_max <= np.finfo(np.float32).max:
                            col_dtype = "float32"
                        else:
                            col_dtype = "float64"
                    else:
                        col_dtype = "category"

                    if output:
                        print(f"The best dtype for {col} is {col_dtype}")
                        if col_dtype == 'int8':
                            if self[col].nunique(dropna=False) == 2:
                                print("But consider changing it to bool, has you have 2 unique values so you can map the numbers to be True or False")
                            if convert:
                                self[col] = self[col].astype(col_dtype)
                    elif show_df:
                        col_info = [col, col_dtype]
                        dataframe.append(col_info)
                        if convert:
                            self[col] = self[col].astype(col_dtype)
                    elif convert:
                        self[col] = self[col].astype(col_dtype)
                    else:
                        return col_dtype

                else:
                    col_dtype = "category"
                    if output:
                        print(f"The best dtype for {col} is {col_dtype}")
                        if self[col].nunique(dropna=False) == 2:
                            print("But consider changing it to bool, has you have 2 unique values so you can map the numbers to be True or False")
                        if convert:
                            self[col] = self[col].astype(col_dtype)
                    elif show_df:
                        col_info = [col, col_dtype]
                        dataframe.append(col_info)
                        if convert:
                            self[col] = self[col].astype(col_dtype)
                    elif convert:
                        self[col] = self[col].astype(col_dtype)
                    else:
                        return col_dtype

            except Exception as e:
                print(f"Error on processing columm {col}: {e}")

        if show_df and convert:
            dataframe = pd.DataFrame(dataframe, columns=["Column_Name", "Best_Dtype"])
            dataframe = dataframe1.merge(dataframe, how="inner", on="Column_Name")
            display(dataframe)
            return self
        elif convert:
            return self
        elif show_df:
            dataframe1 = Statistics.get_cols_dtypes(self, get_df=True)
            dataframe = pd.DataFrame(dataframe, columns=["Column_Name", "Best_Dtype"])
            dataframe = dataframe1.merge(dataframe, how="inner", on="Column_Name")
            return dataframe
    def get_memory_usage(self, cols=None, output=True, get_total=True, show_df=False, unit="kb", use_deep=True, get_dict=False):
        """
        Calculate the memory usage of each column in a DataFrame and provide options to display the results, calculate the total memory usage, and return the information as a DataFrame or dictionary.

        Parameters:
        - cols (optional): A list of column names to calculate the memory usage for. If not provided, memory usage will be calculated for all columns in the DataFrame.
        - output (optional): A boolean flag indicating whether to print the memory usage for each column. Default is True.
        - get_total (optional): A boolean flag indicating whether to calculate the total memory usage. Default is True.
        - show_df (optional): A boolean flag indicating whether to return the memory usage as a DataFrame. Default is False.
        - unit (optional): The unit of memory usage to be displayed. Supported values are "kb" (kilobytes), "mb" (megabytes), and "b" (bytes). Default is "kb".
        - use_deep (optional): A boolean flag indicating whether to include the memory usage of referenced objects. Default is True.
        - get_dict (optional): A boolean flag indicating whether to return the memory usage as a dictionary. Default is False.

        Returns:
        - If output parameter is True, the memory usage for each column will be printed.
        - If get_total parameter is True, the total memory usage will be returned as a float.
        - If show_df parameter is True, a DataFrame with the column names and memory usage will be returned.
        - If get_dict parameter is True, a dictionary with the column names as keys and memory usage as values will be returned.
        """

        if cols is None:
            cols = self.columns
        supported_bytes = ["kb", "mb", "b"]
        assert unit in supported_bytes, f"{unit} not supported. Units supported is bytes(b), kilobytes(kb) and megabytes(mb)."
        if get_total:
            total = 0
        if show_df:
            dataframe = []
            output = False
        if get_dict:
            get_total = False
            num_of_memory = {}
            num_of_memory.update([("unit", unit)])
        conversion_factors = {
            "kb": 1024,
            "mb": 1024**2,
            "b": 1
        }
        conversion_factor = conversion_factors[unit]
        for col in cols:
            memory_usage = self[col].memory_usage(deep=use_deep)
            value = round(memory_usage / conversion_factor, 2)
            if output:
                print(f"Column: {col} uses {value}{unit}.")
            if get_total:
                total += value   
            if show_df:
                col_info = [col, value]
                dataframe.append(col_info)
            if get_dict:
                num_of_memory.update([(col, value)])    
        if show_df:
            collums = ["Col_Name", f"Memory_Usage({unit})"]
            if get_total:
                dataframe.append(["Total", total])
            dataframe = pd.DataFrame(dataframe, columns=collums)
            if get_total:
                n_rows = len(self.columns) + 1
                display(dataframe.head(n_rows))
                return total
            else:
                return dataframe
        if output:   
                print(f"Total: {total} {unit}")
        if get_total:
            return total
        if get_dict:
            return num_of_memory
    def get_memory_usage_percentage(self, cols=None, output=True, unit="kb", get_total=True, show_df=False, use_deep=True, get_dict=False):
        """
        Calculate the memory usage percentage of each column in a DataFrame.

        Args:
            cols (list, optional): A list of column names. If not provided, all columns in the DataFrame will be considered.
            output (bool, optional): Indicates whether to print the memory usage percentage for each column. Default is True.
            unit (str, optional): The unit of memory usage to be displayed. Supported units are bytes (b), kilobytes (kb), and megabytes (mb). Default is kb.
            get_total (bool, optional): Indicates whether to calculate the total memory usage percentage. Default is True.
            show_df (bool, optional): Indicates whether to return a DataFrame with the column names and their memory usage percentages. Default is False.
            use_deep (bool, optional): Indicates whether to use deep memory usage calculation. Default is True.
            get_dict (bool, optional): Indicates whether to return a dictionary with column names as keys and their memory usage percentages as values. Default is False.

        Returns:
            float or DataFrame or None: Depending on the parameters, the method returns the total memory usage percentage as a float, a DataFrame with the column names and their memory usage percentages, or None.
        """
        if cols is None:
            cols = self.columns
        supported_bytes = ["kb", "mb", "b"]
        assert unit in supported_bytes, f"{unit} not supported. Units supported is bytes(b), kilobytes(kb) and megabytes(mb)."
        if get_total:
            total = 0
        if show_df:
            dataframe = []
            output = False
        if get_dict:
            get_total = False
            percentage_of_memory = {}
            percentage_of_memory.update([("unit", unit)])
        for col in cols:
            total_usage = Statistics.get_memory_usage(self, output=False)
            col_usage = Statistics.get_memory_usage(self, [col], output=False, unit=unit, use_deep=use_deep)
            value = round((col_usage/total_usage) * 100, 2)
            if output:
                print(f"Column: {col} uses {value}{unit}.")
            if get_total:
                total += value   
            if show_df:
                col_info = [col, f"{value}%"]
                dataframe.append(col_info)
            if get_dict:
                percentage_of_memory.update([(col, f"{value}%")])
        if show_df:
            collums = ["Col_Name", f"Percentage_of_Memory_Usage({unit})"]
            if get_total:
                dataframe.append(["Total", f"{total}%"])
            dataframe = pd.DataFrame(dataframe, columns=collums)
            if get_total:
                n_rows = len(self.columns) + 1
                display(dataframe.head(n_rows))
                return total
            else:
                return dataframe
        if get_total:
            if output:   
                print(f"Total: {total} {unit}")
            return total
        if get_dict:
            if output:   
                print(f"Total: {total} {unit}")
            return percentage_of_memory
    def get_nulls_count(self, cols=None, output=True, show_df=False, get_total=True, get_dict=False):
        """
        Calculate the number of null values in each column of a DataFrame.

        Args:
            cols (list, optional): A list of column names to calculate the number of null values for. If not provided, all columns in the DataFrame will be considered.
            output (bool, optional): A boolean flag indicating whether to print the number of null values for each column. Default is True.
            show_df (bool, optional): A boolean flag indicating whether to return a DataFrame with the column names and their corresponding null value counts. Default is False.
            get_total (bool, optional): A boolean flag indicating whether to return the total number of null values in the DataFrame. Default is True.
            get_dict (bool, optional): A boolean flag indicating whether to return a dictionary with column names as keys and their corresponding null value counts as values. Default is False.

        Returns:
            DataFrame or int or dict: Depending on the input parameters, the method returns:
                - If show_df is True, a DataFrame with the column names and their corresponding null value counts.
                - If get_total is True, the total number of null values in the DataFrame.
                - If get_dict is True, a dictionary with column names as keys and their corresponding null value counts as values.
        """
        if cols is None:
            cols = self.columns
        if get_total:
            total = 0
        if show_df:
            dataframe = [] 
            output = False
        if get_dict:
            get_total = False
            num_of_nulls = {}
        for col in cols:
            value = self[col].isnull().sum() 
            if output:
                print(f"The number of null values in {col} is {value}")
            if get_total:
                total += value   
            if show_df:
                col_info = [col, value]
                dataframe.append(col_info)
            if get_dict:
                num_of_nulls.update([(col, value)])
        if show_df:
            collums = ["Col_Name", "Null_Values"]
            if get_total:
                dataframe.append(["Total", total])
            dataframe = pd.DataFrame(dataframe, columns=collums)
            if get_total:
                n_rows = len(dataframe.columns)
                display(dataframe.head(n_rows))
                return total
            else:
                return dataframe
        if get_total:
            if output:   
                print(f"In this dataframe are missing a total {total} of null values.")
            return total
        if get_dict:
            return num_of_nulls

    def get_null_percentage(self, cols=None, output=True, show_df=False, get_total=True, get_dict=False):
        """
        Calculate the percentage of null values in each column of a DataFrame.

        Args:
            cols (list, optional): A list of column names. If not provided, all columns in the DataFrame will be considered.
            output (bool, optional): Indicates whether to print the percentage of null values in each column. Default is True.
            show_df (bool, optional): Indicates whether to return a DataFrame with the column names and their percentage of null values. Default is False.
            get_total (bool, optional): Indicates whether to return the total percentage of null values in the DataFrame. Default is True.
            get_dict (bool, optional): Indicates whether to return a dictionary with column names as keys and their corresponding percentage of null values as values. Default is False.

        Returns:
            If output is True, the percentage of null values in each column is printed.
            If show_df is True, a DataFrame with the column names and their percentage of null values is returned.
            If get_total is True, the total percentage of null values in the DataFrame is returned.
            If get_dict is True, a dictionary with column names as keys and their corresponding percentage of null values as values is returned.
        """
        if cols is None:
            cols = self.columns
        if get_total:
            total = 0
        if show_df:
            dataframe = [] 
            output = False
        if get_dict:
            get_total = False
            percentage_of_nulls = {}
        for col in cols:
            value = round((Statistics.get_nulls_count(self, [col], False)/len(self[col])) * 100, 2)
            if output:
                print(f"The percentage of null values in {col} is {value}%")
            if get_total:
                total += value   
            if show_df:
                col_info = [col, f"{value}%"]
                dataframe.append(col_info)
            if get_dict:
                percentage_of_nulls.update([(col, f"{value}%")])
        if show_df:
            collums = ["Col_Name", "Percentage_of_Null_Values"]
            if get_total:
                dataframe.append(["Total", f"{total}%"])
            dataframe = pd.DataFrame(dataframe, columns=collums)
            if get_total:
                n_rows = len(self.columns) + 1
                display(dataframe.head(n_rows))
                return total
            else:
                return dataframe
        elif get_total:
            if output:   
                print(f"{total}% of the values in this dataframe are missing.")
            return total
        elif get_dict:
            return percentage_of_nulls
    def get_num_of_unique_values(self, cols=None, output=True, show_df=False):
        """
        Calculate the number of unique values in specified columns of a DataFrame.

        Args:
            cols (list, optional): A list of column names. If not provided, all columns in the DataFrame will be considered.
            output (bool, optional): A boolean flag indicating whether to print the number of unique values. Default is True.
            show_df (bool, optional): A boolean flag indicating whether to return a DataFrame with the column names and their corresponding number of unique values. Default is False.

        Returns:
            dict or DataFrame: If `show_df` is True, a DataFrame is returned with the column names and their corresponding number of unique values.
                               Otherwise, a dictionary is returned with the column names as keys and the number of unique values as values.
        """

        if cols is None:
            cols = self.columns
        if show_df:
            dataframe = []  
            output = False
        num_of_uniques = {}
        for col in cols:
            try:
                num_unique_values = self[col].nunique()
                num_of_uniques.update([(col, num_unique_values)])
                if output:
                    print(f"The number of unique values in {col} is {num_unique_values}")
                if show_df:
                    col_info = [col, num_unique_values]
                    dataframe.append(col_info)
            except KeyError:
                print(f"Column {col} does not exist in the DataFrame.")
        if show_df:
            columns = ["Col_Name", "Unique_Values"]
            dataframe = pd.DataFrame(dataframe, columns=columns)
            return dataframe
        else:
            return num_of_uniques
    def get_max_values(self, cols=None, output=True, show_df=False):
        """
        Find the maximum values or the most common values in each column of a DataFrame.

        Args:
            cols (list, optional): A list of column names. If not provided, all columns in the DataFrame will be considered.
            output (bool, optional): Indicates whether to print the maximum values. Default is True.
            show_df (bool, optional): Indicates whether to return a DataFrame with the column names and their maximum values. Default is False.

        Returns:
            dict or DataFrame: If show_df is False, a dictionary is returned with column names as keys and their corresponding maximum values or most common values as values.
                               If show_df is True, a DataFrame is returned with the column names and their maximum values or most common values.
        """
        if cols is None:
            cols = self.columns
        max_values = {}
        for col in cols:
            try:
                if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                    value = self[col].max()
                    max_values.update([(col, value)])
                else:
                    value = self[col].mode()[0]
                    max_values.update([(col, value)])
                if output:
                    if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                        print(f"The maximum value in {col} is {value}")
                    else:
                        print(f"The most common value in {col} is {value}")
            except KeyError:
                print(f"Column {col} does not exist in the DataFrame.")
        if show_df:
            dataframe = []
            for col in cols:
                col_info = [col, max_values[col]]
                dataframe.append(col_info)
            columns = ["Col_Name", "Max_Values/Most_Common"]
            dataframe = pd.DataFrame(dataframe, columns=columns)
            return dataframe
        else:
            return max_values
    def get_max_values_count(self, cols=None, output=True, show_df=False):
        """
        Returns the number of occurrences of the maximum value or the most common value in each column of a DataFrame.

        Args:
            cols (list, optional): A list of column names. If not provided, all columns in the DataFrame will be considered.
            output (bool, optional): Indicates whether to print the number of occurrences of the maximum value or the most common value in each column. Default is True.
            show_df (bool, optional): Indicates whether to return a DataFrame with the column names and the number of occurrences of the maximum value or the most common value. Default is False.

        Returns:
            DataFrame or dict: If show_df is True, returns a DataFrame with the column names and the number of occurrences of the maximum value or the most common value. Otherwise, returns a dictionary with the column names as keys and the number of occurrences of the maximum value or the most common value as values.
        """
        if cols is None:
            cols = self.columns
        max_values_count = {}
        for col in cols:
            try:
                if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                    value = self[col].max()
                    value = self[col].eq(value).sum()  
                    max_values_count.update([(col, value)])
                else:
                    value = self[col].value_counts().iat[0]  
                    max_values_count.update([(col, value)])
                if output:
                    if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                        print(f"The number of ocurrences of the max value in {col} is {value}")
                    else:
                        print(f"The number of ocurrences of the most common value in {col} is {value}")
            except KeyError:
                print(f"Column {col} does not exist in the DataFrame.")
        if show_df:
            dataframe = []
            for col in cols:
                col_info = [col, max_values_count[col]]
                dataframe.append(col_info)
            columns = ["Col_Name", "Max_Values/Most_Common Count"]
            dataframe = pd.DataFrame(dataframe, columns=columns)
            return dataframe
        else:
            return max_values_count
    def get_max_values_percentage(self, cols=None, output=True, show_df=False):
        """
        Calculates the percentage of the maximum value or the most common value in each column of a DataFrame.

        Args:
            cols (list, optional): A list of column names. If not provided, all columns in the DataFrame will be considered.
            output (bool, optional): Indicates whether to print the percentage of the maximum value or the most common value. Default is True.
            show_df (bool, optional): Indicates whether to return a DataFrame with the column names and their corresponding percentages. Default is False.

        Returns:
            dict or DataFrame: If `show_df` is True, it returns a DataFrame with the column names and their corresponding percentages. 
                               Otherwise, it returns a dictionary with column names as keys and their corresponding percentages as values.

        Raises:
            KeyError: If a column specified in `cols` does not exist in the DataFrame.
        """
        if cols is None:
            cols = self.columns
        max_values_percentage = {}
        for col in cols:
            try:
                if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                    value = self[col].max()
                    value = self[col].eq(value).sum()
                    value = (value / self[col].count()) * 100
                    value = round(value, 2)
                    max_values_percentage.update([(col, value)])
                else:
                    value = self[col].value_counts().iat[0]
                    value = (value / self[col].count()) * 100
                    value = round(value, 2)
                    max_values_percentage.update([(col, value)])
                if output:
                    if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                        print(f"The percentage of max value in {col} is {value} %")
                        print("Tip: It's possible for the percentage of max values being lower than the percentage of min values. So don't take this function seriously if you are using it for numerical columns.")
                    else:
                        print(f"The percentage of most common value in {col} is {value} %")
            except KeyError:
                print(f"Column {col} does not exist in the DataFrame.")
        if show_df:
            dataframe = []
            for col in cols:
                col_info = [col, f"{max_values_percentage[col]}%"]
                dataframe.append(col_info)
            columns = ["Col_Name", "Max_Values/Most_Common Percentage"]
            dataframe = pd.DataFrame(dataframe, columns=columns)
            return dataframe
        else:
            return max_values_percentage
    def get_min_values(self, cols=None, output=True, show_df=False):
        """
        Retrieve the minimum values for specified columns in a DataFrame.
    
        Args:
            cols (list, optional): A list of column names for which the minimum values should be retrieved. 
                If not provided, the method will consider all columns in the DataFrame.
            output (bool, optional): A boolean flag indicating whether to print the minimum values for each column. 
                Default is True.
            show_df (bool, optional): A boolean flag indicating whether to return the result as a DataFrame. 
                Default is False.
    
        Returns:
            dict or DataFrame: If show_df is False, the method returns a dictionary with column names as keys 
                and their corresponding minimum values as values. If show_df is True, the method returns a DataFrame 
                with two columns: "Col_Name" and "Min_Values/Less_Common", containing the column names and their 
                minimum values.
    
        Raises:
            KeyError: If a specified column does not exist in the DataFrame.
        """
        if cols is None:
            cols = self.columns
        min_values = {}
        for col in cols:
            try:
                if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                    value = self[col].min()
                    min_values.update([(col, value)])
                else:
                    value = self[col].value_counts()
                    value = value.index[-1]
                    min_values.update([(col, value)])
                if output:
                    if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                        print(f"The minimum value in {col} is {value}")
                    else:
                        print(f"The less common value in {col} is {value}")
            except KeyError:
                print(f"Column {col} does not exist in the DataFrame.")
        if show_df:
            dataframe = []
            for col in cols:
                col_info = [col, min_values[col]]
                dataframe.append(col_info)
            columns = ["Col_Name", "Min_Values/Less_Common"]
            dataframe = pd.DataFrame(dataframe, columns=columns)
            return dataframe
        else:
            return min_values
    def get_min_values_count(self, cols=None, output=True, show_df=False):
        """
        Calculate the count of the minimum values or the count of the less common values in each column of a DataFrame.

        Args:
            cols (list, optional): A list of column names. If not provided, all columns in the DataFrame will be considered.
            output (bool, optional): A boolean flag indicating whether to print the count of the minimum values or less common values. Default is True.
            show_df (bool, optional): A boolean flag indicating whether to return a DataFrame with the column names and their corresponding counts. Default is False.

        Returns:
            dict or DataFrame: If show_df is False, returns a dictionary with column names as keys and their corresponding counts as values.
                               If show_df is True, returns a DataFrame with the column names and their corresponding counts.

        Raises:
            KeyError: If a column specified in cols does not exist in the DataFrame.
        """
        if cols is None:
            cols = self.columns
        min_values_count = {}
        for col in cols:
            try:
                if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                    value = self[col].min()
                    value = self[col].eq(value).sum()
                    min_values_count.update([(col, value)])
                else:
                    value = self[col].value_counts().iat[-1]
                    min_values_count.update([(col, value)])
                if output:
                    if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                        print(f"The number of ocurrences of the min value in {col} is {value}")
                    else:
                        print(f"The number of ocurrences of the less common value in {col} is {value}")
            except KeyError:
                print(f"Column {col} does not exist in the DataFrame.")
        if show_df:
            dataframe = []
            for col in cols:
                col_info = [col, min_values_count[col]]
                dataframe.append(col_info)
            columns = ["Col_Name", "Min_Values/Less_Common Count"]
            dataframe = pd.DataFrame(dataframe, columns=columns)
            return dataframe
        else:
            return min_values_count
    def get_min_values_percentage(self, cols=None, output=True, show_df=False):
        """
        Calculates the percentage of the minimum value or the percentage of the less common value in each column of a DataFrame.

        Args:
            cols (list, optional): A list of column names. If not provided, all columns in the DataFrame will be considered.
            output (bool, optional): Indicates whether to print the percentage of the minimum value or the less common value in each column. Default is True.
            show_df (bool, optional): Indicates whether to return a DataFrame with the column names and their corresponding percentages. Default is False.

        Returns:
            dict or DataFrame: If `show_df` is True, returns a DataFrame with the column names and their corresponding percentages. 
                               If `show_df` is False, returns a dictionary with the column names as keys and their corresponding percentages as values.
                               If `output` is True, prints the percentage of the minimum value or the less common value in each column.
        """
        if cols is None:
            cols = self.columns
        min_values_percentage = {}
        for col in cols:
            try:
                if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                    value = self[col].min()
                    value = self[col].eq(value).sum()
                    value = (value / self[col].count()) * 100
                    value = round(value, 2)
                    min_values_percentage.update([(col, value)])
                else:
                    value = self[col].value_counts().iat[-1]
                    value = (value / self[col].count()) * 100
                    value = round(value, 2)
                    min_values_percentage.update([(col, value)])
                if output:
                    if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                        print(f"The percentage of min value in {col} is {value} %")
                        print("Tip: It's possible for the percentage of max values being lower than the percentage of min values. So don't take this function seriously if you are using it for numerical columns.")
                    else:
                        print(f"The percentage of less common value in {col} is {value} %")
            except KeyError:
                print(f"Column {col} does not exist in the DataFrame.")
        if show_df:
            dataframe = []
            for col in cols:
                col_info = [col, f"{min_values_percentage[col]}%"]
                dataframe.append(col_info)
            columns = ["Col_Name", "Min_Values/Less_Common Percentage"]
            dataframe = pd.DataFrame(dataframe, columns=columns)
            return dataframe
        else:
            return min_values_percentage
    def get_dataframe_mem_insight(self, transpose=False):
        """
        Generate memory insights for each column in a given dataframe.

        Args:
            self (pandas.DataFrame): The dataframe for which memory insights are to be generated.
            transpose (bool, optional): A flag indicating whether the resulting dataframe should be transposed. Default is False.

        Returns:
            pandas.DataFrame: A dataframe containing information such as column name, data type, recommended data type, memory usage, number of missing values, percentage of missing values, and number of distinct values.
        """
        dataframe = []
        for col in self.columns:
            col_info = [
                col,
                str(Statistics.get_dtypes(self, [col], False)).strip("[]'"),
                Statistics.get_best_dtypes(self, [col], False, False),
                Statistics.get_memory_usage(self, [col], False),
                f"{Statistics.get_memory_usage_percentage(self, [col], False)}%",
                Statistics.get_nulls_count(self, [col], False),
                f"{Statistics.get_null_percentage(self, [col], False)}%",
                Statistics.get_num_of_unique_values(self, [col], False)
            ]
            dataframe.append(col_info)
    
        column_names = [
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
            dataframe = dataframe.transpose()
            dataframe.columns = dataframe.iloc[0]
            dataframe = dataframe[1:]
        return dataframe.head(len(self.columns))
    def get_dataframe_values_insight(self, transpose=False):
        """
        Generates insights about the values in each column of a given dataframe.

        Args:
            self (pandas.DataFrame): The dataframe for which insights are to be generated.
            transpose (bool, optional): A boolean flag indicating whether to transpose the resulting dataframe. Default is False.

        Returns:
            pandas.DataFrame: A dataframe containing insights about the values in each column of the input dataframe. The number of rows in the resulting dataframe is equal to the number of columns in the input dataframe.
        """
        dataframe = []
        for col in self.columns:
            col_info = [
                col,
                str(Statistics.get_dtypes(self, [col], False)).strip("[]'"),
                list(Statistics.get_num_of_unique_values(self, [col], False).values())[0],
                list(Statistics.get_max_values(self, [col], False).values())[0],
                list(Statistics.get_max_values_count(self, [col], False).values())[0],
                f"{list(Statistics.get_max_values_percentage(self, [col], False).values())[0]}%",
                list(Statistics.get_min_values(self, [col], False).values())[0],
                list(Statistics.get_min_values_count(self, [col], False).values())[0],
                f"{list(Statistics.get_min_values_percentage(self, [col], False).values())[0]}%",
                Statistics.get_nulls_count(self, [col], False),
                f"{Statistics.get_null_percentage(self, [col], False)}%" 
            ]
            dataframe.append(col_info)

        column_names = [
            'Column',
            'Dtype',
            'Distinct_Values',
            'Most_Common/Max_Value',
            'Occurrences_of_Max_Value',
            'Percentages_of_Occurrences_of_Max_Value',
            'Less_Common/Min_Value',
            'Occurrences_of_Min_Value',
            'Percentage_of_Occurrences_of_Min_Value',
            'Missing_Values',
            'Percentage_of_Missing_Values'
        ]
        dataframe = pd.DataFrame(dataframe, columns=column_names)
        if transpose:
            dataframe = dataframe.transpose()
            dataframe.columns = dataframe.iloc[0]
            dataframe = dataframe[1:]
        return dataframe.head(len(self.columns))
    def find(self, conditions, AND=True, OR=False):
        """
        Filter the data in a DataFrame based on specified conditions using logical operators (AND or OR).

        Args:
            conditions (list): A list of conditions to filter the data. Each condition is a logical expression using comparison operators.
            AND (bool, optional): Indicates whether to use the AND operator for combining the conditions. Default is True.
            OR (bool, optional): Indicates whether to use the OR operator for combining the conditions. Default is False.

        Returns:
            DataFrame: A subset of the original DataFrame that satisfies the specified conditions.

        Raises:
            TypeError: If the conditions input is not a list.
            ValueError: If both AND and OR are True simultaneously.
            ValueError: If neither AND nor OR is True.
        """
        if not isinstance(conditions, list):
            raise TypeError(f"{conditions} has to be a list")
        if OR and AND:
            raise ValueError("Both AND and OR cannot be True simultaneously.")
        combined_condition = conditions[0]
        if AND:
            for condition in conditions[1:]:
                combined_condition = combined_condition & condition
        elif OR:
            for condition in conditions[1:]:
                combined_condition = combined_condition | condition
        else:
            raise ValueError("Either AND or OR must be True.")

        return self[combined_condition]
    def find_replace(self, conditions, replace_with, AND=True, OR=False):
        """
        Find rows in a DataFrame that meet certain conditions and replace values in a specified column with a new value.

        Args:
            conditions (dict): A dictionary specifying the conditions to filter the DataFrame. The keys are column names and the values are either a single value or a lambda function that returns True or False.
            replace_with (tuple): A tuple containing the name of the column to replace values in and the new value to replace with.
            AND (bool, optional): A boolean flag indicating whether to use the AND operator when evaluating multiple conditions. Default is True.
            OR (bool, optional): A boolean flag indicating whether to use the OR operator when evaluating multiple conditions. Default is False.

        Returns:
            None: The method modifies the DataFrame in-place and does not return any value.
        """
        new_dataset = Statistics.find(self, conditions, AND, OR)
        self.loc[new_dataset.index, replace_with[0]] = replace_with[1]
        return self
    def find_delete(self, conditions, AND=True, OR=False):
        """
        Find rows in the DataFrame that meet certain conditions, delete those rows from the DataFrame, and return the modified DataFrame.

        Args:
            conditions (list): A list of conditions to filter the rows of the DataFrame.
            AND (bool, optional): A boolean flag indicating whether the conditions should be combined using the logical AND operator. Default is True.
            OR (bool, optional): A boolean flag indicating whether the conditions should be combined using the logical OR operator. Default is False.

        Returns:
            pandas.DataFrame: The modified DataFrame after deleting the rows that meet the conditions.
        """
        new_dataset = Statistics.find(self, conditions, AND, OR)
        self = self.drop(new_dataset.index)
        return self