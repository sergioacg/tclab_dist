import numpy as np

class Controllers:
    def __init__(self, Kp, Ti=None, Td=None, Ts=1.0):
        self.Kp = Kp
        self.Ti = Ti
        self.Td = Td
        self.Ts = Ts

        pass

        self.u_prev1 = 0 #u[k-1]
        self.e_prev1 = 0 #e[k-1]
        self.e_prev2 = 0 #e[k-2]

    def calculate(self, setpoint, pv):
        pass

    @staticmethod
    def tune_ziegler_nichols(K, theta, tau, Ts, control_type='PI'):
        theta_corrected = theta + Ts / 2  # Correct the delay for discrete control
        if control_type == 'P':
            Kp = tau / (K * theta_corrected)  # Proportional control (P) for Ziegler-Nichols
            Ti = float('inf')
            Td = 0
        elif control_type == 'PI':
            Kp = (0.9 * tau) / (K * theta_corrected)
            Ti = theta_corrected / 0.3
            Td = 0
        elif control_type == 'PID':
            Kp = (1.2 * tau) / (K * theta_corrected)
            Ti = 2 * theta_corrected
            Td = 0.5 * theta_corrected
        return Kp, Ti, Td

    @staticmethod
    def tune_cohen_coon(K, theta, tau, Ts, control_type='PI'):
        pass

    @staticmethod
    def tune_iae(K, theta, tau, Ts, control_type='PI'):
        pass

    @staticmethod
    def tune_iaet(K, theta, tau, Ts, control_type='PI'):
        pass
