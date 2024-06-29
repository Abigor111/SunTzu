import itertools
from matplotlib.container import BarContainer
import numpy as np
import pandas as pd # type: ignore
import matplotlib.pyplot as plt
class Visualization:
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
        ax.set_ylabel("Teste")
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
    def show_bar_values(bars: BarContainer, fontsize: int = 12, color: str = "black", padding: int | float = 0) -> BarContainer:
        """
        This function adds text labels to the bars in a bar plot, displaying the actual height of each bar.

        Parameters:
        bars (BarContainer): The BarContainer object returned by the bar plot function.
        fontsize (int): The size of the text labels. Default is 12.
        color (str): The color of the text labels. Default is "black".
        padding (int | float): The padding between the bar and the text label. Default is 0.

        Returns:
        BarContainer: The same BarContainer object with added text labels.
        """
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, height + padding, f'{height}', ha='center', va='bottom', fontsize=fontsize, color=color)
        return bars
    def highlight_equal_values(bars: BarContainer, facecolor: str = "orange", edgecolor: str = "black", linewidth: int | float = 2, alpha: int | float = 1) -> BarContainer:
        """
        This function highlights bars with equal heights in a bar plot.

        Parameters:
        bars (BarContainer): The container of bars in the bar plot.
        facecolor (str): The color to fill the highlighted bars. Default is "orange".
        edgecolor (str): The color of the edges of the highlighted bars. Default is "black".
        linewidth (int | float): The width of the edges of the highlighted bars. Default is 2.
        alpha (int | float): The transparency of the highlighted bars. Default is 1.

        Returns:
        BarContainer: The modified container of bars with highlighted bars.
        """
        height_to_indices = {}
        for index, bar in enumerate(bars):
            height = bar.get_height()
            if height not in height_to_indices:
                height_to_indices[height] = []
            height_to_indices[height].append(index)
        indices_with_same_value = [indices for indices in height_to_indices.values() if len(indices) > 1]
        flat_indices_with_same_value = [index for sublist in indices_with_same_value for index in sublist]
        for i in flat_indices_with_same_value:
            bars[i].set_color(facecolor)
            bars[i].set_edgecolor(edgecolor)
            bars[i].set_linewidth(linewidth)
            bars[i].set_alpha(alpha)
        return bars
    def change_bar_colors(bars: BarContainer, facecolors: list[str]= ["yellow"], edgecolors: list[str] = ["black"], linewidth: int | float = 2, alpha: int | float = 1)-> BarContainer:
        """
        This function changes the colors of bars in a bar plot.

        Parameters:
        bars (BarContainer): The container of bars in the plot.
        facecolors (list[str]): A list of colors for the face of the bars. Default is ["yellow"].
        edgecolors (list[str]): A list of colors for the edges of the bars. Default is ["black"].
        linewidth (int | float): The width of the bar edges. Default is 2.
        alpha (int | float): The transparency of the bars. Default is 1.

        Returns:
        BarContainer: The modified container of bars with updated colors.
        """
        # Create cyclic iterators for facecolors and edgecolors
        facecolors_cycle = itertools.cycle(facecolors)
        edgecolors_cycle = itertools.cycle(edgecolors)

        # Iterate over each bar, facecolor, and edgecolor
        for bar, facecolor, edgecolor in zip(bars, facecolors_cycle, edgecolors_cycle):
            # Set the color, edgecolor, linewidth, and alpha of the bar
            bar.set_color(facecolor)
            bar.set_edgecolor(edgecolor)
            bar.set_linewidth(linewidth)
            bar.set_alpha(alpha)

        # Return the modified bars
        return bars
    def highlight_max_min_bar(bars: BarContainer, max_facecolor: str | tuple = 'green', max_edgecolor: str | tuple = 'black', max_linewidth: int | float = 2, min_facecolor: str | tuple = 'red', min_edgecolor: str | tuple = 'black', min_linewidth: int | float = 2, alpha: int | float = 1)-> BarContainer:
        """
        This function highlights the maximum and minimum bars in a bar plot.

        Parameters:
        bars (BarContainer): The container of bars in the bar plot.
        max_facecolor (str | tuple): The color of the maximum bar face. Default is 'green'.
        max_edgecolor (str | tuple): The color of the maximum bar edge. Default is 'black'.
        max_linewidth (int | float): The width of the maximum bar edge. Default is 2.
        min_facecolor (str | tuple): The color of the minimum bar face. Default is 'red'.
        min_edgecolor (str | tuple): The color of the minimum bar edge. Default is 'black'.
        min_linewidth (int | float): The width of the minimum bar edge. Default is 2.
        alpha (int | float): The transparency of the bars. Default is 1.

        Returns:
        BarContainer: The modified container of bars with highlighted maximum and minimum bars.
        """
        heights = [bar.get_height() for bar in bars]
        min_height = np.min(heights)
        max_height = np.max(heights)
        for bar in bars:
            if bar.get_height() == min_height:        
                bar.set_color(min_facecolor)
                bar.set_edgecolor(min_edgecolor)
                bar.set_linewidth(min_linewidth)
                bar.set_alpha(alpha)
            if bar.get_height() == max_height:
                bar.set_color(max_facecolor)
                bar.set_edgecolor(max_edgecolor)
                bar.set_linewidth(max_linewidth)
                bar.set_alpha(alpha)
        return bars
    def hightlight_median(bars: BarContainer, facecolor: str = "purple", edgecolor: str = "black", linewidth: int | float = 2, alpha: int | float = 1) -> BarContainer:
        """
        Highlights the median bar in a bar plot by changing its color, edge color, line width, and transparency.

        Parameters:
        bars (BarContainer): The container of bars in the bar plot.
        facecolor (str): The color of the median bar. Default is "purple".
        edgecolor (str): The color of the edge of the median bar. Default is "black".
        linewidth (int | float): The width of the line of the median bar. Default is 2.
        alpha (int | float): The transparency of the median bar. Default is 1.

        Returns:
        BarContainer: The modified container of bars with the highlighted median bar.
        """
        heights = [bar.get_height() for bar in bars]
        median_height = np.median(heights)
        median_index = np.argmin(np.abs(np.array(heights) - median_height))
        bars[median_index].set_color(facecolor)
        bars[median_index].set_edgecolor(edgecolor)
        bars[median_index].set_linewidth(linewidth)
        bars[median_index].set_alpha(alpha)
        return bars