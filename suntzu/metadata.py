import pyarrow as pa
import jsonschema
import pyarrow.parquet as pq
import json
from jsonschema.exceptions import ValidationError
import pandas as pd
import xarray as xr
from .statistics import Statistics
class netCDF_Metadata(xr.Dataset):
    """
    A subclass of `xr.Dataset` that provides methods for reading and inserting metadata into a netCDF file. It also includes methods for reading and inserting global metadata attributes.

    Methods:
    - get_file_variables(): Returns a list of variables in the NetCDF file.
    - read_netCDF_metadata(variables=None, attributes=None): Reads and prints metadata information from a NetCDF file.
    - insert_netCDF_metadata_input(variables=None, attributes=None, new_file=False, filename="new_file.nc"): Prompts the user to input metadata for specified variables in a NetCDF file.
    - insert_netCDF_metadata_dict(dictionary, variables=None, new_file=False, filename="new_file.nc"): Inserts metadata into a NetCDF file using a dictionary.
    - insert_netCDF_metadata_json(json_file, new_file=False, filename="new_file.nc"): Inserts metadata from a JSON file into a NetCDF file.
    - insert_netCDF_metadata(via="input", **kwargs): Inserts metadata into the NetCDF file using the specified method.
    - get_attrs(): Returns the global metadata attributes of the dataset.
    - read_global_metadata(attributes=None): Prints the global metadata attributes of the dataset.
    - insert_netCDF_global_metadata_input(attributes=None, new_file=False, filename="new_file.nc"): Inserts global metadata into a NetCDF file using user input.
    - insert_netCDF_global_metadata_dict(dictionary, new_file=False, filename="new_file.nc"): Inserts global metadata into a NetCDF file using a dictionary.
    - insert_netCDF_global_metadata_json(json_file, new_file=False, filename="new_file.nc"): Inserts global metadata from a JSON file into a NetCDF file.
    - insert_netCDF_global_metadata(via="input", **kwargs): Inserts global metadata into a NetCDF file using the specified method.
    """
    def get_file_variables(self):
        """
        Get the variables of the file.

        Returns:
            list: A list of variables in the file.
        """
        variables = list(self.variables.keys())
        return variables
    def read_netCDF_metadata(self, variables=None, attributes=None):
        """
        Read and print metadata information from a NetCDF file.

        Args:
            variables (list, optional): A list of variable names to retrieve metadata for. If not specified, all variables in the NetCDF file will be retrieved.
            attributes (list, optional): A list of attribute names to retrieve for each variable. If not specified, all attributes for each variable will be retrieved.

        Returns:
            None

        Example Usage:
            # Read metadata for all variables in the NetCDF file
            read_netCDF_metadata()

            # Read metadata for specific variables in the NetCDF file
            read_netCDF_metadata(variables=['temperature', 'humidity'])

            # Read metadata for specific attributes of all variables in the NetCDF file
            read_netCDF_metadata(attributes=['units', 'long_name'])
        """

        def read_variable_metadata(var_name, var):
            print(f"Variable: {var_name}")
            if not var.attrs:
                if var.values is not None:
                    print(f"    Values: {var.values}")
                else:
                    print("No values were found")
                print("    No attributes were found for this variable.")
            else:
                print(f"    Values: {var.values}")
                print("    Attributes:")
                for key, value in var.attrs.items():
                    if attributes is None or key in attributes:
                        print(f"     {key}: {value}")

        if variables is None:
            variables = list(self.variables.keys())
        for var_name in variables:
            try:
                coord_var = self.coords[var_name]
                read_variable_metadata(var_name, coord_var)
            except (KeyError, AttributeError) as e:
                print(f"Error occurred while retrieving metadata for variable {var_name}: {str(e)}")
    def insert_netCDF_metadata_input(self, variables=None, attributes=None, new_file=False, filename="new_file.nc",):
        """
        This function prompts the user to input metadata for the specified variables in a netCDF file.
        
        Parameters:
        - filename (str): Name of the netCDF file.
        - variables (list): List of variable names. If None, all coordinate variables are used.
        - attributes (list): List of attribute names. If None, default attributes are used.
        - new_file (bool): If True, a new netCDF file is created. If False, the existing file is used.
        
        Raises:
        - KeyError: If a variable was not found.
        - FileExistsError: If the specified file already exists.
        - ValueError: If the filename is invalid.
        """
        
        # Define default attributes if not provided
        default_attributes = [
            "Units", "Long_Name", "Standard_Name/Short_Name", 
            "Valid_Min", "Valid_Max", "Missing_Value", 
            "Fill_Value", "Scale_Factor", "Add_Offset", 
            "Coordinates", "Axis", "Description"
        ]
        if attributes is None:
            attributes = default_attributes

        if variables is None:
            variables = Statistics.get_file_variables(self)

        for coord_name in variables:
            try:
                for attribute in attributes:
                    self[coord_name].attrs[attribute] = input(f"{coord_name}: {attribute} - Enter value: ")
            except KeyError as e:
                raise KeyError(f"Variable {coord_name} not found.") from e
        from .file import File
        if new_file:
            File.export_to_file(self,filename)
        netCDF_Metadata.read_netCDF_metadata(self)
    def insert_netCDF_metadata_dict(self, dictionary, variables=None, new_file=False, filename="new_file.nc"):
        """
        Insert metadata into a netCDF file using a dictionary.

        Parameters:
        - self: The netCDF object.
        - dictionary: A dictionary containing the metadata to be inserted.
        - filename: The name of the netCDF file to be created or modified.
        - variables: A list of variables to insert the metadata into. If None, all variables will be used.
        - new_file: If True, a new file will be created. If False, the metadata will be inserted into an existing file.

        Raises:
        - ValueError: If dictionary is None.
        - AttributeError: If dictionary is not a dictionary.
        - FileExistsError: If the specified file already exists.
        - ValueError: If the filename is invalid.

        Returns:
        - None
        """
        if dictionary is None:
            raise ValueError("Please provide a dictionary.")
        if variables is None:
            variables = Statistics.get_file_variables(self)
        if isinstance(dictionary, dict):
            for var in variables:
                for key, value in dictionary.items():
                    self[var].attrs[key] = value
        else:
            raise AttributeError(f"{dictionary} is not a dictionary.")
        from .file import File
        if new_file:
            File.export_to_file(self,filename)
        netCDF_Metadata.read_netCDF_metadata(self)
    def insert_netCDF_metadata_json(self, json_file, new_file=False, filename="new_file.nc"):
        """
        Inserts metadata from a JSON file into a netCDF file.

        Args:
            self: The instance of the class that the function belongs to.
            json_file (str): The path to the JSON file containing the metadata.
            new_file (bool, optional): A boolean flag indicating whether a new netCDF file should be created. Defaults to False.
            filename (str, optional): The name of the new netCDF file. Defaults to "new_file.nc".

        Raises:
            FileNotFoundError: If the specified filename already exists.

        Returns:
            None: The function modifies the attributes of the netCDF file directly.
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
                metadata = json.load(file)
        except IOError:
            raise IOError("Error opening JSON file. Please check if the file exists or if there are any permission issues.")
        try:
            # Validate JSON against schema
            jsonschema.validate(instance=metadata, schema=schema)
        except ValidationError as e:
            raise ValidationError(str(e))
        for var, attributes in metadata.items():
            for attr, value in attributes.items():
                self[var].attrs[attr] = value
        from .file import File   
        if new_file:
            File.export_to_file(self,filename)
        netCDF_Metadata.read_netCDF_metadata(self)
    def insert_netCDF_metadata(self, via="input", **kwargs):
        """
        Insert metadata into the netCDF file.

        Parameters:
            via (str, optional): The method of providing metadata. Can be "dict", "json", or "input". Defaults to "input".
            **kwargs: Additional keyword arguments for the specific method.

        Raises:
            ValueError: If `via` is not a valid metadata input.
        """
        via_lower = via.lower()
        try:
            if via_lower == "dict":
                netCDF_Metadata.insert_netCDF_metadata_dict(self, **kwargs)
            elif via_lower == "json":
                netCDF_Metadata.insert_netCDF_metadata_json(self, **kwargs)
            elif via_lower == "input":
                netCDF_Metadata.insert_netCDF_metadata_input(self, **kwargs)
            else:
                raise ValueError(f"{via} is not a valid metadata input.")
        except Exception as e:
            raise ValueError(f"Error inserting netCDF metadata: {str(e)}")
    def get_attrs(self):
        return self.attrs
    def read_global_metadata(self, attributes=None):
        """
        Print the global metadata attributes of the dataset.

        Args:
            attributes (list): List of attribute names to print. If None, all attributes will be printed.
        """
        attrs = netCDF_Metadata.get_attrs(self)
        if not attrs:
            print("No Global Attributes were found.")
        else:
            if attributes is None:
                for attr_name, attr_value in attrs.items():
                    print(attr_name, ":", attr_value)
            else:
                for attr_name, attr_value in attrs.items():
                    if attr_name in attributes:
                        print(attr_name, ":", attr_value)
    def insert_netCDF_global_metadata_input(self, attributes=None, new_file=False, filename="new_file.nc"):
        """
        Insert global metadata into a netCDF file.

        Args:
            attributes (list, optional): A list of attribute names for which the user will be prompted to enter values. 
                If not provided, a default list of attributes will be used.
            new_file (bool, optional): A boolean indicating whether a new file should be created. 
                If True, the metadata will be exported to a file specified by the filename parameter. 
                Default is False.
            filename (str, optional): The name of the file to which the metadata should be exported if new_file is True. 
                Default is "new_file.nc".

        Returns:
            None. The function modifies the metadata of the netCDF file and optionally exports it to a new file.
        """
        default_attributes = [
            "Title", "Institution", "Source",
            "History", "References", "Conventions",
            "Creator_Author", "Project", "Description"
        ]
        if attributes is None:
            attributes = default_attributes
        try:
            if not isinstance(attributes, list):
                raise ValueError("attributes must be a list")
            for attribute in attributes:
                if not isinstance(attribute, str):
                    raise ValueError("attributes must contain only strings")
                self.attrs[attribute] = input(f"{attribute} - Enter value: ")
        except ValueError as e:
            print(f"An error occurred: {e}")
        from .file import File      
        if new_file:
            File.export_to_file(self, filename)
        netCDF_Metadata.read_global_metadata(self)
    def insert_netCDF_global_metadata_dict(self, dictionary, new_file=False, filename="new_file.nc"):
        """
        Insert global metadata into a netCDF file.

        Args:
            self (NetCDFFile): An instance of the NetCDFFile class.
            dictionary (dict): A dictionary containing the global metadata to be inserted into the netCDF file.
            new_file (bool, optional): A boolean flag indicating whether to export the modified netCDF file to a new file. Default is False.
            filename (str, optional): The filename of the new netCDF file to be exported. Default is 'new_file.nc'.

        Raises:
            TypeError: If the dictionary input is not of type dict.

        Returns:
            None. The function modifies the netCDF file by inserting the global metadata attributes. If new_file is True, it also exports the modified netCDF file to a new file.
        """
        if not isinstance(dictionary, dict):
            raise TypeError(f"{dictionary} is not a dictionary.")
        
        for key, value in dictionary.items():
            self.attrs[key] = value
        from .file import File
        if new_file:
            File.export_to_file(self, filename)
        netCDF_Metadata.read_global_metadata(self)
    def insert_netCDF_global_metadata_json(self, json_file, new_file=False, filename="new_file.nc"):
        """
        Inserts global metadata from a JSON file into a netCDF file.

        Args:
            self: The instance of the class calling the function.
            json_file (str): The path to the JSON file containing the metadata.
            new_file (bool, optional): Indicates whether a new netCDF file should be created. Default is False.
            filename (str, optional): Specifies the name of the new netCDF file. Default is "new_file.nc".

        Raises:
            FileNotFoundError: If there is an error opening the JSON file.
            json.JSONDecodeError: If there is an error decoding the JSON file.
            ValueError: If the filename is invalid.
            FileExistsError: If the filename already exists.
            ValidationError: If the JSON file does not match the specified schema.

        Returns:
            None
        """
        schema = {
            "type": "object",
            "patternProperties": {
                ".*": { "type": "string" }
            },
            "additionalProperties": False
        }

        try:
            with open(json_file, 'r') as file:
                metadata = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("Error opening JSON file. Please check if the file exists or if there are any permission issues.")
        except json.JSONDecodeError:
            raise json.JSONDecodeError("Error decoding JSON file. Please check if the file contains valid JSON.")
        
        try:
            # Validate JSON against schema
            jsonschema.validate(instance=metadata, schema=schema)
        except ValidationError as e:
            raise ValidationError(str(e))
        from .file import File
        if new_file:
            File.export_to_file(self, filename)
        netCDF_Metadata.read_global_metadata(self)
    def insert_netCDF_global_metadata(self, via="input", **kwargs):
        """
        Insert global metadata into a NetCDF file.

        Parameters:
        via (str, optional): The method of providing metadata. Can be "dict", "json", or "input". Defaults to "input".
        **kwargs: Additional keyword arguments for the specific method.

        Raises:
        ValueError: If the provided 'via' parameter is not valid or if there is an error inserting the metadata.

        Returns:
        None. The method modifies the metadata of the NetCDF file.
        """
        via_lower = via.lower()
        try:
            if via_lower == "dict":
                netCDF_Metadata.insert_netCDF_global_metadata_dict(self, **kwargs)
            elif via_lower == "json":
                netCDF_Metadata.insert_netCDF_global_metadata_json(self, **kwargs)
            elif via_lower == "input":
                netCDF_Metadata.insert_netCDF_global_metadata_input(self, **kwargs)
            else:
                raise ValueError(f"{via} is not a valid metadata input.")
        except Exception as e:
            raise ValueError(f"Error inserting netCDF metadata: {str(e)}")
class ParquetMetadata(pd.DataFrame):
    """
    The `ParquetMetadata` class is a subclass of `pd.DataFrame` that provides methods for reading and inserting metadata into Parquet files. It allows users to read the metadata of a Parquet file and print the attributes of each column. Users can also insert metadata into a Parquet file using various methods such as providing metadata through user input, a dictionary, or a JSON file.

    Main functionalities:
    - Reading the metadata of a Parquet file and printing the attributes of each column
    - Inserting metadata into a Parquet file using user input, a dictionary, or a JSON file

    Methods:
    - read_parquet_metadata(attributes=None, cols=None): Reads the metadata of a Parquet file and prints the attributes of each column.
    - insert_parquet_metadata_input(attributes=None, cols=None, new_file=False, filename="new_file.parquet"): Inserts metadata for columns in a Parquet file.
    - insert_parquet_metadata_dict(dictionary, cols=None, new_file=False, filename="new_file.parquet"): Inserts metadata into a Parquet file based on a given dictionary.
    - insert_parquet_metadata_json(json_file, new_file=False, filename="new_file.parquet"): Inserts metadata from a JSON file into a Parquet file.
    - insert_parquet_metadata(via="input", **kwargs): Inserts metadata into a Parquet file.

    Fields:
    - No significant fields.
    """
    def read_parquet_metadata(self, attributes=None, cols=None):
        """
        Reads the metadata of a Parquet file and prints the attributes of each column.

        Args:
            attributes (list, optional): A list of attributes to filter the metadata. If not provided, all attributes will be printed.
            cols (list, optional): A list of column names to filter the columns. If not provided, metadata of all columns will be printed.

        Returns:
            None

        Example Usage:
            # Example 1: Read metadata of all columns
            read_parquet_metadata()

            # Example 2: Read metadata of specific columns
            read_parquet_metadata(cols=['column1', 'column2'])

            # Example 3: Read metadata of specific attributes
            read_parquet_metadata(attributes=['attribute1', 'attribute2'])

            # Example 4: Read metadata of specific columns and attributes
            read_parquet_metadata(cols=['column1', 'column2'], attributes=['attribute1', 'attribute2'])
        """
        if isinstance(self, pd.DataFrame):
            self = pa.Table.from_pandas(self)
        if cols is None:
            for i in range(self.num_columns):
                field = self.field(i)
                col = field.name
                print(col)
                if field.metadata is None:
                    print("    No attributes were found for this column.")
                else:
                    metadata = {key.decode('utf-8'): value.decode('utf-8') for key, value in field.metadata.items()}
                    if attributes:
                        for attr in attributes:
                            if attr in metadata:
                                print(f"    {attr}: {metadata[attr]}")
                            else:
                                print(f"    The '{attr}' attribute was not found in this column's metadata.")
                    else:
                        for key, value in metadata.items():
                            print(f"    {key}: {value}") 
        else:
            for i in range(self.num_columns):
                field = self.field(i)
                col = field.name
                if col in cols:
                    print(col)
                    if field.metadata is None:
                        print("    No attributes were found for this column.")
                    else:
                        metadata = {key.decode('utf-8'): value.decode('utf-8') for key, value in field.metadata.items()}
                        if attributes:
                            for attr in attributes:
                                if attr in metadata:
                                    print(f"    {attr}: {metadata[attr]}")
                                else:
                                    print(f"    The '{attr}' attribute was not found in this column's metadata.")
                        else:
                            for key, value in metadata.items():
                                print(f"    {key}: {value}")
    def insert_parquet_metadata_input(self, attributes=None, cols=None, new_file=False, filename="new_file.parquet"):
        """
        Insert metadata for columns in a Parquet file.

        Args:
            attributes (list, optional): A list of attributes for which metadata needs to be inserted. If not provided, default attributes are used.
            cols (list, optional): A list of columns for which metadata needs to be inserted. If not provided, metadata is inserted for all columns in the DataFrame.
            new_file (bool, optional): A boolean indicating whether to export the DataFrame to a new Parquet file. Default is False.
            filename (str, optional): The name of the new Parquet file. Default is "new_file.parquet".

        Returns:
            pyarrow.Table: A Parquet table with the inserted metadata.

        Example Usage:
            # Insert metadata for all columns in a DataFrame and export it to a Parquet file
            df.insert_parquet_metadata_input()

            # Insert metadata for specific columns in a DataFrame and export it to a new Parquet file
            df.insert_parquet_metadata_input(attributes=['Description', 'Units'], cols=['col1', 'col2'], new_file=True, filename='metadata.parquet')
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
        table = pa.Table.from_pandas(self, schema=table_schema)
        from .file import File 
        if new_file:
            File.export_to_file(table, filename)
        return table
    def insert_parquet_metadata_dict(self, dictionary, cols=None, new_file=False, filename="new_file.parquet"):
        """
        Inserts metadata into a Parquet file based on a given dictionary.

        Args:
            dictionary (dict): A dictionary containing the metadata to be inserted into the Parquet file.
            cols (list, optional): A list of column names to specify which columns the metadata should be inserted into. 
                If not provided, metadata will be inserted into all columns. Default is None.
            new_file (bool, optional): A boolean value indicating whether to create a new Parquet file with the inserted metadata. 
                Default is False.
            filename (str, optional): The name of the new Parquet file to be created. Default is "new_file.parquet".

        Returns:
            pyarrow.Table: A Parquet table with the inserted metadata.

        Raises:
            ValueError: If the dictionary parameter is not provided.
            AttributeError: If the dictionary parameter is not a dictionary.

        Example Usage:
            # Create a DataFrame
            df = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})

            # Define a dictionary with metadata
            metadata_dict = {'A': 'This is column A', 'B': 'This is column B'}

            # Insert metadata into the Parquet file
            df.insert_parquet_metadata_dict(metadata_dict, new_file=True, filename='new_file.parquet')
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
            table = pa.Table.from_pandas(self, schema=table_schema)
            from .file import File       
            if new_file:
                File.export_to_file(table, filename)
            return table  
        else:
            raise AttributeError(f"{dictionary} is not a dictionary.")
    def insert_parquet_metadata_json(self, json_file, new_file=False, filename="new_file.parquet"):
        """
        Inserts metadata from a JSON file into a Parquet file.

        Args:
            json_file (str): The path to the JSON file containing the metadata.
            new_file (bool, optional): Indicates whether a new Parquet file should be created. Defaults to False.
            filename (str, optional): The name of the new Parquet file. Defaults to "new_file.parquet".

        Returns:
            pyarrow.Table: The Parquet table with the updated metadata.

        Raises:
            IOError: If there is an error opening the JSON file.
            ValidationError: If the JSON data does not match the predefined schema.
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
            # Validate JSON against schema
            jsonschema.validate(instance=json_data, schema=schema)
        except ValidationError as e:
            raise ValidationError(str(e))
        cols_dtypes = Statistics.get_cols_dtypes(self)
        cols_dtypes = [[col, "string"] if dtype == "category" else [col, str(dtype)] for col, dtype in cols_dtypes]
        metadata = []
        for col in cols_dtypes:
            if col[0] in json_data:
                col_metadata = json_data[col[0]]
                metadata.append(col_metadata)
            else:
                metadata.append(None)
        cols_dtypes = zip(cols_dtypes, metadata)
        schema = [pa.field(col_dtype[0], pa.type_for_alias(col_dtype[1]), metadata=meta) for col_dtype, meta in cols_dtypes]
        table_schema = pa.schema(schema)
        table = pa.Table.from_pandas(self, schema=table_schema)
        from .file import File
        if new_file:
            File.export_to_file(table, filename)
        return table
    def insert_parquet_metadata(self, via="input", **kwargs):
        """
        Insert metadata into a Parquet file.

        Parameters:
        - via (str): The method of providing metadata. It can be "dict", "json", or "input".
        - **kwargs: Additional keyword arguments for the specific method.

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