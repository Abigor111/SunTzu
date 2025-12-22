import pandas as pd 
import numpy as np

from .getter import Getter
from .utils import Utils
from .errors import *

class Statistics(pd.DataFrame):

    
    def show_nulls(self, cols:list[str]=None)-> None:
        """
        Displays the number and percentage of null values for specified DataFrame columns.

        Args:
            cols (list[str], optional): List of columns to analyze. If None, all columns are analyzed.

        Returns:
            None: The function prints a summary table of null counts and percentages and does not return a value.

        Raises:
            ColumnNotExists: If any column in `cols` does not exist in the DataFrame.
        """

        if cols is None:
            cols: list[pd.Series] = self.columns

        
        nulls_percentage: list= [] # will be converted later to a dataframe
  

        for col in cols:
            if col not in list(self.columns):
                raise ColumnNotExists("Column {col} doesnt exists. Please provide columns that are in the dataframe")
            value: int = Getter.get_nulls_count(self, [col])
            # len(self[col]) returns the size of the columns
            percentage: float = round((value/len(self[col])) * 100, 2)
            nulls_percentage.append([col, value, f"{percentage}%"])


        Utils.convert_dataframe(nulls_percentage, ["Nulls Count","Percentage"])

    def show_num_unique_values(self, cols: list[str]=None) -> None:
        """
        Displays the number of unique values for specified DataFrame columns.

        Args:
            cols (list[str], optional): List of columns to analyze. If None, all columns are analyzed.

        Returns:
            None: The function prints a summary table of unique value counts and does not return a value.

        Raises:
            ColumnNotExists: If any column in `cols` does not exist in the DataFrame.
        """

        if cols is None:
            cols = self.columns
        unique_values: list = []  

        for col in cols:
            if col not in list(self.columns):
                raise ColumnNotExists("Column {col} doesnt exists. Please provide columns that are in the dataframe")
            num_unique_values: int = Getter.get_unique_values()
            unique_values.append([col, num_unique_values])
        Utils.convert_dataframe(unique_values, ["Num of Unique Values"])

    def show_max_values(self, cols: list[str] =None) -> None:
        """
        Displays the maximum (or most common) values for specified DataFrame columns, 
        including their count and percentage of occurrences.

        Args:
            cols (list[str], optional): List of columns to analyze. If None, all columns are analyzed.

        Returns:
            None: The function prints a summary table of maximum values and does not return a value.

        Raises:
            ColumnNotExists: If any column in `cols` does not exist in the DataFrame.
        """

        if cols is None:
            cols = self.columns

        max_values_list: list = []

        for col in cols:
            if col not in list(self.columns):
                raise ColumnNotExists("Column {col} doesnt exists. Please provide columns that are in the dataframe")
            
            max_value = Getter.get_max_value(self, col)
            max_value_count = self[col].eq(max_value).sum()  
        
            perc = round((max_value_count / len(self[col])) * 100, 2)
            max_values_list.append([col, max_value, max_value_count, perc])

        Utils.convert_dataframe(max_values_list,  ["Max/Most Common Value", "Occurences", "Percentage"])

    def show_min_values(self, cols: list[str]=None) -> None:
        """
        Displays the minimum (or least common) values for specified DataFrame columns, 
        including their count and percentage of occurrences.

        Args:
            cols (list[str], optional): List of columns to analyze. If None, all columns are analyzed.

        Returns:
            None: The function prints a summary table of minimum values and does not return a value.

        Raises:
            ColumnNotExists: If any column in `cols` does not exist in the DataFrame.
        """

        if cols is None:
            cols = self.columns

        min_values_list: list = []

        for col in cols:
            if col not in list(self.columns):
                raise ColumnNotExists("Column {col} doesnt exists. Please provide columns that are in the dataframe")
            
            min_value = Getter.get_min_value(self, col)
            min_value_count = self[col].eq(min_value).sum()  
        
            perc = round((min_value_count / len(self[col])) * 100, 2)
            min_values_list.append([col, min_value, min_value_count, perc])

        Utils.convert_dataframe(min_values_list,  ["Min/Less Common Value", "Occurences", "Percentage"])

    def show_values_insight(self, cols: list[str]= None, transpose: bool =False) -> None:
        """
        Displays key insights for specified DataFrame columns, including data type, unique values, 
        max/min values with their counts and percentages, and null value statistics.

        Args:
            cols (list[str], optional): List of columns to analyze. If None, all columns are analyzed.
            transpose (bool, optional): If True, the resulting table is transposed for better readability. Defaults to False.

        Returns:
            None: The function prints a summary table of insights and does not return a value.

        Raises:
            ColumnNotExists: If any column in `cols` does not exist in the DataFrame.
        """

        if cols is None:
            cols = self.columns
        dataframe: list = []  
        for col in cols:
            if col not in list(self.columns):
                raise ColumnNotExists("Column {col} doesnt exists. Please provide columns that are in the dataframe") 
            max_value_count: int =self[col].eq(Getter.get_max_value(self, col)).sum()
            min_value_count: int =self[col].eq(Getter.get_min_value(self, col)).sum()
            nulls_count: int = Getter.get_nulls_count(self, [col])
            col_size: int = len(self[col])
            col_info = [  
                col,  
                Getter.get_dtype(self, col),  
                Getter.get_unique_values(self, col),  
                Getter.get_max_value(self, col),  
                max_value_count,  
                f"{round((max_value_count/col_size)*100, 2)}%",  
                Getter.get_min_value(self, col),  
                min_value_count,  
                f"{round((min_value_count/col_size)*100, 2)}%",   
                nulls_count,  
                f"{round((nulls_count/col_size)*100,2)}%"  
            ]
            dataframe.append(col_info)  

        column_names = [    
            'Dtype',  
            'Distinct Values',  
            'Max Value',  
            'Max Value Occurrences',  
            'Max Value Occurences Percentage',  
            'Min Value',  
            'Min Value Occurrences',  
            'Min Value Occurences Percentage',  
            'Null Values',  
            'Null Values Percentage'  
        ] 
    
        Utils.convert_dataframe(dataframe, column_names, transpose)  
