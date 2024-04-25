

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from scipy.interpolate import interp1d
from control.matlab import *
from math import pi
from scipy.interpolate import interp1d


# Define the TCLabFT class to define the transfer function continiuous and discrete model of the plant
class TCLabFT:

    def __init__(self, data = None, x0 = 25, lin_params = None):
        """
        Constructor of the class
        args:
            interfaz: TCLab interface
            data: data from the TCLab [t, Q, T]
            x0: Initial temperature
            lin_params: Linear model parameters
        """
        self.x0 = x0
        self.lin_params = lin_params
        self.data = data

    def update_data(self, data):
        self.data = data

    def update_x0(self, x0):
        self.x0 = x0

    def update_lin_params(self, lin_params):
        self.lin_params = lin_params

    
    
if __name__ == "__main__":
    pass

    