import pandas as pd
import numpy as np
from suntzu.statistics import Statistics
from IPython.display import display # type: ignore
class Optimization(pd.DataFrame):
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
                    col_min, col_max = Optimization.convert_python_type(col_min, col_max)

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
            total_usage = Optimization.get_memory_usage(self, output=False)
            # Get the memory usage of the column
            col_usage = Optimization.get_memory_usage(self, [col], output=False, unit=unit, use_deep=use_deep)
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
                Optimization.get_best_dtypes(self, [col], False, False),  # Recommendation for data type
                f"{Optimization.get_memory_usage(self, [col], False)} kb",  # Memory usage of the column
                f"{Optimization.get_memory_usage_percentage(self, [col], False)}%",  # Memory usage percentage of the column
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