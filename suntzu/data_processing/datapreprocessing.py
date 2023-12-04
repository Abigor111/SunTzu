import polars as pl
#from .dataloading import Loading
class PreProcessing:
    #def __init__(self, path):
    #    self.loading = Loading.read_file(path)  
    #    self.df = self.loading 
    @staticmethod
    def view(self):
        """
        Returns the head of the DataFrame if it is not empty.
        Raises a ValueError if the DataFrame is empty.
        """
        try:
            if self.shape[0] == 0:
                raise ValueError("No DataFrame loaded yet.")
            return self.head()
        except ValueError as e:
            raise ValueError(f"Error: {e}")

    def get_dims(self):
        try:
            if self.is_empty():
                raise ValueError("No DataFrame loaded yet.")
            print(f"Cols: {self.shape[1]}")
            print(f"Rows: {self.shape[0]}")
        except ValueError as e:
            print(f"Error: {e}")
