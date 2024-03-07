import sys
import time
import datetime
import tclab_cae.tclab_cae as tclab
import numpy as np
import matplotlib.pyplot as plt
from tclab_plotter import TCLabPlotter
from tools import *
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Define the TCLAB_CAE class to comunicate with the real device
class InterfazTCLab:
    # Constructor of the class
    def __init__(self):
        """Connect to the TCLab device"""
        pass


    # Method to disconnect from the device
    def disconnect(self):
        """Disconnect from the TCLab device"""
        pass

    # Method to test the Temperature Control Lab
    def test(self, power, duration):
        """
        Test the TCLab device in only one Heater (SISO system)
            power: percentage of the heater power
            duration: time in seconds to turn on the heater
        """
        pass



    def open_loop_response(self, test_type='step', filename='data.txt', duration=None, step_test=None, prbs_params=None, update_data_callback=None, stop=False):
        """
        Open loop response of the Temperature Control Lab
        args:
            test_type: 'step' or 'prbs'
            filename: name of the file to save the data
            duration: time in seconds of the test
            step_test: value of the step test
            prbs_params: parameters of the PRBS test
            update_data_callback: callback function to update the data in a GUI
            stop: flag to stop the test
        """
        tm, T1, Q1 = [], [], []
        
        if test_type == 'step':
            if duration is None or step_test is None:
                raise ValueError("For step test, 'duration' and 'setpoint' must be provided.")
            Q1 = np.zeros(duration + 1)
            Q1[10:] = step_test  # Step after 10 seconds
        elif test_type == 'prbs':
            if prbs_params is None:
                raise ValueError("For PRBS test, 'prbs_params' must be provided.")
            Q1 = SignalGenerator.create_prbs(*prbs_params)
            duration = len(Q1) - 1
        else:
            raise ValueError("Invalid 'test_type' provided. Use 'step' or 'prbs'.")


        # Create the time and temperature arrays
        pass

        # Create a plotter object if no callback is provided
        if update_data_callback == None:
            pass
        
        # Loop to control the TCLab
        try:
            for k in range(1, duration + 1):
                # Calculate the time for the next iteration
                pass
                
                 # update current time and record time and temperature
                pass

                # Llama al callback con los nuevos datos
                # si es ejecutado por la interfaz gráfica
                if update_data_callback:
                    pass
                else:
                    # Print line of data to terminal
                    pass

                if update_data_callback == None:
                    # Plot the data
                    pass

                # Calculate sleep time and record time and temperature 
                pass

                # Check if the user requested to stop the test
                if self.stop_requested:
                    break

                
            # Save the data to a text file
            self.lab.Q1(0)  # turn off the heater
            print("Test completed.")
            if update_data_callback == None:
                # Save the data to a text file
                self.save_txt(tm, Q1, T1, filename)
                input("Press Enter to Finish")
            else:
                #preguntar si desea guardar los datos con mensaje emergente tkinter
                root = tk.Tk()
                root.withdraw()
                if messagebox.askyesno("Save data", "Do you want to save the data?"):
                    file = filedialog.asksaveasfile(mode='w',
                                                     defaultextension=".txt", 
                                                     initialfile=filename)
                    if file is not None:
                        self.save_txt(tm, Q1, T1, file.name)
                        file.close()
                root.destroy()


        except KeyboardInterrupt:
            print("Test interrupted by user.")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            self.lab.Q1(0)  # Asegura que el heater se apague al finalizar.
            if update_data_callback == None:
                self.disconnect()

    @staticmethod
    def save_txt(t, u1, y1, filename='tclab_step.txt'):
        """
        save the TCLAB data in a text file
        args:
            t: time
            u1: heater power
            y1: temperature
            filename: name of the file
        """
        data = np.vstack((t,u1,y1)).T
        top = 'Time (sec), Heater 1 (%), Temperature 1 (degC)'
        np.savetxt(filename, data, delimiter=',', header=top, comments='')


        

# Define the class to control the Temperature Control Lab
if __name__ == "__main__":
    pass
