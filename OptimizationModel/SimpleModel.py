from scipy.optimize import *
import numpy as np


def target_function(liquid_x, water_cut):
    return sum(liquid_x * water_cut)


def derivative_vector(_, water_cut):
    return water_cut


def minimization_water(water_cut, linear_constraint):
    first_approach = np.ones(len(water_cut)) * 0.1
    sol = minimize(target_function, x0=first_approach, args=(water_cut,),
                   constraints=[linear_constraint],
                   method='SLSQP', jac=derivative_vector)
    return sol
