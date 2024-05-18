import matplotlib.pyplot as plt
import numpy as np

class TCLabPlotter:
    """
    A class dedicated to plotting results for the Temperature Control Lab (TCLab).
    This includes plotting controlled variables, manipulated variables, setpoints, 
    and potentially comparing these to reference values or simulations.
    """

    # Plot a single variable over time.
    def plot_sv(self, time, variable, title='Process Variable', y_label='Temperature', x_label='Time [s]'):
        """
        Plot a single variable over time.
        
        Parameters:
            time (list or ndarray): Time data points.
            variable (list or ndarray): Data points of the variable to be plotted.
            title (str): The title of the plot.
            y_label (str): The label for the Y-axis.
            x_label (str): The label for the X-axis.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(time, variable, label=y_label, linewidth=2)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True)
        plt.legend()
        plt.show()

    # Plot multiple variables over time.
    def plot_mv(self, time, variables, labels, ax=None, title='Process Variables', y_label='Temperature', x_label='Time [s]'):
        """
        Plot multiple variables over time on given axes.
        
        Parameters:
            time (list or ndarray): Time data points.
            variables (list of ndarrays): Data points of the variables to be plotted.
            labels (list of str): Labels for the variables.
            ax (matplotlib.axes.Axes): Axes object to plot on. If None, creates new figure and axes.
            title (str): Title of the plot.
            y_label (str): Label for the Y-axis.
            x_label (str): Label for the X-axis.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))

        for i, variable in enumerate(variables):
            ax.plot(time, variable, label=labels[i], linewidth=2)

        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.grid(True)
        ax.legend()

    # Plot controlled and manipulated variables
    def plot_control(self, time, controlled, manipulated, setpoint, ax1=None, ax2=None, title='Control and Manipulation', controlled_label='Temperature [C]', manipulated_label='Power [%]'):
        """
        Plot the controlled variable with setpoint and the manipulated variable in two subplots
        with shared x-axis (time).
        
        Parameters:
        time (list or ndarray): Time data points.
        controlled (list or ndarray): Data points for the controlled variable (e.g., temperature).
        manipulated (list or ndarray): Data points for the manipulated variable (e.g., heater power).
        setpoint (list or ndarray): Setpoint data points for the controlled variable.
        title (str): The title of the plot.
        controlled_label (str): The label for the controlled variable plot.
            manipulated_label (str): The label for the manipulated variable plot.
        """
        if ax1 is None or ax2 is None:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12), sharex=True)  # Create two vertical subplots with shared x-axis

        # First subplot for the controlled variable and setpoint
        ax1.plot(time, controlled, 'b-', label=controlled_label)
        ax1.plot(time, setpoint, 'r--', label='Setpoint')
        ax1.set_title(title)
        ax1.set_ylabel(controlled_label)
        ax1.legend()
        ax1.grid(True)

        # Second subplot for the manipulated variable
        ax2.plot(time, manipulated, 'g-', label=manipulated_label)
        ax2.set_xlabel('Time [s]')
        ax2.set_ylabel(manipulated_label)
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()  # Adjust layout to not overlap
        plt.show()


# Example of usage
if __name__ == "__main__":

    # Datos de ejemplo
    time_data = np.linspace(0, 600, 600)  # Tiempo de 0 a 600 segundos
    temp_data = np.random.normal(50, 5, 600)  # Datos de temperatura simulados
    power_data = np.random.normal(30, 10, 600)  # Datos de potencia del calentador simulados
    temp_setpoint = np.linspace(50, 55, 600)  # Setpoint de temperatura incrementando linealmente

    # Crear una instancia de TCLabPlotter
    plotter = TCLabPlotter()

    # Usar el método para graficar los datos
    plotter.plot_control(time_data, temp_data, power_data, temp_setpoint, 
                         title='TCLab Control and Power', controlled_label='Temperature [C]',
                           manipulated_label='Heater Power [%]')
    plotter.plot_sv(time_data, temp_data, title='Temperature Over Time', y_label='Temperature [C]')
