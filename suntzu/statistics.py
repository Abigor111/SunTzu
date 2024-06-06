# Import necessary libraries
import pandas as pd # type: ignore
import numpy as np
from IPython.display import display # type: ignore
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

    def get_dtypes(self: pd.DataFrame, cols: pd.Series =None, output: bool =True) -> list:
        """
        Get the data types of the specified columns.

        Args:
            cols (list): List of column names. If None, all columns will be used.
            output (bool): If True, print the data types. Default is True.

        Returns:
            list: List of data types.

        """
        # If no columns are specified, use all columns
        if cols is None:
            cols = self.columns
        # If output is True, print the data type of each column
        if output:
            for col in cols:
                print(f"{col} dtype is {self[col].dtype.name}")
        # Return a list of data types for the specified columns
        dtypes = [self[col].dtype.name for col in cols]
        return dtypes
    def get_cols(self: pd.DataFrame) -> list:
        """
        Get the column names of the DataFrame.

        Returns:
            list: A list of column names.
        """
        try:
            # Return a list of column names
            return self.columns.tolist()
        except Exception as e:
            # Print an error message if an exception occurs
            print(f"Error occurred while accessing self.columns: {e}")
            # Return an empty list if an exception occurs
            return []
    def get_cols_dtypes(self: pd.DataFrame, cols: pd.Series =None, get_df: bool =True) -> dict | pd.DataFrame:
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
        # Check if the number of columns and number of data types match
        if cols is None:
            # If no columns are provided, use all columns
            cols = self.columns
        dtypes = []
        # Iterate through each column
        for col in cols:
            # Get the data type of the column
            dtypes.append(Statistics.get_dtypes(self, [col], output=False))
        # Check if the number of columns and number of data types match
        if len(cols) != len(dtypes):
            # If not, raise an error
            raise ValueError("Number of columns and number of data types do not match.")
        # Create a dictionary mapping column names to data types
        cols_dtypes = {col: dtype for col, dtype in zip(cols, dtypes)}
        # If get_df is True, return a DataFrame with column names and data types
        if get_df:
            # Create a list of lists containing column names and data types
            cols_info = [[col, str(dtype).strip("[]'")] for col, dtype in zip(cols, dtypes)]
            # Create a DataFrame with column names and data types
            columns_name = ["Column_Name", "Dtype"]
            dataframe = pd.DataFrame(cols_info, columns=columns_name)
            # Return the DataFrame
            return dataframe
        # If get_df is False, return the dictionary mapping column names to data types
        return cols_dtypes
    def convert_python_type(min_value: int, max_value: int) -> tuple[int, int] | tuple[float, float] | tuple[bool, bool]:
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
        # Check if the type of min_value and max_value are the same
        if type(min_value) != type(max_value):
            # Raise a ValueError if they are not the same
            raise ValueError("min_value and max_value must be of the same type")

        # Check if the type of min_value and max_value are valid
        if not isinstance(min_value, (int, np.integer, float, np.floating, np.bool_, bool)):
            # Raise a ValueError if they are not valid
            raise ValueError("Invalid input: min_value must be numeric or boolean.")
        if not isinstance(max_value, (int, np.integer, float, np.floating, np.bool_, bool)):
            # Raise a ValueError if they are not valid
            raise ValueError("Invalid input: max_value must be numeric or boolean.")

        # Check if the type of min_value and max_value can be converted to int or float
        if isinstance((min_value, max_value), (int, np.integer)):
            # Convert min_value and max_value to int
            return int(min_value), int(max_value)
        elif isinstance((min_value, max_value), (float, np.floating)):
            # Convert min_value and max_value to float
            return float(min_value), float(max_value)
        elif isinstance((min_value, max_value), (np.bool_, bool)):
            # Convert min_value and max_value to bool
            return bool(min_value), bool(max_value)
        else:
            # Return min_value and max_value as they are
            return min_value, max_value
    
    def get_best_dtypes(self: pd.DataFrame, cols: pd.Series =None, convert: bool =False, output: bool =True, show_df: bool =False) -> pd.DataFrame:
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
        # If no columns are specified, use all columns
        if cols is None:
            cols = self.columns
        # If show_df is True, display the dataframe
        if show_df:
            output = False
            dataframe = []
            # Get the dataframe with the columns and their data types
            dataframe1: pd.DataFrame = Statistics.get_cols_dtypes(self, get_df=True)
        # Iterate through each column
        for col in cols:
            try:
                # Check if the column is numeric
                is_numeric = pd.api.types.is_numeric_dtype(self[col])
                # Check if the column is boolean
                is_bool = pd.api.types.is_bool_dtype(self[col])
                # Check if the column is integer
                is_integer = pd.api.types.is_integer_dtype(self[col])
                # Check if the column is float
                is_float = pd.api.types.is_float_dtype(self[col])

                if is_numeric:
                    # Get the minimum and maximum values of the column
                    col_min = self[col].min()
                    col_max = self[col].max()
                    # Convert the minimum and maximum values to the appropriate Python type
                    col_min, col_max = Statistics.convert_python_type(col_min, col_max)

                    if is_bool:
                        col_dtype = "bool"
                    elif is_integer:
                        # Check if the column's values can be represented using a smaller data type
                        if col_min >= -128 and col_max <= 127:
                            col_dtype = "int8"
                        elif col_min >= -32768 and col_max <= 32767:
                            col_dtype = "int16"
                        elif col_min >= -2147483648 and col_max <= 2147483647:
                            col_dtype = "int32"
                        else:
                            col_dtype = "int64"
                    elif is_float:
                        # Check if the column's values can be represented using a smaller data type
                        if col_min >= np.finfo(np.float16).min and col_min <= np.finfo(np.float16).max:
                            col_dtype = "float16"
                        elif col_max >= np.finfo(np.float32).min and col_max <= np.finfo(np.float32).max:
                            col_dtype = "float32"
                        else:
                            col_dtype = "float64"
                    else:
                        col_dtype = "category"
                    # If output is True, print the best dtype for the column
                    if output:
                        print(f"The best dtype for {col} is {col_dtype}")
                        # If the column's dtype is int8, and it has 2 unique values, consider changing it to bool
                        if col_dtype == 'int8':
                            if self[col].nunique(dropna=False) == 2:
                                print("But consider changing it to bool, has you have 2 unique values so you can map the numbers to be True or False")
                            # If convert is True, convert the column to the best dtype
                            if convert:
                                self[col] = self[col].astype(col_dtype)
                    # If show_df is True, append the column's name and dtype to a list
                    elif show_df:
                        col_info = [col, col_dtype]
                        dataframe.append(col_info)
                        # If convert is True, convert the column to the best dtype
                        if convert:
                            self[col] = self[col].astype(col_dtype)
                    # If convert is True, convert the column to the best dtype
                    elif convert:
                        self[col] = self[col].astype(col_dtype)
                    # Otherwise, return the best dtype
                    else:
                        return col_dtype
                else:
                    # If the column is of type object, we check if it contains any categorical data
                    col_dtype = "category"
                    if output:
                        print(f"The best dtype for {col} is {col_dtype}")
                        # If the column contains only 2 unique values, we recommend converting it to bool
                        if self[col].nunique(dropna=False) == 2:
                            print("But consider changing it to bool, has you have 2 unique values so you can map the numbers to be True or False")
                        # If convert is True, we convert the column to the best dtype
                        if convert:
                            self[col] = self[col].astype(col_dtype)
                    elif show_df:
                        # If show_df is True, we append the column information to a list
                        col_info = [col, col_dtype]
                        dataframe.append(col_info)
                        # If convert is True, we convert the column to the best dtype
                        if convert:
                            self[col] = self[col].astype(col_dtype)
                    elif convert:
                        # If convert is True, we convert the column to the best dtype
                        self[col] = self[col].astype(col_dtype)
                    else:
                        # If none of the above conditions are met, we return the best dtype
                        return col_dtype

            except Exception as e:
                print(f"Error on processing columm {col}: {e}")

        if show_df and convert:
            # If show_df is True and convert is True, we display the dataframe
            dataframe = pd.DataFrame(dataframe, columns=["Column_Name", "Best_Dtype"])
            dataframe = dataframe1.merge(dataframe, how="inner", on="Column_Name")
            display(dataframe)
            return self
        elif convert:
            # If convert is True, we return the dataframe
            return self
        elif show_df:
            # If show_df is True, we return the dataframe
            dataframe1 = Statistics.get_cols_dtypes(self, get_df=True)
            dataframe = pd.DataFrame(dataframe, columns=["Column_Name", "Best_Dtype"])
            dataframe = dataframe1.merge(dataframe, how="inner", on="Column_Name")
            return dataframe
    def get_memory_usage(self: pd.DataFrame, cols: pd.Series=None, output: bool =True, get_total: bool =True, show_df: bool =False, unit: str ="kb", use_deep: bool=True, get_dict: bool =False):
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

        # If no columns are specified, use the columns specified in the class
        if cols is None:
            cols = self.columns
        # Supported bytes are kb, mb, and b
        supported_bytes = ["kb", "mb", "b"]
        # Assert that the unit is supported
        assert unit in supported_bytes, f"{unit} not supported. Units supported is bytes(b), kilobytes(kb) and megabytes(mb)."
        # If the total memory usage is required
        if get_total:
            total = 0
        # If the dataframe is required
        if show_df:
            dataframe: pd.DataFrame = []
            output = False
        # If the memory usage for each column is required in a dictionary
        if get_dict:
            get_total = False
            num_of_memory: dict = {}
            num_of_memory.update([("unit", unit)])
        # Set the conversion factors
        conversion_factors = {
            "kb": 1024,
            "mb": 1024**2,
            "b": 1
        }
        conversion_factor = conversion_factors[unit]
        # Loop through each column
        for col in cols:
            # Calculate the memory usage
            memory_usage = self[col].memory_usage(deep=use_deep)
            # Convert the memory usage to the specified unit
            value = round(memory_usage / conversion_factor, 2)
            # If output is required, print the memory usage of each column
            if output:
                print(f"Column: {col} uses {value}{unit}.")
            # If the total memory usage is required, add the memory usage to the total
            if get_total:
                total += value   
            # If the dataframe is required, append the column name and memory usage to the dataframe
            if show_df:
                col_info = [col, value]
                dataframe.append(col_info)
            # If the memory usage for each column is required in a dictionary, append the memory usage to the dictionary
            if get_dict:
                num_of_memory.update([(col, value)])    
        # If the dataframe is required, convert the dataframe to a pandas dataframe
        if show_df:
            collums = ["Col_Name", f"Memory_Usage({unit})"]
            if get_total:
                dataframe.append(["Total", total])
            dataframe = pd.DataFrame(dataframe, columns=collums)
            # If the total memory usage is required, display the dataframe up to the total memory usage
            if get_total:
                n_rows = len(self.columns) + 1
                display(dataframe.head(n_rows))
                total = round(total, 2)
                return total
            # If the total memory usage is not required, return the dataframe
            else:
                return dataframe
        # If output is required, print the total memory usage
        if output:
            total = round(total, 2)   
            print(f"Total: {total} {unit}")
        # If the total memory usage is required, return the total memory usage
        if get_total:
            total = round(total, 2)
            return total
        # If the memory usage for each column is required in a dictionary, return the dictionary
        if get_dict:
            return num_of_memory    
    def get_memory_usage_percentage(self: pd.DataFrame, cols: pd.Series=None, output: bool =True, unit: str="kb", get_total:bool =True, show_df:bool =False, use_deep:bool =True, get_dict: bool=False):
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
        # Check if the number of columns is None
        if cols is None:
            # If it is None, set it to the columns of the DataFrame
            cols = self.columns
        # Create a list of supported bytes
        supported_bytes = ["kb", "mb", "b"]
        # Check if the unit is in the list of supported bytes
        assert unit in supported_bytes, f"{unit} not supported. Units supported is bytes(b), kilobytes(kb) and megabytes(mb)."
        # If get_total is True
        if get_total:
            # Set total to 0
            total = 0
        # If show_df is True
        if show_df:
            # Set dataframe to an empty list
            dataframe: pd.DataFrame = []
            # Set output to False
            output = False
        # If get_dict is True
        if get_dict:
            # Set get_total to False
            get_total = False
            # Create a dictionary to store the percentage of memory usage
            percentage_of_memory: dict = {}
            # Update the dictionary with the unit
            percentage_of_memory.update([("unit", unit)])
        # Loop through each column
        for col in cols:
            # Get the total memory usage
            total_usage = Statistics.get_memory_usage(self, output=False)
            # Get the memory usage of the column
            col_usage = Statistics.get_memory_usage(self, [col], output=False, unit=unit, use_deep=use_deep)
            # Calculate the percentage of memory usage
            value = round((col_usage/total_usage) * 100, 2)
            # If output is True, print the percentage of memory usage
            if output:
                print(f"Column: {col} uses {value}{unit}.")
            # If get_total is True, add the percentage of memory usage to total
            if get_total:
                total += value   
            # If show_df is True, append the column and percentage of memory usage to dataframe
            if show_df:
                col_info = [col, f"{value}%"]
                dataframe.append(col_info)
            # If get_dict is True, append the column and percentage of memory usage to the dictionary
            if get_dict:
                percentage_of_memory.update([(col, f"{value}%")])
        # If show_df is True, create a DataFrame with the columns and percentage of memory usage
        if show_df:
            collums = ["Col_Name", f"Percentage_of_Memory_Usage({unit})"]
            if get_total:
                # Append the total percentage of memory usage to the dataframe
                dataframe.append(["Total", f"{total}%"])
            # Create a DataFrame from the dataframe
            dataframe = pd.DataFrame(dataframe, columns=collums)
            # If get_total is True, display the first n rows of the DataFrame and return the total percentage of memory usage
            if get_total:
                n_rows = len(self.columns) + 1
                display(dataframe.head(n_rows))
                return total
            # Otherwise, return the DataFrame
            else:
                return dataframe
        # If get_total is True, print the total percentage of memory usage and return it
        if get_total:
            if output:   
                print(f"Total: {total} {unit}")
            return total
        # If get_dict is True, print the total percentage of memory usage and return the dictionary
        if get_dict:
            if output:   
                print(f"Total: {total} {unit}")
            return percentage_of_memory
    def get_nulls_count(self: pd.DataFrame, cols: pd.Series=None, output=True, show_df: bool=False, get_total: bool=True, get_dict: bool=False):
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
        # If no columns are specified, use all columns
        if cols is None:
            cols = self.columns
        # Initialize total variable
        if get_total:
            total = 0
        # Initialize dataframe variable
        if show_df:
            dataframe: pd.DataFrame = []
            output = False
        # If dictionary is needed, switch to total and get_total to False
        if get_dict:
            get_total = False
            num_of_nulls: dict = {}
        # Loop through each column
        for col in cols:
            # Calculate the number of null values in the column
            value = self[col].isnull().sum() 
            # If output is True, print the number of null values in the column
            if output:
                print(f"The number of null values in {col} is {value}")
            # If get_total is True, add the number of null values to the total
            if get_total:
                total += value   
            # If show_df is True, append the column name and number of null values to the dataframe
            if show_df:
                col_info = [col, value]
                dataframe.append(col_info)
            # If get_dict is True, append the column name and number of null values to the dictionary
            if get_dict:
                num_of_nulls.update([(col, value)])
        # If show_df is True, convert the dataframe to a pandas DataFrame and display the first n rows
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
        # If get_total is True, print the total number of null values and return it
        if get_total:
            if output:   
                print(f"In this dataframe are missing a total {total} of null values.")
            return total
        # If get_dict is True, return the dictionary of column names and number of null values
        if get_dict:
            return num_of_nulls

    def get_null_percentage(self: pd.DataFrame, cols:pd.Series =None, output: bool =True, show_df: bool =False, get_total: bool =True, get_dict: bool=False):
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
        # If no columns are specified, use all columns
        if cols is None:
            cols = self.columns
        # Initialize total null values count
        if get_total:
            total: int = 0
        # Initialize dataframe
        if show_df:
            dataframe: pd.DataFrame = []
            output = False
        # If percentage of nulls is required, set get_total to False and percentage_of_nulls to an empty dictionary
        if get_dict:
            get_total = False
            percentage_of_nulls: dict = {}
        # Loop through each column
        for col in cols:
            # Calculate the percentage of null values in the column
            value = round((Statistics.get_nulls_count(self, [col], False)/len(self[col])) * 100, 2)
            # If output is True, print the percentage of null values in the column
            if output:
                print(f"The percentage of null values in {col} is {value}%")
            # If get_total is True, add the percentage of null values to the total
            if get_total:
                total += value   
            # If show_df is True, append the column name and percentage of null values to the dataframe
            if show_df:
                col_info = [col, f"{value}%"]
                dataframe.append(col_info)
            # If get_dict is True, append the column name and percentage of null values to the percentage_of_nulls dictionary
            if get_dict:
                percentage_of_nulls.update([(col, f"{value}%")])
        # If show_df is True, display the dataframe with the total percentage of null values at the end
        if show_df:
            collums = ["Col_Name", "Percentage_of_Null_Values"]
            if get_total:
                dataframe.append(["Total", f"{total}%"])
            dataframe = pd.DataFrame(dataframe, columns=collums)
            # If get_total is True, display the dataframe with the total percentage of null values at the end
            if get_total:
                n_rows = len(self.columns) + 1
                display(dataframe.head(n_rows))
                return total
            # Otherwise, return the dataframe
            else:
                return dataframe
        # If get_total is True, print the total percentage of null values and return it
        elif get_total:
            if output:   
                print(f"{total}% of the values in this dataframe are missing.")
            return total
        # If get_dict is True, return the percentage_of_nulls dictionary
        elif get_dict:
            return percentage_of_nulls
    def get_num_of_unique_values(self: pd.DataFrame, cols: pd.Series=None, output: bool =True, show_df: bool =False) -> pd.DataFrame | dict:
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

        # If no column is specified, use all columns
        if cols is None:
            cols = self.columns
        # If show_df is True, create an empty DataFrame to store column information
        if show_df:
            dataframe: pd.DataFrame = []  
            output = False
        # Create a dictionary to store the number of unique values in each column
        num_of_uniques: dict = {}
        # Iterate through each column
        for col in cols:
            # Try to get the number of unique values in the column
            try:
                num_unique_values = self[col].nunique()
                num_of_uniques.update([(col, num_unique_values)])
                # If output is True, print the number of unique values in each column
                if output:
                    print(f"The number of unique values in {col} is {num_unique_values}")
                # If show_df is True, append the column information to the DataFrame
                if show_df:
                    col_info = [col, num_unique_values]
                    dataframe.append(col_info)
            # If the column does not exist in the DataFrame, print an error message
            except KeyError:
                print(f"Column {col} does not exist in the DataFrame.")
        # If show_df is True, return the DataFrame containing column information
        if show_df:
            columns = ["Col_Name", "Unique_Values"]
            dataframe = pd.DataFrame(dataframe, columns=columns)
            return dataframe
        # Otherwise, return the dictionary containing the number of unique values in each column
        else:
            return num_of_uniques
    def get_max_values(self: pd.DataFrame, cols: pd.Series =None, output: bool=True, show_df: bool =False):
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
        # Check if the 'cols' parameter is None, if so set it to the columns of the DataFrame
        if cols is None:
            cols = self.columns
        # Initialize an empty dictionary to store the maximum values for each column
        max_values: dict = {}
        # Iterate through each column in the 'cols' parameter
        for col in cols:
            try:
                # Check if the column is of a type that can have a maximum value
                if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                    # Get the maximum value of the column
                    value = self[col].max()
                    # Update the dictionary with the column and its maximum value
                    max_values.update([(col, value)])
                else:
                    # Get the most common value of the column
                    value = self[col].mode()[0]
                    # Update the dictionary with the column and its most common value
                    max_values.update([(col, value)])
                # Print the maximum value of the column if the 'output' parameter is True
                if output:
                    if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                        print(f"The maximum value in {col} is {value}")
                    else:
                        print(f"The most common value in {col} is {value}")
            # Handle the case where the column does not exist in the DataFrame
            except KeyError:
                print(f"Column {col} does not exist in the DataFrame.")
        # Return the DataFrame containing the column names and their maximum values/most common values
        if show_df:
            dataframe = []
            # Iterate through each column in the 'cols' parameter
            for col in cols:
                # Create a list containing the column name and its maximum value/most common value
                col_info = [col, max_values[col]]
                # Append the list to the dataframe
                dataframe.append(col_info)
            # Set the columns of the DataFrame
            columns = ["Col_Name", "Max_Values/Most_Common"]
            # Create the DataFrame
            dataframe = pd.DataFrame(dataframe, columns=columns)
            # Return the DataFrame
            return dataframe
        else:
            # Return the dictionary containing the column names and their maximum values/most common values
            return max_values
    def get_max_values_count(self: pd.DataFrame, cols: pd.Series =None, output: bool =True, show_df: bool =False) -> pd.DataFrame | dict:
        """
        Returns the number of occurrences of the maximum value or the most common value in each column of a DataFrame.

        Args:
            cols (list, optional): A list of column names. If not provided, all columns in the DataFrame will be considered.
            output (bool, optional): Indicates whether to print the number of occurrences of the maximum value or the most common value in each column. Default is True.
            show_df (bool, optional): Indicates whether to return a DataFrame with the column names and the number of occurrences of the maximum value or the most common value. Default is False.

        Returns:
            DataFrame or dict: If show_df is True, returns a DataFrame with the column names and the number of occurrences of the maximum value or the most common value. Otherwise, returns a dictionary with the column names as keys and the number of occurrences of the maximum value or the most common value as values.
        """
        # Check if the 'cols' parameter is None, if it is, set it to the columns of the DataFrame
        if cols is None:
            cols = self.columns
        # Initialize an empty dictionary to store the count of the maximum values in each column
        max_values_count: dict = {}
        # Iterate through each column in the 'cols' list
        for col in cols:
            # Check if the column is of a type that can have a maximum value (not categorical or boolean)
            try:
                if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                    # Get the maximum value in the column
                    value = self[col].max()
                    # Get the count of the maximum value
                    value = self[col].eq(value).sum()  
                    # Update the dictionary with the column and its count of maximum values
                    max_values_count.update([(col, value)])
                else:
                    # Get the count of the most common value in the column
                    value = self[col].value_counts().iat[0]  
                    # Update the dictionary with the column and its count of maximum values
                    max_values_count.update([(col, value)])
                # Print the count of the maximum values in the column if the 'output' parameter is True
                if output:
                    if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                        print(f"The number of ocurrences of the max value in {col} is {value}")
                    else:
                        print(f"The number of ocurrences of the most common value in {col} is {value}")
            # Handle any KeyErrors that occur
            except KeyError:
                print(f"Column {col} does not exist in the DataFrame.")
        # If the 'show_df' parameter is True, return a DataFrame with the column name and its count of maximum values
        if show_df:
            dataframe = []
            # Iterate through each column in the 'cols' list
            for col in cols:
                # Append a list with the column name and its count of maximum values
                col_info = [col, max_values_count[col]]
                dataframe.append(col_info)
            # Set the columns for the DataFrame
            columns = ["Col_Name", "Max_Values/Most_Common Count"]
            # Return the DataFrame
            dataframe = pd.DataFrame(dataframe, columns=columns)
            return dataframe
        # Otherwise, return the dictionary with the column and its count of maximum values
        else:
            return max_values_count
    def get_max_values_percentage(self: pd.DataFrame, cols:pd.Series=None, output: bool =True, show_df: bool =False) -> pd.DataFrame | dict:
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
        # Check if the column names are provided, if not, use all columns
        if cols is None:
            cols = self.columns
        # Initialize an empty dictionary to store the percentage of max values
        max_values_percentage: dict = {}
        # Iterate through each column in the provided list
        for col in cols:
            # Try to find the max value in the column
            try:
                # Check if the column is of a type that can have max values (not categorical or boolean)
                if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                    # Calculate the percentage of max values
                    value = self[col].max()
                    value = self[col].eq(value).sum()
                    value = (value / self[col].count()) * 100
                    value = round(value, 2)
                    max_values_percentage.update([(col, value)])
                # If the column is categorical or boolean, find the most common value and calculate its percentage
                else:
                    value = self[col].value_counts().iat[0]
                    value = (value / self[col].count()) * 100
                    value = round(value, 2)
                    max_values_percentage.update([(col, value)])
                # Print the percentage of max values if the output flag is set
                if output:
                    if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                        print(f"The percentage of max value in {col} is {value} %")
                        print("Tip: It's possible for the percentage of max values being lower than the percentage of min values. So don't take this function seriously if you are using it for numerical columns.")
                    else:
                        print(f"The percentage of most common value in {col} is {value} %")
            # Handle any KeyErrors that occur if a column does not exist in the DataFrame
            except KeyError:
                print(f"Column {col} does not exist in the DataFrame.")
        # If the show_df flag is set, return a DataFrame with the column names and their corresponding max values/most common values percentages
        if show_df:
            dataframe = []
            for col in cols:
                col_info = [col, f"{max_values_percentage[col]}%"]
                dataframe.append(col_info)
            columns = ["Col_Name", "Max_Values/Most_Common Percentage"]
            dataframe = pd.DataFrame(dataframe, columns=columns)
            return dataframe
        # Otherwise, return the dictionary containing the max values/most common values percentages
        else:
            return max_values_percentage
    def get_min_values(self: pd.DataFrame, cols: pd.Series=None, output: bool=True, show_df: bool =False) -> pd.DataFrame | dict:
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
        # Check if the 'cols' parameter is None, if it is, set it to the columns of the DataFrame
        if cols is None:
            cols = self.columns
        # Initialize an empty dictionary to store the minimum values
        min_values: dict = {}
        # Iterate through the columns
        for col in cols:
            # Try to find the minimum value of the column
            try:
                # Check if the column is of a non-categorical and non-boolean data type
                if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                    # If it is, find the minimum value
                    value = self[col].min()
                    # Store the column and its minimum value in the dictionary
                    min_values.update([(col, value)])
                else:
                    # If it is a categorical or boolean data type, find the least common value
                    value = self[col].value_counts()
                    value = value.index[-1]
                    # Store the column and its least common value in the dictionary
                    min_values.update([(col, value)])
                # If the 'output' parameter is True, print the minimum value or least common value
                if output:
                    if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                        print(f"The minimum value in {col} is {value}")
                    else:
                        print(f"The less common value in {col} is {value}")
            # Handle any KeyErrors that may occur
            except KeyError:
                print(f"Column {col} does not exist in the DataFrame.")
        # If the 'show_df' parameter is True, create a DataFrame with the column names and their minimum values
        if show_df:
            dataframe = []
            for col in cols:
                # Create a list with the column name and its minimum value
                col_info = [col, min_values[col]]
                # Append the list to the dataframe
                dataframe.append(col_info)
            # Create a DataFrame with the column names and minimum values
            columns = ["Col_Name", "Min_Values/Less_Common"]
            dataframe = pd.DataFrame(dataframe, columns=columns)
            # Return the DataFrame
            return dataframe
        # Otherwise, return the dictionary of minimum values
        else:
            return min_values
    def get_min_values_count(self: pd.DataFrame, cols: pd.Series=None, output: bool =True, show_df: bool =False) -> pd.DataFrame | dict:
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
        # If no columns are specified, use all columns
        if cols is None:
            cols = self.columns
        # Initialize a dictionary to store the count of the minimum values in each column
        min_values_count: dict = {}
        # Iterate through each column in the specified columns
        for col in cols:
            # Check if the column is of a type that can have a minimum value
            try:
                if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                    # If the column is not categorical or boolean, get the minimum value and count its occurrences
                    value = self[col].min()
                    value = self[col].eq(value).sum()
                    min_values_count.update([(col, value)])
                else:
                    # If the column is categorical or boolean, get the least common value and count its occurrences
                    value = self[col].value_counts().iat[-1]
                    min_values_count.update([(col, value)])
                # Print the count of the minimum values if the output parameter is set to True
                if output:
                    if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                        print(f"The number of ocurrences of the min value in {col} is {value}")
                    else:
                        print(f"The number of ocurrences of the less common value in {col} is {value}")
            # Handle any KeyErrors that occur
            except KeyError:
                print(f"Column {col} does not exist in the DataFrame.")
        # If the show_df parameter is set to True, return a DataFrame with the column names and counts
        if show_df:
            dataframe = []
            # Iterate through each column in the specified columns
            for col in cols:
                # Append a list containing the column name and its count to the dataframe
                col_info = [col, min_values_count[col]]
                dataframe.append(col_info)
            # Set the column names for the DataFrame
            columns = ["Col_Name", "Min_Values/Less_Common Count"]
            # Return the DataFrame
            dataframe = pd.DataFrame(dataframe, columns=columns)
            return dataframe
        # Otherwise, return the dictionary containing the counts
        else:
            return min_values_count
    def get_min_values_percentage(self: pd.DataFrame, cols: pd.Series=None, output: bool =True, show_df: bool =False) -> pd.DataFrame | dict:
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
        # Check if the 'cols' parameter is None, if it is, set it to the columns of the DataFrame
        if cols is None:
            cols = self.columns
        # Initialize an empty dictionary to store the percentage of min values in each column
        min_values_percentage: dict = {}
        # Iterate through each column in the 'cols' list
        for col in cols:
            try:
                # Check if the column is a categorical or boolean data type, if it is, calculate the percentage of the least common value
                if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                    # Calculate the minimum value in the column
                    value = self[col].min()
                    # Calculate the number of times the minimum value appears in the column
                    value = self[col].eq(value).sum()
                    # Calculate the percentage of the minimum value in the column
                    value = (value / self[col].count()) * 100
                    # Round the percentage to 2 decimal places
                    value = round(value, 2)
                    # Add the column and its percentage of min value to the dictionary
                    min_values_percentage.update([(col, value)])
                # If the column is a categorical or boolean data type, calculate the percentage of the least common value
                else:
                    # Calculate the least common value in the column
                    value = self[col].value_counts().iat[-1]
                    # Calculate the percentage of the least common value in the column
                    value = (value / self[col].count()) * 100
                    # Round the percentage to 2 decimal places
                    value = round(value, 2)
                    # Add the column and its percentage of least common value to the dictionary
                    min_values_percentage.update([(col, value)])
                # If the 'output' parameter is True, print the percentage of min value in each column
                if output:
                    if not pd.api.types.is_categorical_dtype(self[col]) and not pd.api.types.is_bool_dtype(self[col]):
                        print(f"The percentage of min value in {col} is {value} %")
                        print("Tip: It's possible for the percentage of max values being lower than the percentage of min values. So don't take this function seriously if you are using it for numerical columns.")
                    else:
                        print(f"The percentage of less common value in {col} is {value} %")
            # If a KeyError occurs, print a message indicating that the column does not exist in the DataFrame
            except KeyError:
                print(f"Column {col} does not exist in the DataFrame.")
        # If the 'show_df' parameter is True, create a DataFrame containing the column name and its percentage of min value
        if show_df:
            dataframe = []
            for col in cols:
                col_info = [col, f"{min_values_percentage[col]}%"]
                dataframe.append(col_info)
            columns = ["Col_Name", "Min_Values/Less_Common Percentage"]
            dataframe = pd.DataFrame(dataframe, columns=columns)
            # Return the DataFrame
            return dataframe
        # Otherwise, return the dictionary containing the column name and its percentage of min value
        else:
            return min_values_percentage
    def get_dataframe_mem_insight(self: pd.DataFrame, transpose: bool =False) -> pd.DataFrame:
        """
        Generate memory insights for each column in a given dataframe.

        Args:
            self (pandas.DataFrame): The dataframe for which memory insights are to be generated.
            transpose (bool, optional): A flag indicating whether the resulting dataframe should be transposed. Default is False.

        Returns:
            pandas.DataFrame: A dataframe containing information such as column name, data type, recommended data type, memory usage, number of missing values, percentage of missing values, and number of distinct values.
        """
        dataframe: pd.DataFrame = []  # Initialize an empty dataframe
        for col in self.columns:  # Iterate through each column in the DataFrame
            col_info = [  # Create a list of information about the column
                col,  # Column name
                str(Statistics.get_dtypes(self, [col], False)).strip("[]'"),  # Data type of the column
                Statistics.get_best_dtypes(self, [col], False, False),  # Recommendation for data type
                f"{Statistics.get_memory_usage(self, [col], False)} kb",  # Memory usage of the column
                f"{Statistics.get_memory_usage_percentage(self, [col], False)}%",  # Memory usage percentage of the column
                Statistics.get_nulls_count(self, [col], False),  # Number of missing values in the column
                f"{Statistics.get_null_percentage(self, [col], False)}%",  # Percentage of missing values in the column
                list(Statistics.get_num_of_unique_values(self, [col], False).values())[0],  # Number of distinct values in the column
            ]
            dataframe.append(col_info)  # Add the column information to the dataframe
    
        column_names = [  # Create a list of column names
            'Column',  # Column name
            'Dtype',  # Data type of the column
            'Recommend_Dtype',  # Recommendation for data type
            'Memory',  # Memory usage of the column
            'Memory_Percentage',  # Memory usage percentage of the column
            'Missing_Values',  # Number of missing values in the column
            'Percentage_of_Missing_Values',  # Percentage of missing values in the column
            'Distinct_Values'  # Number of distinct values in the column
        ]
        dataframe = pd.DataFrame(dataframe, columns=column_names)  # Create the dataframe
        if transpose:  # If transpose is True
            dataframe = dataframe.transpose()  # Transpose the dataframe
            dataframe.columns = dataframe.iloc[0]  # Set the column names to the first row
            dataframe = dataframe[1:]  # Remove the first row
        return dataframe  # Return the dataframe
    def get_dataframe_values_insight(self: pd.DataFrame, transpose: bool =False) -> pd.DataFrame:
        """
        Generates insights about the values in each column of a given dataframe.

        Args:
            self (pandas.DataFrame): The dataframe for which insights are to be generated.
            transpose (bool, optional): A boolean flag indicating whether to transpose the resulting dataframe. Default is False.

        Returns:
            pandas.DataFrame: A dataframe containing insights about the values in each column of the input dataframe. The number of rows in the resulting dataframe is equal to the number of columns in the input dataframe.
        """
        dataframe: pd.DataFrame = []  # Create an empty list to store the column information
        for col in self.columns:  # Iterate through each column in the DataFrame
            col_info = [  # Create a list to store the column information
                col,  # Column name
                str(Statistics.get_dtypes(self, [col], False)).strip("[]'"),  # Data type of the column
                list(Statistics.get_num_of_unique_values(self, [col], False).values())[0],  # Number of distinct values in the column
                list(Statistics.get_max_values(self, [col], False).values())[0],  # Most common value in the column
                list(Statistics.get_max_values_count(self, [col], False).values())[0],  # Number of occurrences of the most common value
                f"{list(Statistics.get_max_values_percentage(self, [col], False).values())[0]}%",  # Percentage of occurrences of the most common value
                list(Statistics.get_min_values(self, [col], False).values())[0],  # Least common value in the column
                list(Statistics.get_min_values_count(self, [col], False).values())[0],  # Number of occurrences of the least common value
                f"{list(Statistics.get_min_values_percentage(self, [col], False).values())[0]}%",  # Percentage of occurrences of the least common value
                Statistics.get_nulls_count(self, [col], False),  # Number of missing values in the column
                f"{Statistics.get_null_percentage(self, [col], False)}%"  # Percentage of missing values in the column
            ]
            dataframe.append(col_info)  # Add the column information to the list

        column_names = [  # Create a list of column names
            'Column',  # Column name
            'Dtype',  # Data type of the column
            'Distinct_Values',  # Number of distinct values in the column
            'Most_Common/Max_Value',  # Most common value in the column
            'Occurrences_of_Max_Value',  # Number of occurrences of the most common value
            'Percentages_of_Occurrences_of_Max_Value',  # Percentage of occurrences of the most common value
            'Less_Common/Min_Value',  # Least common value in the column
            'Occurrences_of_Min_Value',  # Number of occurrences of the least common value
            'Percentage_of_Occurrences_of_Min_Value',  # Percentage of occurrences of the least common value
            'Missing_Values',  # Number of missing values in the column
            'Percentage_of_Missing_Values'  # Percentage of missing values in the column
        ]
        dataframe = pd.DataFrame(dataframe, columns=column_names)  # Create a DataFrame from the list
        if transpose:  # If the transpose parameter is True
            dataframe = dataframe.transpose()  # Transpose the DataFrame
            dataframe.columns = dataframe.iloc[0]  # Set the column names to the first row of the DataFrame
            dataframe = dataframe[1:]  # Remove the first row of the DataFrame
        return dataframe  # Return the DataFrame
    def find(self: pd.DataFrame, conditions: list, AND: bool=True, OR: bool =False) -> pd.DataFrame:
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
        # Check if conditions is not a list
        if not isinstance(conditions, list):
            # Raise a TypeError if conditions is not a list
            raise TypeError(f"{conditions} has to be a list")
        # Check if both AND and OR are True
        if OR and AND:
            # Raise a ValueError if both AND and OR are True
            raise ValueError("Both AND and OR cannot be True simultaneously.")
        # Create a variable to store the combined condition
        combined_condition = conditions[0]
        # Check if AND is True
        if AND:
            # Loop through the conditions list starting from the second element
            for condition in conditions[1:]:
                # Combine the conditions using the & operator
                combined_condition = combined_condition & condition
        # Check if OR is True
        elif OR:
            # Loop through the conditions list starting from the second element
            for condition in conditions[1:]:
                # Combine the conditions using the | operator
                combined_condition = combined_condition | condition
        # Check if neither AND nor OR is True
        else:
            # Raise a ValueError if neither AND nor OR is True
            raise ValueError("Either AND or OR must be True.")

        # Return the combined condition
        return self[combined_condition]
    def find_replace(self: pd.DataFrame, conditions: list, replace_with: tuple, AND: bool =True, OR: bool =False) -> pd.DataFrame:
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
        # Find the new dataset based on the conditions
        new_dataset = Statistics.find(self, conditions, AND, OR)
        # Replace the values in the original dataset with the values from the new dataset
        self.loc[new_dataset.index, replace_with[0]] = replace_with[1]
        # Return the original dataset
        return self
    def find_delete(self: pd.DataFrame, conditions: list, AND: bool =True, OR: bool =False) -> pd.DataFrame:
        """
        Find rows in the DataFrame that meet certain conditions, delete those rows from the DataFrame, and return the modified DataFrame.

        Args:
            conditions (list): A list of conditions to filter the rows of the DataFrame.
            AND (bool, optional): A boolean flag indicating whether the conditions should be combined using the logical AND operator. Default is True.
            OR (bool, optional): A boolean flag indicating whether the conditions should be combined using the logical OR operator. Default is False.

        Returns:
            pandas.DataFrame: The modified DataFrame after deleting the rows that meet the conditions.
        """
        # Find the new dataset based on the conditions and the AND/OR operator
        new_dataset = Statistics.find(self, conditions, AND, OR)
        # Drop the index of the new dataset from the original dataset
        self = self.drop(new_dataset.index)
        # Return the original dataset
        return self