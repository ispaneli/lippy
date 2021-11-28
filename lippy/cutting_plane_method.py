from typing import List

import numpy as np

from .simplex_method import SimplexMethod
from ._log_modes import FULL_LOG, MEDIUM_LOG, LOG_OFF


class CuttingPlaneMethod:
    """
    In mathematical optimization, the cutting-plane method is any of a variety of optimization methods that
    iteratively refine a feasible set or objective function by means of linear inequalities, termed cuts.
    Such procedures are commonly used to find integer solutions to mixed integer linear programming (MILP) problems,
    as well as to solve general, not necessarily differentiable convex optimization problems.
    The use of cutting planes to solve MILP was introduced by Ralph E. Gomory.
    """
    def __init__(self, func_vec: List[int or float] or np.ndarray,
                 conditions_matrix: List[List[int or float]] or np.ndarray,
                 constraints_vec: List[int or float] or np.ndarray,
                 var_tag: str = "x", func_tag: str = "F", log_mode: int = LOG_OFF):
        """
        Initialization of an object of the "Cutting Plane method" class.

        :param func_vec: Coefficients of the equation.
        :param conditions_matrix: The left part of the restriction system.
        :param constraints_vec: The right part of the restriction system.
        :param var_tag: The name of the variables, default is "x".
        :param func_tag: The name of the function, default is "F".
        :param log_mode: So much information about the solution to write to the console.
        """
        self.c_vec = np.array(func_vec)
        self.a_matrix = np.array(conditions_matrix)
        self.b_vec = np.array(constraints_vec)

        self._num_of_vars = self.c_vec.shape[0]
        self.var_tag = var_tag
        self.func_tag = func_tag
        self.log_mode = log_mode

        self._simplex: SimplexMethod = NotImplemented

    def solve(self) -> (np.ndarray, np.float64):
        """
        Solve the integer problem of linear programming by the Cutting Plane method.

        :return: The solution and the value of the function.
        """
        self._simplex = SimplexMethod(self.c_vec, self.a_matrix, self.b_vec, var_tag=self.var_tag,
                                      func_tag=self.func_tag, log_mode=self.log_mode)
        start_table = np.copy(self._simplex.table.table)
        self._simplex.solve()

        while self._check_solution():
            table = self._simplex.table.table

            fractional_parts = np.modf(table[:-1, 0])[0]
            row_index = fractional_parts.argmax()

            coefficients = table[row_index]
            coefficients -= np.floor(coefficients)
            coefficients[0] *= -1

            new_equation = np.zeros(self.c_vec.shape[0] + 1)
            for i_1, x_i in enumerate(self._simplex.table.column_indices):
                if x_i >= self.c_vec.shape[0]:
                    for i_2, y_i in enumerate(np.arange(table.shape[0] - 1) + table.shape[1]):
                        if x_i == y_i:
                            for i_3 in range(new_equation.shape[0]):
                                new_equation[i_3] += coefficients[i_1] * start_table[i_2, i_3]
                            break
                else:
                    for column_index in range(self.c_vec.shape[0]):
                        if column_index == x_i:
                            new_equation[column_index] += coefficients[i_1]
                            break

            if self.log_mode in [FULL_LOG, MEDIUM_LOG]:
                var_tags = [f"{self.var_tag}{i + 1}" for i in range(self._num_of_vars)]
                equation = " + ".join([f"{c}*{v}" for c, v in zip(np.around(new_equation[1:], 3), var_tags)])
                print(f"New equation: {equation} <= {new_equation[0]}")

            self.a_matrix = np.vstack((self.a_matrix, new_equation[1:]))
            self.b_vec = np.append(self.b_vec, new_equation[0])

            self._simplex = SimplexMethod(self.c_vec, self.a_matrix, self.b_vec, var_tag=self.var_tag,
                                          func_tag=self.func_tag, log_mode=self.log_mode)
            start_table = np.copy(self._simplex.table.table)
            self._simplex.solve()

        if self.log_mode in [FULL_LOG, MEDIUM_LOG]:
            print("\nSolution of the integer problem of linear programming:")
            print(np.around(self._simplex.get_solution(), 3))
            print("The value of the function:")
            print(np.around(self._simplex.get_func_value(), 3), "\n")

        return self._simplex.get_solution(), self._simplex.get_func_value()

    def _check_solution(self) -> bool:
        """
        Checks the solution for integers.

        :return: True - solution is integer; False - is not.
        """
        solution = self._simplex.get_solution(self._num_of_vars)
        for value in solution:
            if round(value, 5) % 1 != 0:
                return True
        return False

    def get_solution(self) -> np.ndarray:
        """
        Return solution of problem of linear programming.

        :return: Solution of problem of linear programming
        """
        return self._simplex.get_solution()

    def get_func_value(self) -> np.float64:
        """
        Return the value of the function.

        :return: The value of the function.
        """
        return self._simplex.get_func_value()