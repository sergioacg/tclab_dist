import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import time
import datetime
from tclab_class import InterfazTCLab
from tclab_model import TCLabModel
from tclab_ft import TCLabFT
from tclab_parameters import TCLabParameters
from tclab_stability import TCLabStability
from controllers import Controllers
from tools import *
import tkinter as tk
import threading
import pickle
import os


class TCLabGUI:
    
    
    def __init__(self, master):
        """
        Constructor de la clase TCLabGUI

        """
        
        font_size = 14
        font = ('Bookman Old Style', font_size)
        font_name = 'Bookman Old Style'

        # Interfaz variables
        self.connected = False # To know if the tclab is connected
        self.setpoint = None # Setpoint variable
        self.duration = None # Duration variable
        self.Gz = self.load_file('Gz')
        self.lin_params = self.load_file('lin_params')
        self.edo_params = self.load_file('edo_params')
        
        
        #================================================================================================
        #========  CREATE THE OBJECTS ==============================================================
        #================================================================================================
        self.tclab_model = TCLabModel()
        self.tclab_parameters = TCLabParameters()
        self.tclab_ft = TCLabFT()
        self.tclab_stability = TCLabStability()

        # Set the main window properties
        self.master = master
        self.master.title("TCLab Control Interface")
        self.master.geometry("+0+0") 

        #================================================================================================
        #========  CREATE MENU BAR FOR THE GUI     ======================================================
        #================================================================================================
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)
        self.modelbar = tk.Menu(self.menubar, tearoff=0)
        self.modelbar.add_command(label="View Transfer Function", command=self.view_tf)
        self.modelbar.add_command(label="View Parameters", command=self.view_parameters)
        self.modelbar.add_separator()
        self.modelbar.add_command(label="Exit", command=self.master.quit)

        self.menubar.add_cascade(label="Model", menu=self.modelbar)
        
        #================================================================================================
        #========  CREATE FRAMES CONNECT AND TEXT WIDGETS ======================================================
        #================================================================================================
        self.frame_controls = tk.Frame(self.master, width=50)  # Frame para los controles de la interfaz
        self.frame_controls.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)  # Ubicación del frame 
        self.frame_controls.config(bg="#f9fae3", bd = 5)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        #================================================================================================
        #========  CREATE FRAMES FOR OPTIONS LIKE STEP RESPONSE ======================================================
        #================================================================================================
        self.frame_options = tk.Frame(self.master, width=50)  # Frame para los controles de la interfaz
        self.frame_options.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.frame_options.config(bg="#f9fae3", bd = 5)
        self.master.columnconfigure(0, weight=1) # make the column expand
        self.master.rowconfigure(0, weight=1) # make the row expand

        #================================================================================================
        #========  CREATE FRAMES FOR RUN AND STOP BUTTONS ======================================================
        #================================================================================================
        self.frame_run = tk.Frame(self.master, width=50)  # Frame para los controles de la interfaz
        self.frame_run.grid(row=2, column=0, sticky='nsew', padx=1, pady=1)
        self.frame_run.config(bg="#f9fae3", bd = 5) # color frame_controls blue
        self.master.columnconfigure(0, weight=1) # make the column expand
        self.master.rowconfigure(0, weight=1) # make the row expand


        #================================================================================================
        #========  CREATE FRAMES FOR THE TERMINAL ======================================================
        #================================================================================================
        self.frame_terminal = tk.Frame(self.master, width=50) # Frame para los controles de la interfaz
        self.frame_terminal.grid(row=3, column=0, sticky='nsew', padx=5, pady=5) # Ubicación del frame 
        # color frame_controls blue
        self.frame_terminal.config(bg="black", bd = 4)
        # Hacer que la columna y la fila del frame se expandan
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        #================================================================================================
        #========  CREATE FRAMES FOR THE GRAPHS ======================================================
        #================================================================================================
        self.frame_graphs_pv = tk.Frame(self.master, width=480, height=400)
        self.frame_graphs_pv.grid(row=0, column=1,rowspan=4,  sticky="nsew", padx=2, pady=2)
        # color frame_controls blue
        self.frame_graphs_pv.config(bg="red", bd = 5)

        # Create upper graph for the Process Variable (PV)
        self.fig_pv = plt.Figure(figsize=(7, 6), dpi=100)
        self.ax_pv = self.fig_pv.add_subplot(211)
        self.ax_mv = self.fig_pv.add_subplot(212, sharex=self.ax_pv)  # Segunda subfigura comparte el eje x con la primera

        # Deactived the x label of the first graph
        self.ax_pv.tick_params(axis='x', labelbottom=False)

        # Add labels to the y axes and the x axis of the second graph
        self.ax_pv.set_ylabel('Temperature [C]')
        self.ax_mv.set_ylabel('Power [%]')
        self.ax_mv.set_xlabel('Time [s]')

        # Create the canvas and the toolbar for the graph
        self.canvas_pv = FigureCanvasTkAgg(self.fig_pv, self.frame_graphs_pv)
        self.toolbar_pv = NavigationToolbar2Tk(self.canvas_pv, self.frame_graphs_pv)
        self.toolbar_pv.update()
        self.canvas_pv.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        #================================================================================================
        #========  Create the connection buttons ======================================================
        #================================================================================================
        self.button_connect = tk.Button(self.frame_controls, width=10,
                                        text="Connect", font=font,
                                        command=self.connect)
        self.button_connect.grid(row=0, column=1, padx=5, pady=5)

        # DESCONNECT TO THE TCLAB
        self.button_disconnect = tk.Button(self.frame_controls, width=10,
                                           text="Desconnect", font=font, 
                                           command=self.disconnect)
        self.button_disconnect.grid(row=0, column=2, padx=5, pady=5)
        self.button_disconnect.config(state='disabled')  # Inicialmente, el botón Disconnect está deshabilitado

        #================================================================================================
        #========  SETPOINT AND DURATION ======================================================
        #================================================================================================
        bg_color = self.frame_controls.cget('bg')
        validation = (self.master.register(self.validate_numeric_input), '%P')
        self.label_sp = tk.Label(self.frame_controls, text="Setpoint",
                                  font=font, bg=bg_color, anchor='nw')
        self.label_sp.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.entry_setpoint = tk.Entry(self.frame_controls, font=font, width=10, 
                                       validate='key', validatecommand=validation)
        self.entry_setpoint.grid(row=2, column=1, padx=5, pady=5)
        self.label_sp_units = tk.Label(self.frame_controls, text="[°C]", 
                                       font=font, bg=bg_color, 
                                       anchor='nw')
        self.label_sp_units.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

        self.label_duration = tk.Label(self.frame_controls, text="Duration",
                                        font=font, bg=bg_color, anchor='nw')
        self.label_duration.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        

        #================================================================================================
        #========  DURATION ======================================================
        #================================================================================================
        self.entry_duration = tk.Entry(self.frame_controls, font=font, width=10, 
                                       validate='key', validatecommand=validation)
        self.entry_duration.grid(row=3, column=1, padx=5, pady=5)
        self.label_duration_units = tk.Label(self.frame_controls, text="[ s]",
                                                font=font, bg=bg_color, 
                                                anchor='nw')
        self.label_duration_units.grid(row=3, column=2, sticky="nsew", padx=5, pady=5)

        self.button_send = tk.Button(self.frame_controls, text="Send",
                                        command=self.send, width=10,
                                        font=(font_name, 16, "bold"), 
                                        bg="blue", fg="white", relief="raised")
        self.button_send.grid(row=4, column=2, padx=5, pady=5)

        #label para mostrar el setpoint y la duración enviadas al presionar el botón send
        self.label_sent = tk.Label(self.frame_controls, 
                                   text=f"Setpoint: {self.setpoint} [°C]\n Duration: {self.duration} [s]",
                                   font=font, bg=bg_color, justify='left')
        self.label_sent.grid(row=4, columnspan=2, column=0)

        #================================================================================================
        #========  SOLVE THE EDO OF TCLAB WITH SPECIFIED PARAMETERS ======================================================
        #================================================================================================
        #check button para resolver la edo del tclab con los parámetros especificados
        self.solve_edo = tk.BooleanVar()
        self.check_solve_edo = tk.Checkbutton(self.frame_options, text="Solve EDO",
                                                variable=self.solve_edo, 
                                                font=font, bg=bg_color, anchor='nw',
                                                command=self.tclab_edo_model)
        self.check_solve_edo.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

        #================================================================================================
        #========  CALCULATE THE SAMPLING TIME ======================================================
        #================================================================================================
        #check button para calcular el periodo de muestreo row 3, column 1
        self.calculate_sampling_time = tk.BooleanVar()
        self.check_calculate_sampling_time = tk.Checkbutton(self.frame_options, text="Calculate Ts",
                                                            variable=self.calculate_sampling_time, 
                                                            font=font, bg=bg_color, anchor='nw',
                                                            command=self.calculate_ts)
        self.check_calculate_sampling_time.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)
        # Entry read-only to show the sampling time next to the check button
        self.entry_sampling_time = tk.Entry(self.frame_options, font=font, width=5,
                                            validate='key', validatecommand=validation)
        self.entry_sampling_time.grid(row=3, column=2, padx=5, pady=5)
               

        #================================================================================================
        #========  COLECT DATA FOR INDENTIFYING THE SYSTEM ==============================================
        #================================================================================================
        self.collect_data = tk.BooleanVar()
        self.check_collect_data = tk.Checkbutton(self.frame_options, text="Collect Data",
                                                 variable=self.collect_data, 
                                                 command=self.toggle_test_type,
                                                 font=font, bg=bg_color, anchor='nw')
        self.check_collect_data.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

        # Radiobuttons para Step Test y PRBS Test
        self.test_type = tk.StringVar()
        self.radio_step = tk.Radiobutton(self.frame_options, text="Step Test",
                                         variable=self.test_type, value="step",
                                         font=font, bg=bg_color, anchor='nw')
        self.radio_step.grid(row=4, column=1, sticky="nsew", padx=5, pady=5)
        self.radio_prbs = tk.Radiobutton(self.frame_options, text="PRBS Test",
                                         variable=self.test_type, value="prbs",
                                         font=font, bg=bg_color, anchor='nw')
        self.radio_prbs.grid(row=4, column=2, sticky="nsew", padx=5, pady=5)

        # Ocultar inicialmente los Radiobuttons
        self.radio_step.grid_remove()
        self.radio_prbs.grid_remove()

        #================================================================================================
        #========  REGRESION       ====================================================================
        #================================================================================================
        self.regression = tk.BooleanVar()
        self.check_regression = tk.Checkbutton(self.frame_options, text="Regression",
                                                  variable=self.regression, 
                                                  command=self.toggle_regression,
                                                  font=font, bg=bg_color, anchor='nw')
        self.check_regression.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)

        #radio button to select regression in edo or in tf model
        self.regression_type = tk.IntVar(value=-1)
        self.radio_edo = tk.Radiobutton(self.frame_options, text="EDO",
                                         variable=self.regression_type, value="edo",
                                         font=font, bg=bg_color, anchor='nw',
                                         command=self.regression_model_edo)
        self.radio_edo.grid(row=5, column=1, sticky="nsew", padx=5, pady=5)
        self.radio_tf = tk.Radiobutton(self.frame_options, text="TF",
                                            variable=self.regression_type, value="tf",
                                            font=font, bg=bg_color, anchor='nw',
                                            command=self.regression_model_ft)
        self.radio_tf.grid(row=5, column=2, sticky="nsew", padx=5, pady=5)

        # Ocultar inicialmente los Radiobuttons
        self.radio_edo.grid_remove()
        self.radio_tf.grid_remove()
        
        #================================================================================================
        #========  STABILITY       ====================================================================
        #================================================================================================
        self.stability = tk.BooleanVar()
        self.check_stability = tk.Checkbutton(self.frame_options, text="Stability",
                                                    variable=self.stability, 
                                                    font=font, bg=bg_color, anchor='nw',
                                                    command=self.toggle_stability)
        self.check_stability.grid(row=6, column=0, sticky="nsew", padx=5, pady=5)

        #radio button to select stability analysys by LGR or Bode
        self.stability_type = tk.IntVar(value=-1)
        
        self.radio_pzmap = tk.Radiobutton(self.frame_options, text="PZMAP",
                                            variable=self.stability_type, value="pzmap",
                                            font=font, bg=bg_color, anchor='nw',
                                            command=self.stability_pzmap)
        self.radio_pzmap.grid(row=6, column=1, sticky="nsew", padx=5, pady=5)


        self.radio_lgr = tk.Radiobutton(self.frame_options, text="LGR",
                                            variable=self.stability_type, value="lgr",
                                            font=font, bg=bg_color, anchor='nw',
                                            command=self.stability_lgr)
        self.radio_lgr.grid(row=6, column=2, sticky="nsew", padx=5, pady=5)
        self.radio_bode = tk.Radiobutton(self.frame_options, text="Bode",
                                            variable=self.stability_type, value="bode",
                                            font=font, bg=bg_color, anchor='nw',
                                            command=self.stability_bode)
        self.radio_bode.grid(row=6, column=3, sticky="nsew", padx=5, pady=5)

        # Ocultar inicialmente los Radiobuttons
        self.radio_lgr.grid_remove()
        self.radio_bode.grid_remove()
        self.radio_pzmap.grid_remove()

        #================================================================================================
        #========  CONTROLLERS ==============================================================================
        #================================================================================================
        self.controller_active = tk.BooleanVar()
        self.check_controller_active = tk.Checkbutton(self.frame_options, text="Closed Loop",
                                                 variable=self.controller_active, 
                                                 command=self.toggle_test_type,
                                                 font=font, bg=bg_color, anchor='nw')
        self.check_controller_active.grid(row=7, column=0, sticky="nsew", padx=5, pady=5)

        #center de label 'Controllers'
        self.label_controllers = tk.Label(self.frame_options, text="Controllers",
                                            font=font, bg=bg_color, anchor='nw', justify='center')
        self.label_controllers.grid(row=7, columnspan=2, column=1)

        # pop up menu to select the tuning method
        self.pid_tuning_method = tk.StringVar()
        self.pid_tuning_menu = tk.OptionMenu(self.frame_options,
                                             self.pid_tuning_method, "Ziegler-Nichols",
                                             "cohen-coon", "IAE", "IAET")
        self.pid_tuning_menu.configure(font=font)
        self.pid_tuning_menu.grid(row=8, columnspan=3, column=0)

        #popup menu to select controller type P, PI, PID
        self.controller_type = tk.StringVar()
        self.controller_menu = tk.OptionMenu(self.frame_options,
                                                self.controller_type, "P", "PI", "PID")
        self.controller_menu.configure(font=font)
        self.controller_menu.grid(row=8, columnspan=3, column=2)

        #================================================================================================
        #========  RUN TEST ==============================================================================
        #================================================================================================
        # Botón verde para ejecutar el test
        self.button_execute = tk.Button(self.frame_run, text="Run",
                                        command=self.run, width=10,
                                        font=(font_name, 16, "bold"), 
                                        bg="green", fg="white", relief="raised")
        self.button_execute.grid(row=5, column=0, padx=1, pady=1)

        # Botón rojo para detener el test
        self.button_stop = tk.Button(self.frame_run, text="Stop",
                                     command=self.stop,  width=10,
                                     font=(font_name, 16, "bold"), 
                                     bg="red", fg="white", relief="raised")
        self.button_stop.grid(row=5, column=1, padx=1, pady=1)

        # Configurar las columnas para que se expandan
        self.frame_run.grid_columnconfigure(0, weight=1)
        self.frame_run.grid_columnconfigure(1, weight=1)

        
        #================================================================================================
        #========  TERMINAL ==============================================================================
        #================================================================================================
        self.text_terminal = tk.Text(self.frame_terminal, width=60, 
                                     height=13)
        #self.text_terminal.pack(side=tk.TOP, padx=1, pady=1)
        self.text_terminal.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.text_terminal.insert(tk.END, "TCLab Terminal\n")
        self.text_terminal.insert(tk.END, "----------------\n")
        
        
    def connect(self):
        """
        Connect to the TCLab hardware and start the control loop.

        """
        # Create an instance of the TCLab class
        self.tclab = InterfazTCLab()
        # bool para saber si el tclab esta conectado
        self.connected = True
        # Código para conectar a TCLab
        self.button_connect.config(state='disabled')  # Deshabilita el botón Connect
        self.button_disconnect.config(state='normal')  # Habilita el botón Disconnect


    def disconnect(self):
        """
        Disconnect from the TCLab hardware and stop the control loop.
        """
        # Close the connection to the TCLab
        self.tclab.disconnect()
        self.connected = False
        # Código para conectar a TCLab
        self.button_disconnect.config(state='disabled')  # Deshabilita el botón Disconnect
        self.button_connect.config(state='normal')  # Habilita el botón Connect

    def tclab_edo_model(self):
        """
        Solve the EDO of the TCLab with the specified parameters
        """
        try:
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
            opt_params = []
            default_parameters = {}
            # Check if setpoint and duration are provided
            if self.setpoint is not None and self.duration is not None:
                # Check if the Solve EDO checkbox is checked
                if self.solve_edo.get():
                    pass

                else:
                    #clear the graph
                    self.ax_pv.clear()
                    self.ax_mv.clear()
                    self.canvas_pv.draw()
            
            else:
                tk.messagebox.showerror("Error", "Please enter the setpoint and duration.")
                # uncheck the checkbox
                self.solve_edo.set(False)
        except:
            #unchecked the checkbox
            self.solve_edo.set(False)

    def calculate_ts(self):
        """
        Calculate the sampling time of the TCLab
        """
        try: 
            # Check if the Calculate Ts checkbox is checked
            if self.calculate_sampling_time.get():
                try:
                    if self.lin_params is None:
                        raise ValueError("Linear parameters not found.")
                    # Create the transfer function
                    K, tau, theta = self.lin_params
                    sys = tf([K], [tau, 1])
                    self.text_terminal.insert(tk.END, f"\n\nTransfer Function from Regresion:\n")
                except ValueError:
                    #Create transfer function
                    num, den = self.tclab_parameters.get_tf()
                    sys = tf(num, den)

                pass
        except:
            #unchecked the checkbox
            self.calculate_sampling_time.set(False)


    
    def toggle_test_type(self):
        """
        Show or hide the radio buttons for the test type based on the value of 
        the collect_data checkbutton.
        """
        if self.collect_data.get():
            self.radio_step.grid()
            self.radio_prbs.grid()
            # Seleccionar "Step Test" por defecto
            self.test_type.set("step")
            # Deactivate controller_active checkbox
            self.controller_active.set(False)
        elif self.controller_active.get():
            self.radio_step.grid_remove()
            self.radio_prbs.grid_remove()
            self.collect_data.set(False)
        else:
            self.radio_step.grid_remove()
            self.radio_prbs.grid_remove()

    def toggle_regression(self):
        """
        Show or hide the radio buttons for the regression type based on the value of 
        the regression checkbutton.
        """
        if self.regression.get():
            self.radio_edo.grid()
            self.radio_tf.grid()
            
        else:
            self.radio_edo.grid_remove()
            self.radio_tf.grid_remove()

    def validate_numeric_input(self, input):
        """
        Validate that the input is a float, an integer or an empty string in Entry widgets.
        """
        if input == "":
            return True
        else:
            try:
                float(input)
                return True
            except ValueError:
                return False


    def regression_model_edo(self):
        """
        Regression model of the TCLab
        """
        try:
            #print wait message for optimization calculation
            self.text_terminal.insert(tk.END, "Wait for the optimization calculation...\n")
            self.text_terminal.see(tk.END)

            pass
        except:
            #unchecked the checkbox
            self.regression.set(False)
            self.toggle_regression()

    def regression_model_ft(self):
        """
        Regression model of the TCLab
        """
        try:
            #print wait message for optimization calculation
            self.text_terminal.insert(tk.END, "Wait for the optimization calculation...\n")
            self.text_terminal.see(tk.END)

            pass

            # if entry_sampling_time is not empty calculate discrete transfer function
            if self.entry_sampling_time.get():
                Ts = int(self.entry_sampling_time.get())
                pass
        except:
            #unchecked the checkbox
            self.regression.set(False)
            self.toggle_regression()

    def display_tf(self, lin_params):
        """ Displays the transfer function and costs, checks for sampling time. """
        K, tau, theta = lin_params
        Gs = tf([K], [tau, 1])
        
        self.text_terminal.insert(tk.END, f'The transfer function:\n{Gs}\n')
        self.text_terminal.insert(tk.END, f'Transport delay: {theta}\n')
        self.text_terminal.see(tk.END)

        # Check if entry_sampling_time is not empty to calculate discrete transfer function
        Ts = self.entry_sampling_time.get()
        if Ts:
            Ts = float(Ts)
            self.Gz = self.tclab_ft.tfd(K, tau, theta, Ts)
            self.text_terminal.insert(tk.END, f'\nGz: {self.Gz}\n')
            self.text_terminal.see(tk.END)
            #save the discrete transfer function in a file in tclab folder
            self.save_file('Gz', self.Gz)
            self.save_file('lin_params', lin_params)

        else:
            # Show text in RED indicating that if the user put the Ts field
            # the discrete transfer function will be calculated
            self.text_terminal.tag_config("red", foreground="red")
            self.text_terminal.insert(tk.END, "If you want to calculate the discrete transfer function,\n", "red")
            self.text_terminal.insert(tk.END, "please input the sampling time Ts.\n", "red")
            self.text_terminal.see(tk.END)


    def save_file(self, key, value, name_file='parameters.pkl'):
        if os.path.exists(name_file):
            with open(name_file, 'rb') as file:
                parameters = pickle.load(file)
        else:
            parameters = {}

        parameters[key] = value

        with open(name_file, 'wb') as file:
            pickle.dump(parameters, file)

    def load_file(self, key, name_file='parameters.pkl'):
        if os.path.exists(name_file):
            with open(name_file, 'rb') as file:
                parameters = pickle.load(file)
                return parameters.get(key, None)
        return None

    def get_setpoint_duration(self):
        return self.setpoint, self.duration
                
    def run_test(self, test_type, test_params):
        """
        Run a test with the TCLab
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'data_{test_type}_{timestamp}.txt'
        if test_type == 'prbs':
            pass
        else:
            pass

    def run_closed_loop(self):
        """
        Run the TCLab in closed loop mode
        """
        try:
            self.tune_controller()
            #clear graph
            self.clear_graph()
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f'data_closed_loop_{timestamp}.txt'

            # Run the closed loop test
            pass

        except Exception as e:
            #show the exception message
            tk.messagebox.showerror("Error", e)
    
    def run(self):
        """
        Run mode for the TCLab
        """
        if not self.connected:
            tk.messagebox.showerror("Error", "Please connect to the TCLab before executing.")
        elif not self.collect_data.get() or not self.test_type.get():
            tk.messagebox.showerror("Error", "Please select an option before executing.")
        else:
            # Check if setpoint and duration are provided
            if self.setpoint is not None and self.duration is not None:
                if self.controller_active.get():
                    test_thread = threading.Thread(target=self.run_closed_loop)
                # Determine the test type and run the appropriate test
                elif self.test_type.get() == "step":
                    test_thread = threading.Thread(target=self.run_test, args=("step", {"step_test": self.setpoint}))
                elif self.test_type.get() == "prbs":
                    prbs_params = [
                        0,  # initial_value
                        5,  # amplitude
                        self.setpoint,  # offset
                        10,  # register_length
                        50,  # frequency_divider
                        self.duration,  # num_samples
                        30  # star_time
                    ]
                    test_thread = threading.Thread(target=self.run_test, args=("prbs", {"prbs_params": prbs_params}))
                else:
                    tk.messagebox.showerror("Error", "Invalid test type.")
                # Start the test thread
                test_thread.start()
            else:
                tk.messagebox.showerror("Error", "Please enter the setpoint and duration.") 
    
    def stop(self):
        pass

    def send(self):
        """
        Send the setpoint and duration to the TCLab
        """
        # Capture the setpoint and duration from the entry widgets
        setpoint_entry = self.entry_setpoint.get()
        duration_entry = self.entry_duration.get()

        if setpoint_entry:  # if setpoint_entry is not empty
            self.setpoint = float(setpoint_entry)
            self.entry_setpoint.delete(0, tk.END)  # Delete the contents of the entry

        if duration_entry:  # if duration_entry is not empty
            self.duration = float(duration_entry)
            self.entry_duration.delete(0, tk.END)  # Delete the contents of the entry

        # Update the label to show the values sent
        self.label_sent.config(text=f"Setpoint: {self.setpoint} [°C]\n Duration: {self.duration} [s]")


    def load_data(self):
        # ask for the user to load the data in a txt file using np.loadtxt
        filename = tk.filedialog.askopenfilename()
        if filename:
            data = np.loadtxt(filename, delimiter=',', skiprows=1)     
            return data
        else:
            return None

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


    def update_graph(self, time_data, temp_data, power_data, k, label=['Temperature', 'Heater Power'], color=['-r', '-b'], clear=True):
        """
        Update the graph with new data from the TCLab device and the control action. 
        """
        # Asegúrate de que los datos estén en el formato correcto, como listas o np.arrays
        if clear:
            self.ax_pv.clear()  # Limpia la gráfica actual de la variable controlada
        self.ax_pv.plot(time_data[:k], temp_data[:k], color[0], label=label[0])  # Dibuja la nueva gráfica de temperatura
        self.ax_pv.legend()  # Muestra la leyenda para la variable controlada

        if clear:
            self.ax_mv.clear()  # Limpia la gráfica actual de la acción de control
        self.ax_mv.plot(time_data[:k], power_data[:k], color[1], label=label[1])  # Dibuja la nueva gráfica de potencia del calentador
        self.ax_mv.legend()  # Muestra la leyenda para la acción de control

        self.ax_pv.set_ylabel('Temperature [C]')
        self.ax_mv.set_ylabel('Power [%]')
        self.ax_mv.set_xlabel('Time [s]')

        # Como ambos gráficos están en la misma figura, solo necesitas llamar a 'draw' una vez
        self.canvas_pv.draw()  # Actualiza el canvas

    def clear_graph(self):
        self.ax_pv.clear() 
        self.ax_mv.clear()

    def update_terminal(self, time_data, temp_data, power_data, k):
        # Asegúrate de que los datos sean arrays de NumPy o listas y tengan al menos un elemento
        if (isinstance(time_data, np.ndarray) or isinstance(time_data, list)) and len(time_data) > 0 and \
        (isinstance(temp_data, np.ndarray) or isinstance(temp_data, list)) and len(temp_data) > 0 and \
        (isinstance(power_data, np.ndarray) or isinstance(power_data, list)) and len(power_data) > 0:
            # Solo actualiza con el último valor de cada lista o array
            self.text_terminal.insert(tk.END, f"Time: {time_data[k]:6.1f} Temp: {temp_data[k]:6.2f} Power: {power_data[k]:6.2f}\n")
            self.text_terminal.see(tk.END)  # Autoscroll to the bottom
        else:
            print("Data provided to update_terminal is not in the correct format.")


    def update_data(self, time_data, temp_data, power_data, k):
        self.master.after(1, self.update_graph, time_data, temp_data, power_data, k)
        self.master.after(1, self.update_terminal, time_data, temp_data, power_data, k)

    def update_data_controller(self, time_data, temp_data, power_data, setpoint, k):
        self.master.after(1, self.update_graph, time_data, setpoint, power_data, k, ['Setpoint', 'Heater Power'], ['--r', '-k'], False)
        self.master.after(1, self.update_graph, time_data, temp_data, power_data, k, ['Temperature', 'Heater Power'], ['-k', '-k'], False)
        self.master.after(1, self.update_terminal, time_data, temp_data, power_data, k)


    def toggle_stability(self):
        """
        Show or hide the radio buttons for the stability type based on the value of 
        the stability checkbutton.
        """
        if self.stability.get():
            self.radio_lgr.grid()
            self.radio_bode.grid()
            self.radio_pzmap.grid()
            
        else:
            self.radio_lgr.grid_remove()
            self.radio_bode.grid_remove()
            self.radio_pzmap.grid_remove()

    def toggle_controller(self):
        """
        Show or hide the radio buttons for the controller type based on the value of 
        the controller checkbutton.
        """
        if self.controller.get():
            self.radio_p.grid()
            self.radio_pi.grid()
            self.radio_pid.grid()
            self.pid_tuning_menu.grid()
            
        else:
            self.radio_p.grid_remove()
            self.radio_pi.grid_remove()
            self.radio_pid.grid_remove()
            self.pid_tuning_menu.grid_remove()

    def view_tf(self):
        """
        View the transfer function of the TCLab
        """
        # Ask if self.lin_params exists
        try:
            #display the transfer function
            self.display_tf(self.lin_params)
            
        except:
            tk.messagebox.showerror("Error", "Please run the regression model first.")

    def view_parameters(self):
        """
        View the parameters of the TCLab
        """
        # Ask if self.edo_params exists
        try:
            #display the parameters
            if self.edo_params is None:
                raise Exception
            self.text_terminal.insert(tk.END, f'The parameters of the EDO model: {self.edo_params}\n')
            self.text_terminal.see(tk.END)
            
        except Exception as e:
            tk.messagebox.showerror("Error", "Please run the regression model first.")


    def stability_pzmap(self):
        """
        Stability analysis by pole-zero map
        """
        pass

    def stability_lgr(self):
        """
        Stability analysis by LGR
        """
        pass

    def stability_bode(self):
        """
        Stability analysis by Bode
        """
        pass

    def tune_controller(self):
        """
        Tune the controller based on the selected method and type.
        """
        # Check if setpoint and duration are provided
        if self.setpoint is not None and self.duration is not None:
            # Check if the tuning method is selected
            if self.pid_tuning_method.get():
                # Check if the control type is selected
                if self.controller_type.get():
                    # Check if the transfer function is defined
                    if hasattr(self, 'Gz') and self.Gz is not None:
                        # Check if the sampling time is defined
                        Ts = self.Gz.dt
                        if Ts:
                            Ts = float(Ts)
                            # Determine the tuning method and control type
                            tuning_method = self.pid_tuning_method.get()
                            control_type = self.controller_type.get()

                            # Get the parameters of the transfer function
                            K, tau, theta = self.lin_params

                            # Tune the controller
                            if tuning_method == "Ziegler-Nichols":
                                Kp, Ti, Td = Controllers.tune_ziegler_nichols(K, theta, tau, Ts, control_type=control_type)
                            elif tuning_method == "cohen-coon":
                                Kp, Ti, Td = Controllers.tune_cohen_coon(K, theta, tau, Ts, control_type=control_type)
                            elif tuning_method == "IAE":
                                Kp, Ti, Td = Controllers.tune_iae(K, theta, tau, Ts, control_type=control_type)
                            elif tuning_method == "IAET":
                                Kp, Ti, Td = Controllers.tune_iaet(K, theta, tau, Ts, control_type=control_type)
                            else:
                                tk.messagebox.showerror("Error", "Invalid tuning method.")
                                return
                            
                            init_controller_params = [
                            {"name": "Kp", "label": "Kp", "default": Kp},
                            {"name": "Ti", "label": "Ti", "default": Ti},
                            {"name": "Td", "label": "Td", "default": Td}
                            ]

                            # Ask the user for the controller parameters to implement
                            par = self.tclab_parameters.get_parameters(init_controller_params)

                            # Implement the controller
                            self.controller = Controllers(par['Kp'], par['Ti'], par['Td'], Ts)


                        else:
                            tk.messagebox.showerror("Error", "Please enter the sampling time Ts.")
                    else:
                        tk.messagebox.showerror("Error", "Please run the regression model first.")
                else:
                    tk.messagebox.showerror("Error", "Please select a controller type.")
            else:
                tk.messagebox.showerror("Error", "Please select a tuning method.")

#================================================================================
    
# Ejecución principal
if __name__ == "__main__":
    root = tk.Tk()
    app = TCLabGUI(root)
    root.mainloop()