import pyarrow as pa # type: ignore
import jsonschema # type: ignore
import pyarrow.parquet as pq # type: ignore
import json # type: ignore
from jsonschema.exceptions import ValidationError # type: ignore
import pandas as pd # type: ignore
import xarray as xr # type: ignore
from .statistics import Statistics
from typing import Optional

class netCDF_Metadata(xr.Dataset):
    """
    A subclass of `xr.Dataset` that provides methods for reading and inserting metadata into a netCDF file. It also includes methods for reading and inserting global metadata attributes.

    Methods:
        - get_file_variables(): Returns a list of variables in the NetCDF file.
        
        - read_netCDF_metadata(variables=None, attributes=None): Reads and prints metadata information from a NetCDF file.
        
        - insert_netCDF_metadata_input(variables=None, attributes=None, new_file=False, filename="new_file.nc"): Prompts the user to input metadata for specified variables in a NetCDF file.
        
        - insert_netCDF_metadata_dict(dictionary, variables=None, new_file=False, filename="new_file.nc"): Inserts metadata into a NetCDF file using a dictionary.
        
        - insert_netCDF_metadata_json(json_file, new_file=False, filename="new_file.nc"): Inserts metadata from a JSON file into a NetCDF file.
        
        - insert_netCDF_metadata(via="input", kwargs): Inserts metadata into the NetCDF file using the specified method.
        
        
        - read_global_metadata(attributes=None): Prints the global metadata attributes of the dataset.
        
        - insert_netCDF_global_metadata_input(attributes=None, new_file=False, filename="new_file.nc"): Inserts global metadata into a NetCDF file using user input.
        
        - insert_netCDF_global_metadata_dict(dictionary, new_file=False, filename="new_file.nc"): Inserts global metadata into a NetCDF file using a dictionary.
        
        - insert_netCDF_global_metadata_json(json_file, new_file=False, filename="new_file.nc"): Inserts global metadata from a JSON file into a NetCDF file.
        
        - insert_netCDF_global_metadata(via="input", kwargs): Inserts global metadata into a NetCDF file using the specified method.
    """
    def get_file_variables(self: xr.Dataset) -> list:
        """
        Get the variables of the file.

        Returns:
            list: A list of variables in the file.
        """
        # Create a list of the keys in the variables dictionary
        variables = list(self.variables.keys())
        # Return the list of variables
        return variables
    def read_netCDF_metadata(self: xr.Dataset, variables: Optional[list[str]] = None, attributes: Optional[list[str]] = None) -> None:
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
        def read_variable_metadata(var_name: str, var):
            # Print the variable name
            print(f"Variable: {var_name}")
            # Check if the variable has any attributes
            if not var.attrs:
                # Check if the variable has any values
                if var.values is not None:
                    # Print the values
                    print(f"    Values: {var.values}")
                else:
                    # Print that no values were found
                    print("No values were found")
                # Print that no attributes were found for this variable
                print("    No attributes were found for this variable.")
            else:
                # Print the values
                print(f"    Values: {var.values}")
                # Print the attributes
                print("    Attributes:")
                # Iterate through the attributes
                for key, value in var.attrs.items():
                    # Check if the attributes are in the list of attributes to be read
                    if attributes is None or key in attributes:
                        # Print the key and value
                        print(f"     {key}: {value}")

        # Check if a list of variables was provided
        if variables is None:
            # If not, set the variables to the keys of the variables dictionary
            variables = list(self.variables.keys())
        # Iterate through the variables
        for var_name in variables:
            # Try to retrieve the coordinate variable
            try:
                coord_var = self.coords[var_name]
                # Call the function to read the metadata
                read_variable_metadata(var_name, coord_var)
            # If an error occurs, print the error message
            except (KeyError, AttributeError) as e:
                print(f"Error occurred while retrieving metadata for variable {var_name}: {str(e)}")
    def insert_netCDF_metadata_input(self: xr.Dataset, variables: Optional[list[str]]=None, attributes: Optional[list[str]]=None, filename: Optional[str]=None) -> None:
            """
            Insert metadata attributes for specified variables in a netCDF file.

            Parameters:
            - self (xr.Dataset): The netCDF dataset.
            - variables (Optional[list[str]]): List of variable names to input metadata for. If not provided, all variables are used.
            - attributes (Optional[list[str]]): List of attribute names to input. If not provided, a default list is used.
            - filename (Optional[str]): Name of the file to save the updated dataset. If not provided, the dataset is not saved to a file.
        
            Returns:
            - None
            """
        
            # Define default attributes if not provided
            default_attributes = [
                "Units", "Long_Name", "Standard_Name/Short_Name", 
                "Valid_Min", "Valid_Max", "Missing_Value", 
                "Fill_Value", "Scale_Factor", "Add_Offset", 
                "Coordinates", "Axis", "Description"
            ]
            # Check if attributes is None, if so set it to the default_attributes
            if attributes is None:
                attributes = default_attributes

            # Check if variables is None, if so set it to the variables in the file
            if variables is None:
                variables = Statistics.get_file_variables(self)

            # Loop through each variable in the file
            for coord_name in variables:
                try:
                    # Loop through each attribute in the attributes list
                    for attribute in attributes:
                        # Set the attribute value for the current variable
                        self[coord_name].attrs[attribute] = input(f"{coord_name}: {attribute} - Enter value: ")
                except KeyError as e:
                    # Raise a KeyError if the variable is not found
                    raise KeyError(f"Variable {coord_name} not found.") from e
            # Import the File class
            from .library_settings import Settings
            # Check if a filename is given, if so export the file to that filename
            if filename:
                Settings.export_to_file(self, filename)
            # Read the netCDF metadata
            netCDF_Metadata.read_netCDF_metadata(self)
    def insert_netCDF_metadata_dict(self: xr.Dataset, dictionary: dict, variables: Optional[list[str]]=None, filename: Optional[str]=None) -> None:
        """
        Inserts metadata into specified variables of a netCDF file using a provided dictionary.

        Args:
        - self (xr.Dataset): The netCDF dataset to which metadata will be added.
        - dictionary (dict): A dictionary containing metadata attributes and their values.
        - variables (Optional[list[str]]): A list of variable names to which the metadata will be applied. If not provided, all variables are used.
        - filename (Optional[str]): The name of the file to save the updated dataset. If not provided, the dataset is not saved to a file.
        
        Returns:
        - None

        Raises:
        - ValueError: If `dictionary` is not provided.
        - AttributeError: If `dictionary` is not a dictionary.
        """
        # Check if the dictionary is None
        if dictionary is None:
            # Raise a ValueError if the dictionary is None
            raise ValueError("Please provide a dictionary.")
        # Check if the variables is None
        if variables is None:
            # Set the variables to the file variables if the variables is None
            variables = Statistics.get_file_variables(self)
        # Check if the dictionary is a dictionary
        if isinstance(dictionary, dict):
            # Loop through the variables
            for var in variables:
                # Loop through the dictionary items
                for key, value in dictionary.items():
                    # Set the attribute of the variable to the value
                    self[var].attrs[key] = value
        # Raise an AttributeError if the dictionary is not a dictionary
        else:
            raise AttributeError(f"{dictionary} is not a dictionary.")
        # Import the File class
        from .library_settings import Settings
        # Check if a filename is provided
        if filename:
            # Export the data to a file if a filename is provided
            Settings.export_to_file(self, filename)
        # Read the netCDF metadata
        netCDF_Metadata.read_netCDF_metadata(self)
    def insert_netCDF_metadata_json(self: xr.Dataset, json_file: str, filename: Optional[str]=None) -> None:
        """
        Inserts metadata into a netCDF file from a JSON file.

        Parameters:
        - self (xr.Dataset): The netCDF dataset object.
        - json_file (str): The path to the JSON file containing the metadata.
        - filename (Optional[str]): The name of the file to save the updated dataset.

        Raises:
        - IOError: If there is an error opening the JSON file.
        - ValidationError: If the JSON content does not match the predefined schema.

        Returns:
        - None

        """
        # Define a schema for validating JSON
        schema = {
            # The root element is an object
            "type": "object",
            # The object can have properties that match a given pattern
            "patternProperties": {
                # The pattern can be any string
                ".*": {
                    # The properties of the object can be an object with the following pattern
                    "type": "object",
                    "patternProperties": {
                        # The pattern can be any string
                        ".*": {
                            # The property is a string
                            "type": "string",
                        }
                    }
                },
                # There can be no additional properties
                "additionalProperties": False
                }   
            }   
        # Try to open the JSON file
        try:
            with open(json_file, 'r') as file:
                metadata = json.load(file)
        # If the file cannot be opened, raise an error
        except IOError:
            raise IOError("Error opening JSON file. Please check if the file exists or if there are any permission issues.")
        # Try to validate the JSON against the schema
        try:
            # Validate JSON against schema
            jsonschema.validate(instance=metadata, schema=schema)
        # If the validation fails, raise an error
        except ValidationError as e:
            raise ValidationError(str(e))
        # Set the metadata in the object
        for var, attributes in metadata.items():
            for attr, value in attributes.items():
                self[var].attrs[attr] = value
        # Import the File class
        from .library_settings import Settings   
        # If a filename is given, export the object to a file
        if filename:
            Settings.export_to_file(self, filename)
        # Read the netCDF metadata
        netCDF_Metadata.read_netCDF_metadata(self)
    def insert_netCDF_metadata(self: xr.Dataset, via: str="input", **kwargs) -> None:
        """
        Insert metadata into the netCDF file.

        Parameters:
            via (str, optional): The method of providing metadata. Can be "dict", "json", or "input". Defaults to "input".
            **kwargs: Additional keyword arguments for the specific method.

        Raises:
            ValueError: If `via` is not a valid metadata input.
        """
        # Convert the via string to lower case
        via_lower = via.lower()
        try:
            # Check if the via string is "dict"
            if via_lower == "dict":
                # If so, call the insert_netCDF_metadata_dict function and pass the kwargs
                netCDF_Metadata.insert_netCDF_metadata_dict(self, **kwargs)
            # Check if the via string is "json"
            elif via_lower == "json":
                # If so, call the insert_netCDF_metadata_json function and pass the kwargs
                netCDF_Metadata.insert_netCDF_metadata_json(self, **kwargs)
            # Check if the via string is "input"
            elif via_lower == "input":
                # If so, call the insert_netCDF_metadata_input function and pass the kwargs
                netCDF_Metadata.insert_netCDF_metadata_input(self, **kwargs)
            # If none of the above conditions are met
            else:
                # Raise a ValueError with the invalid via string
                raise ValueError(f"{via} is not a valid metadata input.")
        # If any exception occurs
        except Exception as e:
            # Raise a ValueError with the exception message
            raise ValueError(f"Error inserting netCDF metadata: {str(e)}")
    def get_attrs(self):
        return self.attrs
    def read_global_metadata(self: xr.Dataset, attributes: Optional[list[str]]=None) -> None:
        """
        Print the global metadata attributes of the dataset.

        Args:
            attributes (list): List of attribute names to print. If None, all attributes will be printed.
        """
        attrs = netCDF_Metadata.get_attrs(self)
        # Check if there are any global attributes
        if not attrs:
            # Print a message if there are no global attributes
            print("No Global Attributes were found.")
        else:
            # Check if the user provided any attributes to display
            if attributes is None:
                # If no attributes provided, display all global attributes
                for attr_name, attr_value in attrs.items():
                    # Print the attribute name and value
                    print(attr_name, ":", attr_value)
            else:
                # If attributes provided, display only the requested attributes
                for attr_name, attr_value in attrs.items():
                    # Check if the attribute is in the user provided attributes
                    if attr_name in attributes:
                        # Print the attribute name and value
                        print(attr_name, ":", attr_value)
    def insert_netCDF_global_metadata_input(self: xr.Dataset, attributes: Optional[list[str]]=None, new_file: bool=False, filename: str="new_file.nc") -> None:
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
        # This list contains the default attributes that will be used if the user does not provide any
        default_attributes = [
            "Title", "Institution", "Source",
            "History", "References", "Conventions",
            "Creator_Author", "Project", "Description"
        ]
        # If the user does not provide any attributes, use the default ones
        if attributes is None:
            attributes = default_attributes
        try:
            # Check if the attributes provided by the user is a list
            if not isinstance(attributes, list):
                # Raise a ValueError if the attributes is not a list
                raise ValueError("attributes must be a list")
            # Check if the attributes list contains only strings
            for attribute in attributes:
                if not isinstance(attribute, str):
                    # Raise a ValueError if the attributes list contains a non-string element
                    raise ValueError("attributes must contain only strings")
                # Set the value of the given attribute
                self.attrs[attribute] = input(f"{attribute} - Enter value: ")
        except ValueError as e:
            # Print the error message
            print(f"An error occurred: {e}")
        # Import the File class
        from .library_settings import Settings      
        # If the user wants to create a new file, export the metadata to a file
        if new_file:
            Settings.export_to_file(self, filename)
        # Read the global metadata from the netCDF file
        netCDF_Metadata.read_global_metadata(self)
    def insert_netCDF_global_metadata_dict(self: xr.Dataset, dictionary: dict, new_file: bool =False, filename: str="new_file.nc") -> None:
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
        # Check if the input is a dictionary
        if not isinstance(dictionary, dict):
            # Raise a TypeError if the input is not a dictionary
            raise TypeError(f"{dictionary} is not a dictionary.")
        
        # Iterate through the dictionary
        for key, value in dictionary.items():
            # Set the attribute value
            self.attrs[key] = value
        # Import the File class
        from .library_settings import Settings
        # If a new file is being created
        if new_file:
            # Export the object to a file
            Settings.export_to_file(self, filename)
        # Read the global metadata
        netCDF_Metadata.read_global_metadata(self)
    def insert_netCDF_global_metadata_json(self: xr.Dataset, json_file: str, new_file: bool=False, filename: str ="new_file.nc") -> None:
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
        # Define a schema for validating the JSON file
        schema = {
            # The type of the JSON object should be "object"
            "type": "object",
            # The patternProperties should be a key-value pair where the key is any string and the value is a string
            "patternProperties": {
                ".*": { "type": "string" }
            },
            # There should be no additional properties
            "additionalProperties": False
        }

        # Try to open the JSON file and load its content
        try:
            with open(json_file, 'r') as file:
                metadata = json.load(file)
        # If the file does not exist or if there are permission issues, raise an error
        except FileNotFoundError:
            raise FileNotFoundError("Error opening JSON file. Please check if the file exists or if there are any permission issues.")
        except json.JSONDecodeError:
            # If the file contains invalid JSON, raise an error
            raise json.JSONDecodeError("Error decoding JSON file. Please check if the file contains valid JSON.")
        
        # Try to validate the JSON against the schema
        try:
            # Validate JSON against schema
            jsonschema.validate(instance=metadata, schema=schema)
        # If the validation fails, raise a ValidationError
        except ValidationError as e:
            raise ValidationError(str(e))
        # If the new file flag is set, export the metadata to a file
        from .library_settings import Settings
        if new_file:
            Settings.export_to_file(self, filename)
        # If the read global metadata flag is set, read the global metadata
        netCDF_Metadata.read_global_metadata(self)
    def insert_netCDF_global_metadata(self: xr.Dataset, via: str="input", **kwargs) -> None:
        """
        Insert global metadata into a NetCDF file.

        Parameters:
        via (str, optional): The method of providing metadata. Can be "dict", "json", or "input". Defaults to "input".
        kwargs: Additional keyword arguments for the specific method.

        Raises:
        ValueError: If the provided 'via' parameter is not valid or if there is an error inserting the metadata.

        Returns:
        None. The method modifies the metadata of the NetCDF file.
        """
        # Convert the via string to lower case
        via_lower = via.lower()
        try:
            # Check if the via string is "dict"
            if via_lower == "dict":
                # If so, call the function to insert netCDF global metadata from a dictionary
                netCDF_Metadata.insert_netCDF_global_metadata_dict(self, **kwargs)
            # Check if the via string is "json"
            elif via_lower == "json":
                # If so, call the function to insert netCDF global metadata from JSON
                netCDF_Metadata.insert_netCDF_global_metadata_json(self, **kwargs)
            # Check if the via string is "input"
            elif via_lower == "input":
                # If so, call the function to insert netCDF global metadata from input
                netCDF_Metadata.insert_netCDF_global_metadata_input(self, **kwargs)
            # If the via string is not valid, raise a ValueError
            else:
                raise ValueError(f"{via} is not a valid metadata input.")
        # If an error occurs, raise a ValueError with the error message
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
    def read_parquet_metadata(self: pd.DataFrame, attributes: Optional[list[str]] = None, cols: Optional[list[str]] = None) -> None:        
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
        # Check if the object is a pandas DataFrame
        if isinstance(self, pd.DataFrame):
            # If it is, convert it to a pyarrow Table
            self = pa.Table.from_pandas(self)
        # If no columns are specified, print the names of all the columns
        if cols is None:
            for i in range(self.num_columns):
                # Get the field from the table
                field = self.field(i)
                # Get the name of the column
                col = field.name
                print(col)
                # If there is no metadata for the column, print a message
                if field.metadata is None:
                    print("    No attributes were found for this column.")
                else:
                    # If there is metadata, decode it and print it
                    metadata = {key.decode('utf-8'): value.decode('utf-8') for key, value in field.metadata.items()}
                    if attributes:
                        # If specific attributes are specified, print them
                        for attr in attributes:
                            if attr in metadata:
                                print(f"    {attr}: {metadata[attr]}")
                            else:
                                print(f"    The '{attr}' attribute was not found in this column's metadata.")
                    else:
                        # If no attributes are specified, print all the metadata
                        for key, value in metadata.items():
                            print(f"    {key}: {value}") 
        else:
            # If specific columns are specified, print the metadata for those columns
            for i in range(self.num_columns):
                # Get the field from the table
                field = self.field(i)
                # Get the name of the column
                col = field.name
                if col in cols:
                    print(col)
                    # If there is no metadata for the column, print a message
                    if field.metadata is None:
                        print("    No attributes were found for this column.")
                    else:
                        # If there is metadata, decode it and print it
                        metadata = {key.decode('utf-8'): value.decode('utf-8') for key, value in field.metadata.items()}
                        if attributes:
                            # If specific attributes are specified, print them
                            for attr in attributes:
                                if attr in metadata:
                                    print(f"    {attr}: {metadata[attr]}")
                                else:
                                    print(f"    The '{attr}' attribute was not found in this column's metadata.")
                        else:
                            # If no attributes are specified, print all the metadata
                            for key, value in metadata.items():
                                print(f"    {key}: {value}")
    def insert_parquet_metadata_input(self: pd.DataFrame, attributes: Optional[list[str]]=None, cols: Optional[list[str]]=None, new_file: bool=False, filename: str="new_file.parquet") -> pa.Table:
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
        # Set default attributes
        default_attributes = ['Description', 'Units', 'Data Source', 'Valid Range or Categories']
        # If attributes is None, set it to the default attributes
        if attributes is None:
            attributes = default_attributes
        # If cols is None, set it to the list of columns
        if cols is None:
            cols = list(self.columns)
        # Initialize metadata list
        metadata = []
        # Get columns from the DataFrame
        columns = self.columns  
        # Set cols_set to the set of cols
        cols_set = set(cols)  
        # Iterate through each column
        for col in columns:
            # If col is in cols_set, add a dictionary to the metadata list
            if col in cols_set:
                col_metadata = {}
                # Iterate through the attributes
                for attribute in attributes:
                    # Get input for the attribute
                    data = input(f"{col}: {attribute} - Enter value: ")
                    # Add the attribute and input to the col_metadata dictionary
                    col_metadata[attribute] = data
                # Add the col_metadata dictionary to the metadata list
                metadata.append(col_metadata)
            # Otherwise, add None to the metadata list
            else:
                metadata.append(None)
        # Get dtypes from the DataFrame
        dtypes = self.dtypes
        # Set dtypes to "string" if dtype is "category", otherwise keep the dtype as is
        dtypes = ["string" if dtype == "category" else str(dtype) for dtype in dtypes]
        # Zip the columns, dtypes, and metadata
        cols_dtypes = zip(columns, dtypes, metadata)
        # Initialize the schema list
        schema = [pa.field(col, pa.type_for_alias(dtype), metadata=meta) for col, dtype, meta in cols_dtypes]
        # Create the table schema
        table_schema = pa.schema(schema)
        # Create the table from the DataFrame
        table = pa.Table.from_pandas(self, schema=table_schema)
        # Import the File class
        from .library_settings import Settings 
        # If new_file is True, export the table to a file
        if new_file:
            Settings.export_to_file(table, filename)
        # Return the table
        return table
    def insert_parquet_metadata_dict(self: pd.DataFrame, dictionary: dict, cols: Optional[list[str]] =None, new_file: bool =False, filename: str="new_file.parquet") -> pa.Table:
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

        # Check if the dictionary is provided
        if dictionary is None:
            # Raise an error if no dictionary is provided
            raise ValueError("Please provide a dictionary.")
        # If no columns are provided, use all columns
        if cols is None:
            cols = list(self.columns)
        # Get the columns, dtypes and metadata
        columns = self.columns
        dtypes = self.dtypes
        # Convert the dtypes to strings
        dtypes = ["string" if dtype == "category" else str(dtype) for dtype in dtypes]
        # Initialize the metadata list
        metadata = []
        # Check if the dictionary is a dictionary
        if isinstance(dictionary, dict):
            # Create a set of the columns
            cols_set = set(cols)
            # Iterate through the columns
            for col in columns:
                # If the column is in the set of columns, append the dictionary to the metadata list
                if col in cols_set:
                    metadata.append(dictionary)
                # Otherwise, append None
                else:
                    metadata.append(None)
            # Zip the columns, dtypes and metadata
            cols_dtypes = zip(columns, dtypes, metadata)
            # Create the schema
            schema = [pa.field(col, pa.type_for_alias(dtype), metadata=meta) for col, dtype, meta in cols_dtypes]
            # Create the table
            table_schema = pa.schema(schema)
            table = pa.Table.from_pandas(self, schema=table_schema)
            # Import the File class
            from .library_settings import Settings       
            # Export the table to a file
            if new_file:
                Settings.export_to_file(table, filename)
            # Return the table
            return table  
        else:
            # Raise an error if the dictionary is not a dictionary
            raise AttributeError(f"{dictionary} is not a dictionary.")
    def insert_parquet_metadata_json(self: pd.DataFrame, json_file: str, new_file: bool=False, filename: str ="new_file.parquet") -> pa.Table:
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
        # Define a schema for validating JSON data
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
        # Open the JSON file and load the data
        try:
            with open(json_file, 'r') as file:
                json_data = json.load(file)
        except IOError:
            raise IOError("Error opening JSON file. Please check if the file exists or if there are any permission issues.")
        # Validate JSON against schema
        try:
            jsonschema.validate(instance=json_data, schema=schema)
        except ValidationError as e:
            raise ValidationError(str(e))
        # Get the column names and data types from the DataFrame
        cols_dtypes = Statistics.get_cols_dtypes(self)
        # Convert category data types to string
        cols_dtypes = [[col, "string"] if dtype == "category" else [col, str(dtype)] for col, dtype in cols_dtypes]
        # Initialize an empty list to store the metadata
        metadata = []
        # Iterate through the columns and their data types
        for col in cols_dtypes:
            # If the column is in the JSON data, get the metadata
            if col[0] in json_data:
                col_metadata = json_data[col[0]]
                metadata.append(col_metadata)
            # Otherwise, append None
            else:
                metadata.append(None)
        # Zip the columns and their metadata together
        cols_dtypes = zip(cols_dtypes, metadata)
        # Initialize an empty list to store the schema
        schema = []
        # Iterate through the columns and their metadata
        for col_dtype, meta in cols_dtypes:
            # Create a field for the column with the appropriate data type and metadata
            schema.append(pa.field(col_dtype[0], pa.type_for_alias(col_dtype[1]), metadata=meta))
        # Create a table schema from the schema list
        table_schema = pa.schema(schema)
        # Create a table from the DataFrame and table schema
        table = pa.Table.from_pandas(self, schema=table_schema)
        # Import the File class
        from .library_settings import Settings
        # If a new file is being created, export the table to a file
        if new_file:
            Settings.export_to_file(table, filename)
        # Return the table
        return table
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
        # Convert the via parameter to lower case
        via_lower = via.lower()
        try:
            # If the via parameter is "dict", call the ParquetMetadata class method insert_parquet_metadata_dict
            if via_lower == "dict":
                ParquetMetadata.insert_parquet_metadata_dict(self, **kwargs)
            # If the via parameter is "json", call the ParquetMetadata class method insert_parquet_metadata_json
            elif via_lower == "json":
                ParquetMetadata.insert_parquet_metadata_json(self, **kwargs)
            # If the via parameter is "input", call the ParquetMetadata class method insert_parquet_metadata_input
            elif via_lower == "input":
                ParquetMetadata.insert_parquet_metadata_input(self, **kwargs)
            # If the via parameter is not valid, raise a ValueError
            else:
                raise ValueError(f"{via} is not a valid metadata input.")
        # If an exception occurs, raise a ValueError with the error message
        except Exception as e:
            raise ValueError(f"Error inserting netCDF metadata: {str(e)}")