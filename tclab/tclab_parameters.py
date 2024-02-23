import tkinter as tk
from tkinter import messagebox

class TCLabParameters:
    def __init__(self):
        self.font_size = 14
        self.font = ('Bookman Old Style', self.font_size)
        self.font_name = 'Bookman Old Style'
        

    def get_parameters(self, parameters):
        
        #Create a windows to insert the parameters pop up with default values
        root_edo = tk.Tk()
        root_edo .title("Enter the Parameters")
        vcmd = (root_edo.register(self.validate_numeric_input_par), '%P')

        #Create the labels and entries for the parameters with default values
        entries = {}
        for i, param in enumerate(parameters):
            tk.Label(root_edo, text=param['label'], font=self.font).grid(row=i, column=0)
            entry = tk.Entry(root_edo, validate="key", validatecommand=vcmd, font=self.font)
            entry.insert(0, str(param['default']))
            entry.grid(row=i, column=1)
            entries[param['name']] = entry

        #Create the button to accept the parameters and pass them to tclab_model.solve_nl in opt_params and parameters in default_parameters
        parameters_values = {}
        def on_accept():
        # Iterate through each parameter name and entry widget, capturing the value entered by the user.
            for name, entry in entries.items():
                try:
                    # Attempt to convert the entry to a float for numeric parameters
                    parameters_values[name] = float(entry.get())
                except ValueError:
                    # Handle cases where conversion to float fails, e.g., for non-numeric parameters or if the field is left blank
                    parameters_values[name] = entry.get()  # Store as string, or handle as appropriate for your application
            root_edo.destroy()  # Close the window after capturing the parameters

        #Create the button to accept the parameters and pass them to tclab_model.solve_nl in opt_params and parameters in default_parameters
        # Define and place the "Accept" button, linking it to the on_accept function
        accept_button = tk.Button(root_edo, text="Accept", command=on_accept, font=self.font)
        accept_button.grid(row=len(parameters), columnspan=2)
            
        
        #wait for user click the button accept and exit for the mainloop to continue 
        root_edo.wait_window(root_edo)
        return parameters_values
    
    def validate_numeric_input_par(self, input):
        """
        Validate that the input is a number (including floating point numbers) or an empty string in Entry widgets.
        """
        if input == "":
            return True  # Allow empty string
        try:
            float(input)  # Try to convert the string to float
            return True  # Return True if the string is a valid float
        except ValueError:
            return False  # Return False if the string cannot be converted to float

    def separate_parameters(self, parameters_values, optimization_params):
        """
        Separate the parameters in optimization parameters and default parameters
        """
        opt_params = []
        default_parameters = {}
        for name, value in parameters_values.items():
            if name in optimization_params:
                opt_params.append(value)  # Agrega el valor a la lista de parámetros de optimización
            else:
                default_parameters[name] = value  # Agrega el parámetro al diccionario de parámetros por defecto
        return opt_params, default_parameters
    

    def get_tf(self):
        """
        Ask the user for the numerator and denominator coefficients of a transfer function.
        Returns the coefficients as two separate lists.
        """
        root_tf = tk.Tk()
        root_tf.title("Transfer Function Coefficients")

        # Numerator
        tk.Label(root_tf, text="Numerator (comma-separated):", font=self.font).grid(row=0, column=0)
        numerator_entry = tk.Entry(root_tf,  font=self.font)
        numerator_entry.grid(row=0, column=1)

        # Denominator
        tk.Label(root_tf, text="Denominator (comma-separated):",  font=self.font).grid(row=1, column=0)
        denominator_entry = tk.Entry(root_tf,  font=self.font)
        denominator_entry.grid(row=1, column=1)

        def on_accept():
            try:
                # Convert the input strings to lists of floating-point numbers
                numerator = [float(coef.strip()) for coef in numerator_entry.get().split(',')]
                denominator = [float(coef.strip()) for coef in denominator_entry.get().split(',')]
                self.numerator = numerator
                self.denominator = denominator
                root_tf.destroy()
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter only numbers separated by commas.")
                self.numerator, self.denominator = [], []

        # Accept Button
        button_accept = tk.Button(root_tf, text="Accept", command=on_accept,  font=self.font)
        button_accept.grid(row=2, columnspan=2)

        root_tf.wait_window(root_tf)

        return self.numerator, self.denominator

# Usage of the method
if __name__ == "__main__":
    specific_params = [
        {"name": "U", "label": "U", "default": 10},
        {"name": "alpha", "label": "alpha", "default": 0.01},
        {"name": "m", "label": "m", "default": 0.004},
        {"name": "Cp", "label": "Cp", "default": 500},
        {"name": "A", "label": "A", "default": 0.0012},
        {"name": "eps", "label": "eps", "default": 0.9},
        {"name": "sigma", "label": "sigma", "default": 5.67e-8},
        {"name": "Ta", "label": "Ta", "default": 298}
    ]
    tclab_params = TCLabParameters()
    parameters_values = tclab_params.get_parameters(specific_params)
    #separate U and aplpha in opt_params and the rest of the parameters in default_parameters
    opt_params, default_parameters = tclab_params.separate_parameters(parameters_values, ['U', 'alpha'])

    print(f"Optimized Parameters: {opt_params}")
    print(f"Default Parameters: {default_parameters}")
    num, den = tclab_params.get_tf()
    print(f"Numerator: {num}")
    print(f"Denominator: {den}")