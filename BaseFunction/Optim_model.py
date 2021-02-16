import numpy as np
from scipy.optimize import minimize


class Approximation:
    @staticmethod
    def x_function(coefficient: np.array, x: np.array) -> np.array:
        print(coefficient, x)
        return coefficient[0] * x

    @staticmethod
    def x2_function(coefficient: np.array, x: np.array) -> np.array:
        print(coefficient, x)
        return coefficient[0] * x ** 2 + coefficient[1] * x

    @staticmethod
    def x3_function(coefficient: np.array, x: np.array) -> np.array:
        f = coefficient[0] * x ** 3
        s = coefficient[1] * x ** 2
        t = coefficient[2] * x
        return f + s + t

    @staticmethod
    def x4_function(coefficient: np.array, x: np.array) -> np.array:
        f = coefficient[0] * x ** 4
        s = coefficient[1] * x ** 3
        t = coefficient[2] * x ** 2
        fo = coefficient[3] * x
        return f + s + t + fo

    @staticmethod
    def deviation(y_experienced: np.array, y_calculated: np.array) -> np.array:
        return sum((y_calculated - y_experienced)**2)

    def function_deviation(self, coefficient: np.array,
                           fun: callable,
                           x_experienced: np.array,
                           y_experienced: np.array) -> np.array:
        y_calculated = fun(coefficient, x_experienced)
        return self.deviation(y_experienced, y_calculated)

    def determine_coefficients(self, fun: callable,
                               first_approach: np.array,
                               x_experienced: np.array,
                               y_experienced: np.array):
        res = minimize(self.function_deviation, first_approach,
                       args=(fun, x_experienced, y_experienced))
        return res

