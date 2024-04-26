


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

    def margin_plot(self):
        """margin_plot(sysdata)

        Calculate gain and phase margins and associated crossover frequencies
        and plot the gain margin and phase margin marked with solid vertical lines. 
        The dashed vertical lines indicate the locations of Wcg, the frequency where the gain margin is measured, 
        and Wcp, the frequency where the phase margin is measured.

        Parameters
        ----------
        sysdata : LTI system or (mag, phase, omega) sequence
            sys : StateSpace or TransferFunction
                Linear SISO system representing the loop transfer function
            mag, phase, omega : sequence of array_like
                Input magnitude, phase (in deg.), and frequencies (rad/sec) from
                bode frequency response data

        Returns
        -------
        gm : float
            Gain margin
        pm : float
            Phase margin (in degrees)
        wcg : float or array_like
            Crossover frequency associated with gain margin (phase crossover
            frequency), where phase crosses below -180 degrees.
        wcp : float or array_like
            Crossover frequency associated with phase margin (gain crossover
            frequency), where gain crosses below 1.

        Margins are calculated for a SISO open-loop system.

        If there is more than one gain crossover, the one at the smallest margin
        (deviation from gain = 1), in absolute sense, is returned. Likewise the
        smallest phase margin (in absolute sense) is returned.

        Examples
        --------
        >>> sys = tf(1, [1, 2, 1, 0])
        >>> gm, pm, wcg, wcp = margin_plot(sys)
        
        by: Sergio Andres Castaño Giraldo
        """
        plt.figure()
        mag, phase, omega = bode(self.sys)
        gm, pm, Wcg, Wcp = margin(self.sys)
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
    
    def bode(self, con, plot_b = True, plot_h = True):
        """
        Bode plot of the closed loop system
        args:
            con: controller
            plot_b: boolean to plot the bode diagram
            plot_h: boolean to plot the closed loop system

        returns:
            gm: gain margin
            pm: phase margin
            Wcg: crossover frequency (gain)
            Wcp: crossover frequency (phase)
        """
        pass
    

if __name__ == "__main__":
    #Example Dicrete Transfer function
    Ts   =  28                   #Sampling time
    numz =  np.array([0.2339, 0.2024])   #Numerator
    denz =  np.array([1, -0.8145])        #Denominator
    d    =  1                   #Delay
    denzd = np.hstack((denz, np.zeros(d)))
    Gz   =  tf(numz, denzd, Ts)
    print(Gz)

    


