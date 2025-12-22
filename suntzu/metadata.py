import pyarrow as pa 
import jsonschema 
import pyarrow.parquet as pq 
from jsonschema.exceptions import ValidationError 
import pandas as pd 

import json 
from typing import Optional

class ParquetMetadata:
    def __init__(self, df: pd.DataFrame, metadata: dict, columns: list[str], dtypes: list[str]):
        self.df = df
        self.metadata = metadata
        self.columns = columns
        self.dtypes = dtypes
    def read_parquet_metadata(self, attributes=None, cols=None):
        """
        Reads the metadata of a Parquet file and prints the attributes of each column.

        Args:
            attributes (list, optional): A list of attributes to filter the metadata. If not provided, all attributes will be printed.
            cols (list, optional): A list of column names to filter the columns. If not provided, metadata of all columns will be printed.

        Returns:
            None
        """
        if not self.metadata:
            print("No metadata found.")
            return

        if cols is None:
            cols = self.df.columns

        for col in cols:
            print(f"Column: {col}")
            if col in self.metadata:
                col_metadata = self.metadata[col]
                if attributes:
                    for attr in attributes:
                        if attr in col_metadata:
                            print(f"    {attr}: {col_metadata[attr]}")
                        else:
                            print(f"    The '{attr}' attribute was not found in this column's metadata.")
                else:
                    for key, value in col_metadata.items():
                        print(f"    {key}: {value}")
            else:
                print("    No attributes were found for this column.")
    def insert_parquet_metadata_input(self: pd.DataFrame, attributes: Optional[list[str]]=None, cols: Optional[list[str]]=None, filename: Optional[str]=None) -> pa.Table:
        """
        Inserts metadata into a Parquet file from user input.

        Parameters:
        - self (pd.DataFrame): The DataFrame containing the data.
        - attributes (list, optional): The list of attributes to be included in the metadata. If not provided, a default list is used.
        - cols (list, optional): The list of columns to which the metadata will be applied. If not provided, the metadata will be applied to all columns.
        - filename (str, optional): The path to the Parquet file where the metadata will be inserted. If not provided, the metadata will not be exported to a new file.

        Returns:
        - pa.Table: The Parquet table with the inserted metadata.

        Raises:
        - None

        Note:
        - The function prompts the user to input metadata for each column and attribute.
        - The metadata is stored in a dictionary and added to the schema of the Parquet table.
        - If a filename is provided, the modified table is exported to the specified file.
        """

        default_attributes = ['Description', 'Units', 'Data Source', 'Valid Range or Categories']

        if attributes is None:
            attributes = default_attributes

        if cols is None:
            cols = list(self.columns)
        metadata = []
        columns = self.columns  

        cols_set = set(cols)  

        for col in columns:

            if col in cols_set:
                col_metadata = {}

                for attribute in attributes:

                    data = input(f"{col}: {attribute} - Enter value: ")

                    col_metadata[attribute] = data

                metadata.append(col_metadata)

            else:
                metadata.append(None)

        dtypes = self.dtypes

        dtypes = ["string" if dtype == "category" else str(dtype) for dtype in dtypes]

        cols_dtypes = zip(columns, dtypes, metadata)

        schema = [pa.field(col, pa.type_for_alias(dtype), metadata=meta) for col, dtype, meta in cols_dtypes]

        table_schema = pa.schema(schema)

        table = pa.Table.from_pandas(self.df, schema=table_schema)

        from .library_settings import Settings 

        if filename:
            Settings.export_to_file(table, filename)

    def insert_parquet_metadata_dict(self: pd.DataFrame, dictionary: dict, cols: Optional[list[str]] =None, filename: Optional[str]=None) -> pa.Table:
        """
        Inserts metadata from a dictionary into a Parquet file.

        Parameters:
        - dictionary (dict): The dictionary containing the metadata to be inserted.
        - cols (list, optional): The list of columns to which the metadata will be applied. If not provided, the metadata will be applied to all columns.
        - filename (str, optional): The path to the Parquet file where the metadata will be inserted. If not provided, the metadata will not be exported to a new file.

        Returns:
        - pa.Table: The Parquet table with the inserted metadata.

        Raises:
        - ValueError: If no dictionary is provided.
        - AttributeError: If the provided dictionary is not a dictionary.
        """

        if dictionary is None:

            raise ValueError("Please provide a dictionary.")

        if cols is None:
            cols = list(self.columns)

        columns = self.columns
        dtypes = self.dtypes

        dtypes = ["string" if dtype == "category" else str(dtype) for dtype in dtypes]

        metadata = []

        if isinstance(dictionary, dict):

            cols_set = set(cols)

            for col in columns:

                if col in cols_set:
                    metadata.append(dictionary)

                else:
                    metadata.append(None)

            cols_dtypes = zip(columns, dtypes, metadata)

            schema = [pa.field(col, pa.type_for_alias(dtype), metadata=meta) for col, dtype, meta in cols_dtypes]

            table_schema = pa.schema(schema)
            table = pa.Table.from_pandas(self.df, schema=table_schema)

            from .library_settings import Settings       

            if filename:
                Settings.export_to_file(table, filename)

        else:

            raise AttributeError(f"{dictionary} is not a dictionary.")
    def insert_parquet_metadata_json(self: pd.DataFrame, json_file: str, filename: Optional[str]=None) -> pa.Table:
        """
        Inserts metadata from a JSON file into a Parquet file.

        Parameters:
        - json_file (str): The path to the JSON file containing the metadata.
        - filename (str, optional): The path to the Parquet file where the metadata will be inserted. If not provided, the metadata will not be exported to a new file.

        Returns:
        - pa.Table: The Parquet table with the inserted metadata.

        Raises:
        - IOError: If there is an error opening the JSON file.
        - ValidationError: If the JSON data does not conform to the defined schema.
        """

        schema = {
            "type": "object",
            "patternProperties": {
                ".*": {
                    "type": "object",
                    "patternProperties": {
                        ".*": {
                            "type": "string",
                        }
                    }
                },
                "additionalProperties": False
            }
        }

        try:
            with open(json_file, 'r') as file:
                json_data = json.load(file)
        except IOError:
            raise IOError("Error opening JSON file. Please check if the file exists or if there are any permission issues.")

        try:
            jsonschema.validate(instance=json_data, schema=schema)
        except ValidationError as e:
            raise ValidationError(str(e))

        columns = self.columns
        dtypes = self.dtypes

        cols_dtypes = zip(columns, dtypes)

        cols_dtypes = [[col, "string"] if dtype == "category" or dtype =="object" else [col, str(dtype)] for col, dtype in cols_dtypes]

        metadata = []

        for col in cols_dtypes:

            if col[0] in json_data:
                col_metadata = json_data[col[0]]
                metadata.append(col_metadata)

            else:
                metadata.append(None)

        cols_dtypes = zip(cols_dtypes, metadata)

        schema = []

        for col_dtype, meta in cols_dtypes:

            schema.append(pa.field(col_dtype[0], pa.type_for_alias(col_dtype[1]), metadata=meta))

        table_schema = pa.schema(schema)

        table = pa.Table.from_pandas(self.df, schema=table_schema)

        from .library_settings import Settings

        if filename:
            pq.write_table(table, filename, compression=None)

    def insert_parquet_metadata(self: pd.DataFrame, via: str="input", **kwargs)-> pa.Table:
        """
        Insert metadata into a Parquet file.

        Parameters:
        - via (str): The method of providing metadata. It can be "dict", "json", or "input".
        - kwargs: Additional keyword arguments for the specific method.

        Raises:
        - ValueError: If `via` is not a valid metadata input or if an error occurs during metadata insertion.

        Returns:
        - None: The method modifies the metadata of the Parquet file directly.
        """

        via_lower = via.lower()
        try:

            if via_lower == "dict":
                ParquetMetadata.insert_parquet_metadata_dict(self, **kwargs)

            elif via_lower == "json":
                ParquetMetadata.insert_parquet_metadata_json(self, **kwargs)

            elif via_lower == "input":
                ParquetMetadata.insert_parquet_metadata_input(self, **kwargs)

            else:
                raise ValueError(f"{via} is not a valid metadata input.")

        except Exception as e:
            raise ValueError(f"Error inserting netCDF metadata: {str(e)}")