# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 00:11:27 2023

@author: Sergio
"""

import matplotlib.pyplot as plt
from control.matlab import *
import numpy as np
from math import pi

def margin_plot(sys):
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
    mag, phase, omega = bode(sys)
    gm, pm, Wcg, Wcp = margin(sys)
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
    return gm, pm, Wcg, Wcp

class DataSaver:
    @staticmethod
    def save_txt(t, u1, y1, filename='data.txt'):
        data = np.vstack((t,u1,y1)).T
        top = 'Time (sec), Heater 1 (%), Temperature 1 (degC)'
        np.savetxt(filename, data, delimiter=',', header=top, comments='')


class SamplingTime:
    
    @staticmethod
    def calculate(sys):
        h = feedback(sys, 1)
        mag, phase, w = bode(sys,plot=False)
        
        mWc = 0.707 
        index_wc = np.where(mag >=  mWc)
        wc = w[index_wc[0][-1]]
        wmin = 8 * wc
        wmax = 12 * wc
        ts_small = 2*pi / (wmax)
        ts_big = 2*pi / (wmin)
        return (ts_small + ts_big)/2, ts_small, ts_big
   
    

class SignalGenerator:
    @staticmethod
    def create_prbs(initial_value, amplitude, offset, register_length, frequency_divider, num_samples, start_time):
        """
        Generates a Pseudo Random Binary Sequence (PRBS) for system identification experiments.

        Parameters:
            initial_value (float): Constant initial value before the PRBS sequence starts.
            amplitude (float): Amplitude of the signal changes (difference between high and low values).
            offset (float): DC level or base value on which the amplitude is applied.
            register_length (int): Length of the shift register used to generate the sequence. Affects the sequence period.
            frequency_divider (int): Frequency divider. Controls the duration of each bit in the sequence.
            num_samples (int): Total number of samples in the generated sequence from start time.
            start_time (int): Time of application or delay before the PRBS sequence starts.
                
            

                             ____  ofsset + amplitude          __________      ____
                            |    |                            |          |    |
            offset         -|----|--------                    |          |    |
                            |    |____________________________|          |____|
                            |
                            |
  initial_value ____________|
                                                              |--------->|
            |-start_time -->|                      register_length * frequency_divider 
                

                |---------- num_samples ------------------------------------------->|
                                
            
            "Exit parameter" is  :
            prbs : prbs sequence created by PRBS algo

        """
        k1 = register_length - 1
        k2 = register_length
        if register_length == 5:
            k1 = 3
        elif register_length == 7: 
            k1 = 4
        elif register_length == 9:   
            k1 = 5
        elif register_length == 10: 
            k1 = 7
        elif register_length == 11: 
            k1 = 9    
        
        sbpa = [1]*11
        prbs = [0] * (num_samples + start_time)*2
        
        for i in range(start_time):
           prbs[i] = initial_value;
        
        i = start_time + 1
        while i <= num_samples:
            uiu = -sbpa[k1]*sbpa[k2]
            if register_length == 7:
                uiu = -sbpa[1]*sbpa[2]*sbpa[4]*sbpa[7]
            
            j = 0
            while j <= frequency_divider:
                prbs[i] = uiu * amplitude + offset
                i += 1
                j += 1
            
            for j in range(register_length, 0 , -1):
                sbpa[j] = sbpa[j - 1]
            
            sbpa[0] = uiu;
        
        # Copy the prbs sequence to a new array from 0 to num_samples avoiding the zeros at the end side effects
        prbs = prbs[:num_samples]

        #Convert the last 4 values to initial value
        for i in range(1,5):
            prbs[-i] = initial_value

        return prbs