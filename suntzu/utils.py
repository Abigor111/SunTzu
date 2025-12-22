import pandas as pd
from IPython.display import display
import numpy as np

class Utils:
    @staticmethod
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
    @staticmethod
    def transpose_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.transpose()  
        dataframe.columns = dataframe.iloc[0]  
        dataframe = dataframe[1:]
        return dataframe
    @staticmethod
    def convert_dataframe(dataframe: list, columns: list[str], transpose: bool = False) -> None:
        columns_names = ["Column"] + columns
        dataframe = pd.DataFrame(dataframe, columns=columns_names)
        if transpose:
            dataframe = Utils.transpose_dataframe(dataframe)
        display(dataframe.head(len(dataframe)))