import sys
import time
import datetime
import tclab_cae.tclab_cae as tclab
import numpy as np
import matplotlib.pyplot as plt
from tclab_plotter import TCLabPlotter
from controllers import Controllers
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

    def closed_loop(self, setpoint, duration, controller, filename='closed_loop_data.txt',update_data_callback=None):
        nit = int(duration)  # Total number of iterations
        ts_samples = int(controller.Ts)  # Sampling period in seconds (assuming Ts is an integer)

        # Initialize arrays to store time, control actions, system outputs, errors, and setpoints
        t = np.zeros(nit)
        u = np.zeros(nit)
        y = np.ones(nit) * self.lab.T1
        e = np.zeros(nit)
        r = np.zeros(nit)

        # Initialize arrays to store measured time and temperature
        tm = np.zeros(nit)

        start_time = time.time()  # Record the start time

        # Set up plotting if no update data callback is provided
        if update_data_callback is None:
            plt.ion()  # Enable interactive mode for live plotting
            plotter = TCLabPlotter()  # Create an instance of the plotter
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)  # Create subplots for controlled and manipulated variables

        try:
            for k in range(1, nit):
                current_time = time.time()  # Get the current time
                tm[k] = current_time - start_time  # Calculate elapsed time
                r[k] = setpoint  # You can update the setpoint in real-time here if desired
                y[k] = self.lab.T1  # Read the current temperature
                e[k] = r[k] - y[k]  # Calculate the control error

                # Calculate the control action every Ts
                if k % ts_samples == 0:
                    pass
                else:
                    pass
                
                # Update the graph every second
                if k % 1 == 0:
                    if update_data_callback:
                        update_data_callback(tm, y, u, r, k)  # Update data if callback is provided
                    else:
                        # Print current values to the terminal
                        print(f'{tm[k]:6.1f} {u[k]:6.2f} {y[k]:6.2f}')
                        # Clear the previous plots
                        ax1.clear()
                        ax2.clear()
                        # Plot the controlled and manipulated variables
                        plotter.plot_control(tm[:k + 1], y[:k + 1], u[:k + 1], r[:k + 1], ax1=ax1, ax2=ax2)
                        plt.pause(0.01)  # Pause to allow the plot to update

                # Calculate the sleep time to maintain a consistent loop period
                sleep_time = start_time + k - time.time()
                if sleep_time > 0:
                    time.sleep(sleep_time)

                # Break the loop if stop is requested
                if self.stop_requested:
                    break

            self.lab.Q1(0)  # Turn off the heater after completing the loop
            print("Closed-loop control completed.")
            
            # Save the data if no update data callback is provided
            if update_data_callback is None:
                self.save_txt(tm, u, y, 'closed_loop_data.txt')
                input("Press Enter to Finish")
            else:
                root = tk.Tk()  # Create a Tkinter root widget
                root.withdraw()  # Hide the root window
                if messagebox.askyesno("Save data", "Do you want to save the data?"):
                    file = filedialog.asksaveasfile(mode='w', defaultextension=".txt", initialfile=filename)
                    if file is not None:
                        self.save_txt(tm, u, y, file.name)
                        file.close()
                root.destroy()

        except KeyboardInterrupt:
            print("Closed-loop control interrupted by user.")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            self.lab.Q1(0)  # Ensure the heater is turned off in case of interruption
            if update_data_callback is None:
                self.disconnect()  # Disconnect from the device if no update data callback is provided


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
