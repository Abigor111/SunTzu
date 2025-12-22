import pandas as pd
import matplotlib.pyplot as plt
import pyarrow.parquet as pq
from cycler import cycler

import os
class Settings:
    @staticmethod
    def get_file_extension(path):
        """
        Returns the file extension of a given file path.

        Args:
            path (str): The file path.

        Returns:
            str: The file extension.
        """
        return os.path.splitext(path)[1]

    def export_to_file(self: pd.DataFrame, filename: str):
        """
        Exports data to a file with a specified filename.

        Args:
            filename (str): The name of the file to export the data to.

        Raises:
            ValueError: If the file extension is not valid.
            FileExistsError: If the file already exists.
        """

        if not Settings.get_file_extension(filename) == ".parquet":
            raise ValueError(f"Invalid file extension. Please provide a valid filename. Valid file extesion: .parquet")
        # If the file already exists in returns an error, so we check it first
        if not os.path.isfile(filename):
            pq.write_table(self, filename, compression=None)        
        else:
            raise FileExistsError(f"{filename} already exists. Please change it or delete it.")
    def increase_graph_size(width: int, height: int) -> None:
        """
        This function increases the size of the graph.

        Parameters:
        width (int): The width of the graph in inches.
        height (int): The height of the graph in inches.

        Returns:
        None
        """
        plt.rcParams['figure.figsize'] = (width, height)
    def set_grid(grid_backgroundcolor: str ="#EBEBEB", grid_border: list[bool] = [True, True, True, True], gridline: str ="white", gridlinewidth: int | float =1.2, minorgridlines: bool=False):
        """
        This function sets the grid properties of the plot.

        Parameters:
        grid_backgroundcolor (str): The background color of the grid. Default is "#EBEBEB".
        grid_border (list[bool]): A list of four boolean values indicating the visibility of the top, right, bottom, and left borders of the grid. Default is [True, True, True, True].
        gridline (str): The color of the grid lines. Default is "white".
        gridlinewidth (int | float): The width of the grid lines. Default is 1.2.
        minorgridlines (bool): A boolean indicating whether to display minor grid lines. Default is False.

        Returns:
        None
        """
        plt.rcParams['axes.facecolor'] = grid_backgroundcolor  
        plt.rcParams['axes.grid.axis'] = 'both'
        plt.rcParams['axes.grid.which'] = 'major'  
        plt.rcParams['grid.color'] = gridline  
        plt.rcParams['grid.linewidth'] = gridlinewidth 
        plt.rcParams['axes.grid'] = True
        plt.rcParams['axes.spines.top'] = grid_border[0]  
        plt.rcParams['axes.spines.right'] = grid_border[1]
        plt.rcParams['axes.spines.bottom'] = grid_border[2]  
        plt.rcParams['axes.spines.left'] = grid_border[3]
    def set_full_view(all_cols: bool=True, rows_fullsize: bool=True, max_rowswidth: bool = False, max_colwidth: bool=True):
        """
        This function sets the display options for pandas DataFrame to show all columns, all rows, maximum width, or maximum column width.

        Parameters:
        all_cols (bool): If True, it sets the maximum number of columns to be displayed. Default is True.
        rows_fullsize (bool): If True, it sets the maximum number of rows to be displayed. Default is True.
        max_rowswidth (bool): If True, it sets the maximum width of the rows to be displayed. Default is False.
        max_colwidth (bool): If True, it sets the maximum width of the columns to be displayed. Default is True.

        Returns:
        None
        """
        if rows_fullsize:
            pd.set_option('display.max_rows', None)
        elif all_cols:
            pd.set_option('display.max_columns', None)
        elif max_rowswidth:
            pd.set_option('display.width', None)
        elif max_colwidth:
            pd.set_option('display.max_colwidth', None)
    def reset_settings(matplotlib=True, pandas=True):
        """
        This function resets the settings of matplotlib and pandas to their default values.

        Parameters:
        matplotlib (bool): A boolean indicating whether to reset the matplotlib settings. Default is True.
        pandas (bool): A boolean indicating whether to reset the pandas settings. Default is True.

        Returns:
        None
        """
        if pandas:
            pd.reset_option('all')
        if matplotlib:
            plt.rcdefaults()
    def set_labels_settings(font: str= "serif",labelcolor: str = "black", labelsize: int | str = "medium", labelweight: str = "normal", pad: int |str= 4):
        """
        This function sets the label properties of the plot.

        Parameters:
        font (str): The font family for the labels. Default is "serif".
        labelcolor (str): The color of the labels. Default is "black".
        labelsize (int | str): The size of the labels. Default is "medium".
        labelweight (str): The weight of the labels. Default is "normal".
        pad (int | str): The padding around the labels. Default is 4.

        Returns:
        None
        """
        plt.rcParams['axes.labelcolor'] = labelcolor
        plt.rcParams['axes.labelsize'] = labelsize
        plt.rcParams['axes.labelweight'] = labelweight
        plt.rcParams['axes.labelpad'] = pad
        plt.rcParams['font.family'] = font
    def set_marker_settings(size: int | float = 10, type: str = 'o', color: str | list[str] = "green", outline: str = "white", outlinewidth: int | float = 1):
        """
        This function sets the marker properties for scatter plots.

        Parameters:
        size (int | float): The size of the marker. Default is 10.
        type (str): The type of the marker. Default is 'o'.
        color (str | list[str]): The color(s) of the marker. Default is "green".
        outline (str): The color of the marker outline. Default is "white".
        outlinewidth (int | float): The width of the marker outline. Default is 1.

        Returns:
        None
        """
        plt.rcParams['scatter.marker'] = type
        plt.rcParams['axes.prop_cycle'] = cycler('color', [color, '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
        plt.rcParams['scatter.edgecolors'] = outline
        plt.rcParams['lines.linewidth'] = outlinewidth
        plt.rcParams['lines.markersize'] = size
    def set_title_settings(color: str = 'auto', location: str = 'center', size: int | str = 'large', weight: str = "bold", pad: int | float = 6.0) -> None:
        """
        This function sets the title properties of the plot.

        Parameters:
        color (str): The color of the title. Default is 'auto'.
        location (str): The location of the title. Default is 'center'.
        size (int | str): The size of the title. Default is 'large'.
        weight (str): The weight of the title. Default is 'bold'.
        pad (int | float): The padding around the title. Default is 6.0.

        Returns:
        None
        """
        plt.rcParams['axes.titlecolor'] = color
        plt.rcParams['axes.titlelocation'] = location
        plt.rcParams['axes.titlesize'] = size
        plt.rcParams['axes.titleweight'] = weight
        plt.rcParams['axes.titlepad'] = pad
    def set_line_settings(color: str = "green", linestyle: str ="-", linewidth: int | float = 1.5, marker: str = "None", markeredgecolor: str = 'auto', markeredgewidth: int | float = 1.0, markerfacecolor: str = 'auto', markersize: int | float = 6.0) -> None:
        """
        This function sets the line properties for plots.

        Parameters:
        color (str): The color of the line. Default is "green".
        linestyle (str): The style of the line. Default is "-".
        linewidth (int | float): The width of the line. Default is 1.5.
        marker (str): The marker style for data points. Default is "None".
        markeredgecolor (str): The color of the marker edge. Default is 'auto'.
        markeredgewidth (int | float): The width of the marker edge. Default is 1.0.
        markerfacecolor (str): The color of the marker face. Default is 'auto'.
        markersize (int | float): The size of the marker. Default is 6.0.

        Returns:
        None
        """
        plt.rcParams['lines.color'] = color
        plt.rcParams['lines.linestyle'] = linestyle
        plt.rcParams['lines.linewidth'] = linewidth
        plt.rcParams['lines.marker'] = marker
        plt.rcParams['lines.markeredgecolor'] = markeredgecolor
        plt.rcParams['lines.markeredgewidth'] = markeredgewidth
        plt.rcParams['lines.markerfacecolor'] = markerfacecolor
        plt.rcParams['lines.markersize'] = markersize