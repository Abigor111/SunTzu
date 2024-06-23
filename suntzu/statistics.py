# Import necessary libraries
import pandas as pd # type: ignore
import numpy as np
from IPython.display import display # type: ignore
class Statistics(pd.DataFrame):
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