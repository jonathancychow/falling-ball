import logging
import math

import numpy as np
from scipy.integrate import solve_ivp

from ball.model.etl.utils import interpolate

logger = logging.getLogger()


class Simulation:
    """
    Implementation of an ODE based on Newtons second law. Given power and distance, solve for velocity and time.

    Newtons second law
    dvdt = a = F/m
    dsdt = v

    ODE to solve for velocity and time
    dvds = dvdt * dtds
    dtds = 1 / dsdt

    """

    def __init__(self, ball, environment):
        self._ball = ball
        self._environment = environment

    def velocity_and_time_ode(self, s, x):
        v = x[0]
      
        f_weight = self._ball.mass * self._environment.gravity
        f_drag = self._ball.cda * self._environment.air_density * math.pi * (self._ball.radius**2) * (v **2)
        g_vert = 1 / self._ball.mass * ( f_weight - f_drag )  

        dvds = g_vert / v
        dtds = 1 / v
        return np.array([dvds, dtds])

    def solve_velocity_and_time(self, s, v0, t0):
        sol = solve_ivp(self.velocity_and_time_ode, 
                        t_span=(s[0], s[-1]), 
                        y0=np.array([v0, t0]), 
                        max_step=100
                        )
                        
        sim_v = interpolate(sol.t, sol.y[0, :], s)
        sim_t = interpolate(sol.t, sol.y[1, :], s)
        return sim_v, sim_t
