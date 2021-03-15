from scipy.optimize import *
import numpy as np


def target_function(liquid_x, water_cut):
    return sum(liquid_x * water_cut)


def derivative_vector(_, water_cut):
    return water_cut


def simple_minimization_water(water_cut, my_linear_constraint):
    first_approach = np.ones(len(water_cut)) * 0.1
    # print(my_linear_constraint.get_report())
    linear_constraint = my_linear_constraint.to_scipy()
    sol = minimize(target_function, x0=first_approach, args=(water_cut,),
                   constraints=[linear_constraint],
                   method='SLSQP', jac=derivative_vector)
    return sol
