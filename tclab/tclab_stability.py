


import numpy as np
import matplotlib.pyplot as plt
from tclab_parameters import TCLabParameters
from control.matlab import *

#Define TCLabStability class to analyse the system by LGR and Bode 
class TCLabStability:

    def __init__(self, sys = None):
        self.sys = sys
        self.parameters = TCLabParameters()

    def system(self, sys):
        self.sys = sys

    def lgr(self, xlim=None, ylim=None):
        """ Plot the root locus of the given system. """
        if self.sys is not None:
            pass
        else:
            print("System not defined.")


    def get_gain(self):
        """ Request user to input the gain value using DCMotorParameters. """
        param_specs = [{"name": "K", "label": "Gain K", "default": 1.0}]
        parameters = self.parameters.get_parameters(param_specs)
        K = parameters['K']
        return K

    def closed_loop_response(self, K):
        """ Calculate the closed-loop response for a given gain K. """
        pass

    def display_responses(self, pv, mv):
        """ Display the process and control responses. """
        ty, y = pv
        tu, u = mv

        plt.figure(figsize=(10, 8))
        plt.subplot(2, 1, 1)
        plt.plot(ty, y, label='Process Variable (PV)')
        plt.title('Closed-loop Process Response')
        plt.xlabel('Time (s)')
        plt.ylabel('Output Response')
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(tu, u, label='Manipulated Variable (MV)')
        plt.title('Control Effort Response')
        plt.xlabel('Time (s)')
        plt.ylabel('Control Effort')
        plt.legend()

        plt.tight_layout()
        plt.show()

    def pzanalysis(self, plot=True, print_pz=True):
        """ Plot the poles and zeros of the system. """
        pass

    def bode(self, k, plot_b = True, plot_margin = True):
        """
        Bode plot of the closed loop system
        args:
            con: controller
            plot_b: boolean to plot the bode diagram
            plot_margin: boolean to plot the gain and phase margin

        returns:
            gm: gain margin
            pm: phase margin
            Wcg: crossover frequency (gain)
            Wcp: crossover frequency (phase)
        """
        #open loop
        if plot_b:
            plt.figure()

        # Program the Bode plot here
        pass

        if plot_b:
            plt.show()
        
        """
        if plot_margin:
            plt.figure()
            bode(cg)
            plt.subplot(211)
            plt.scatter(Wcg, -20*np.log10(gm), color ='r')
            plt.plot((Wcg, Wcg), (-20*np.log10(gm),0), '-r', linewidth=3 )
            plt.plot((Wcg, Wcg), (-20*np.log10(gm),min(20*np.log10(mag))), ':r' )
            plt.plot((omega[0],omega[-1]),(0,0),':r')
            plt.plot((Wcp, Wcp), (min(20*np.log10(mag)),0), ':r' )

            plt.subplot(212)
            plt.plot((Wcg, Wcg), (-180,20*np.log10(mag[0])), ':r' )
            plt.plot((omega[0],omega[-1]),(-180,-180),':r')
            plt.scatter(Wcp, -180+pm, color ='r')
            plt.plot((Wcp, Wcp), (-180+pm,-180), '-r',linewidth=3 )
            plt.plot((Wcp, Wcp), (-180+pm,max(phase)), ':r' )
            plt.show()

        return gm, pm, Wcg, Wcp
        """
    

if __name__ == "__main__":
    #Example Dicrete Transfer function
    Ts   =  28                   #Sampling time
    numz =  np.array([0.2339, 0.2024])   #Numerator
    denz =  np.array([1, -0.8145])        #Denominator
    d    =  1                   #Delay
    denzd = np.hstack((denz, np.zeros(d)))
    Gz   =  tf(numz, denzd, Ts)
    print(Gz)

    


