import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from mdc_parameters import DCMotorParameters
import tkinter as tk



class DCMotorModel:
    def __init__(self, x0 = [0, 0], nl_params=None):
        """
        Constructor of the class
        args:
            nl_params: Non-linear model parameters for DC motor
        """
        pass

    
    #modify initial conditions
    def set_x0(self, x0):
        self.x0 = x0
        
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

    # Get the non-linear parameters for the DC motor
    """
    specific_params = [
        {"name": "J", "label": "J", "default": 0.00040},
        {"name": "B", "label": "B", "default": 0.0022},
        {"name": "Km", "label": "Km", "default": 0.2335},
        {"name": "Ka", "label": "Ka", "default": 0.2335},
        {"name": "R", "label": "R", "default": 3.4},
        {"name": "L", "label": "L", "default": 0.0015},
        {"name": "C", "label": "C", "default": 1e-4}
    ]
    mdc_params = DCMotorParameters()
    parameters_values = mdc_params.get_parameters(specific_params)
    """

    # Initial values
    x0 = [0, 0]  # Initial conditions: [initial angular velocity, initial current]

    