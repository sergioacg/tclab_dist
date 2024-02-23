import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
#from tclab_class import InterfazTCLab
#from tclab_plotter import TCLabPlotter
from tclab_parameters import TCLabParameters
import tkinter as tk

# Define the TCLabModel class to define the non linear model of the plant

class TCLabModel:
    # Constructor of the class with the parameters list of the non-linear and linear model 
    def __init__(self, data = None, x0 = 293, nl_params = None):
        """
        Constructor of the class
        args:
            interfaz: TCLab interface
            nl_params: Non linear model parameters
            lin_params: Linear model parameters
            data: data from the TCLab [t, Q, T]
        """
        self.x0 = x0 # Initial temperature
        self.data = data

        # Default non linear parameter values
        default_parameters = {
            'm': 4.0/1000.0,
            'Cp': 0.5 * 1000.0,
            'A': 12.0 / 100.0**2,
            'eps': 0.9,
            'sigma': 5.67e-8,
            'Ta': 298
        }
        # Override default parameters if custom parameters are provided
        if nl_params is not None:
            self.nl_params = nl_params
        else:
            self.nl_params = default_parameters


    
    def update_data(self, data):
        self.data = data

    def load_data(self):
        # ask for the user to load the data in a txt file using np.loadtxt
        filename = tk.filedialog.askopenfilename()
        if filename:
            data = np.loadtxt(filename, delimiter=',', skiprows=1)     
            return data
        else:
            return None

if __name__ == "__main__":

    pass
