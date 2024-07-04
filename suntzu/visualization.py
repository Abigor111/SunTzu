import pandas as pd # type: ignore
import matplotlib.pyplot as plt
from matplotlib.container import BarContainer
class Visualization(pd.DataFrame):
    def scatter_plot(self: pd.DataFrame, x: pd.Series, y: pd.Series, title: str =None, xlabel:str =None, ylabel: str =None,  rotation_xlabel: int = None, grid=False, legend: bool=True) -> None:
        """
        This function creates a scatter plot using the provided x and y series from a DataFrame.

        Parameters:
        self (pd.DataFrame): The DataFrame containing the x and y series.
        x (pd.Series): The x-axis series to be plotted.
        y (pd.Series): The y-axis series to be plotted.
        title (str): The title of the plot. Default is None.
        xlabel (str): The label for the x-axis. Default is None.
        ylabel (str): The label for the y-axis. Default is None.
        rotation_xlabel (int): The rotation angle for the x-axis labels. Default is None.
        grid (bool): A boolean indicating whether to display a grid on the plot. Default is False.
        legend (bool): A boolean indicating whether to display a legend on the plot. Default is True.
        filename (str): The name of the file to save the plot. Default is None.
        dpi (int): The resolution of the saved plot in dots per inch. Default is 100.

        Returns:
        None
        """
        if xlabel is None:
            xlabel = str(x)
        if ylabel is None:
            ylabel = str(y)
        if title is None:
            title = xlabel + " VS " + ylabel
        fig, ax = plt.subplots()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(grid)
        if rotation_xlabel is not None:
            plt.xticks(rotation=rotation_xlabel)
        if plt.gca().get_legend() is not None and legend:
            if any(label.get_label() for label in plt.gca().get_legend().get_texts()):
                plt.legend()
        if x in self.columns and y in self.columns:
            scattter = ax.scatter(x=self[x], y=self[y], zorder=2)
        else:
            raise ValueError(f"Columns '{x}' or '{y}' not found in DataFrame.")
        return scattter
    def lineplot(self: pd.DataFrame , x: pd.Series, y: pd.Series, title: str =None, xlabel:str =None, ylabel: str =None, rotation_xlabel: int = None, grid=False, legend: bool=True) -> None:
        """
        This function creates a line plot using the provided x and y series from a DataFrame.

        Parameters:
        self (pd.DataFrame): The DataFrame containing the x and y series.
        x (pd.Series): The x-axis series to be plotted.
        y (pd.Series): The y-axis series to be plotted.
        title (str): The title of the plot. Default is None.
        xlabel (str): The label for the x-axis. Default is None.
        ylabel (str): The label for the y-axis. Default is None.
        rotation_xlabel (int): The rotation angle for the x-axis labels. Default is None.
        grid (bool): A boolean indicating whether to display a grid on the plot. Default is False.
        legend (bool): A boolean indicating whether to display a legend on the plot. Default is True.

        Returns:
        None
        """
        if xlabel is None:
            xlabel = str(x)
        if ylabel is None:
            ylabel = str(y)
        if title is None:
            title = xlabel + " VS " + ylabel
        fig, ax = plt.subplots()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(grid)
        if rotation_xlabel is not None:
            plt.xticks(rotation=rotation_xlabel)
        if plt.gca().get_legend() is not None and legend:
            if any(label.get_label() for label in plt.gca().get_legend().get_texts()):
                plt.legend()
        if x in self.columns and y in self.columns:    
            line = ax.plot(self[x], self[y], color=plt.rcParams['lines.color'],
                                    linestyle=plt.rcParams['lines.linestyle'],
                                    linewidth=plt.rcParams['lines.linewidth'],
                                    marker=plt.rcParams['lines.marker'],
                                    markeredgecolor=plt.rcParams['lines.markeredgecolor'],
                                    markeredgewidth=plt.rcParams['lines.markeredgewidth'],
                                    markerfacecolor=plt.rcParams['lines.markerfacecolor'],
                                    markersize=plt.rcParams['lines.markersize'],
                                    zorder=2)
        else:
            raise ValueError(f"Columns '{x}' or '{y}' not found in DataFrame.")

        return line
    def multilineplot(self: pd.DataFrame , x: pd.Series, ys: list[pd.Series], colors: list[str] = ["blue", "green", "red"],title: str =None, xlabel:str =None, xlim: tuple = None, ylabel: str =None, ylim: tuple = None, rotation_xlabel: int = None, grid=False, legend: bool=True) -> None:
        """
        This function creates a multiline plot using the provided x and y series from a DataFrame.

        Parameters:
        self (pd.DataFrame): The DataFrame containing the x and y series.
        x (pd.Series): The x-axis series to be plotted.
        ys (list[pd.Series]): The y-axis series to be plotted.
        colors (list[str]): A list of colors for each line in the plot. Default is ["blue", "green", "red"].
        title (str): The title of the plot. Default is None.
        xlabel (str): The label for the x-axis. Default is None.
        xlim (tuple): The limits for the x-axis. Default is None.
        ylabel (str): The label for the y-axis. Default is None.
        ylim (tuple): The limits for the y-axis. Default is None.
        rotation_xlabel (int): The rotation angle for the x-axis labels. Default is None.
        grid (bool): A boolean indicating whether to display a grid on the plot. Default is False.
        legend (bool): A boolean indicating whether to display a legend on the plot. Default is True.

        Returns:
        None
        """
        if xlabel is None:
            xlabel = str(x)
        if ylabel is None:
            ylabel = str(ys)
        if title is None:
            title = xlabel + " VS " + ylabel
        fig, ax = plt.subplots()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(grid)
        if rotation_xlabel is not None:
            plt.xticks(rotation=rotation_xlabel)
        if plt.gca().get_legend() is not None and legend:
            if any(label.get_label() for label in plt.gca().get_legend().get_texts()):
                plt.legend()
        if xlim is not None:
            ax.set_xlim(xlim)
        if ylim is not None:
            ax.set_ylim(ylim)
        i= 0
        for y in ys:
            if x in self.columns and y in self.columns:    
                ax.plot(self[x], self[y], color=colors[i],zorder=2)
            else:
                raise ValueError(f"Columns '{x}' or '{y}' not found in DataFrame.")
            if i + 1 < len(colors):
                i+=1
        
        plt.show()
    def barplot(self: pd.DataFrame , x: pd.Series, y: pd.Series, title: str =None, xlabel:str =None, ylabel: str =None, rotation_xlabel: int = None, grid=False, legend: bool=True) -> BarContainer:
        """
        This function creates a bar plot using the provided x and y series from a DataFrame.

        Parameters:
        self (pd.DataFrame): The DataFrame containing the x and y series.
        x (pd.Series): The x-axis series to be plotted.
        y (pd.Series): The y-axis series to be plotted.
        title (str): The title of the plot. Default is None.
        xlabel (str): The label for the x-axis. Default is None.
        ylabel (str): The label for the y-axis. Default is None.
        rotation_xlabel (int): The rotation angle for the x-axis labels. Default is None.
        grid (bool): A boolean indicating whether to display a grid on the plot. Default is False.
        legend (bool): A boolean indicating whether to display a legend on the plot. Default is True.

        Returns:
        BarContainer: The container object containing the bars of the bar plot.
        """
        if xlabel is None:
            xlabel = str(x)
        if ylabel is None:
            ylabel = str(y)
        if title is None:
            title = xlabel + " VS " + ylabel
        fig, ax = plt.subplots()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(grid)
        if rotation_xlabel is not None:
            plt.xticks(rotation=rotation_xlabel)
        if plt.gca().get_legend() is not None and legend:
            if any(label.get_label() for label in plt.gca().get_legend().get_texts()):
                plt.legend()
        try:
            if x in self.columns and y in self.columns:
                bars = ax.bar(self[x], self[y], zorder=2)
            else:
                raise ValueError(f"Columns '{x}' or '{y}' not found in DataFrame.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return
        return bars