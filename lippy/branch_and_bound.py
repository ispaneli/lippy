from typing import List

import numpy as np

from .simplex_method import SimplexMethod
from ._log_modes import FULL_LOG, MEDIUM_LOG, LOG_OFF


class BranchAndBound:
    """
    Branch and bound is an algorithm design paradigm for discrete and combinatorial optimization problems,
    as well as mathematical optimization.
    A branch-and-bound algorithm consists of a systematic enumeration of candidate solutions by means of state
    space search: the set of candidate solutions is thought of as forming a rooted tree with the full set at the root.
    The algorithm explores branches of this tree, which represent subsets of the solution set.
    """
    def __init__(self, func_vec: List[int or float] or np.ndarray,
                 conditions_matrix: List[List[int or float]] or np.ndarray,
                 constraints_vec: List[int or float] or np.ndarray,
                 var_tag: str = "x", func_tag: str = "F", log_mode: int = LOG_OFF):
        """
        Initialization of an object of the "Branch and Bound" class.

        :param func_vec: Coefficients of the equation.
        :param conditions_matrix: The left part of the restriction system.
        :param constraints_vec: The right part of the restriction system.
        :param var_tag: The name of the variables, default is "x".
        :param func_tag: The name of the function, default is "F".
        :param log_mode: So much information about the solution to write to the console.
        """
        self.c_vec = np.array(func_vec, dtype=np.float64)
        self.a_matrix = np.array(conditions_matrix, dtype=np.float64)
        self.b_vec = np.array(constraints_vec, dtype=np.float64)
        self.num_of_vars = self.c_vec.shape[0]

        self.var_tag = var_tag
        self.func_tag = func_tag
        self.log_mode = log_mode

        self._final_values = list()
        self._solution = NotImplemented
        self._func_value = NotImplemented

    def solve(self) -> (np.ndarray, np.float64):
        """
        Solve the integer problem of linear programming by the Branch and bound method.

        :return: The solution and the value of the function.
        """
        self._node_iteration(self.c_vec, self.a_matrix, self.b_vec)

        func_results = [d['F'] for d in self._final_values]
        index_of_solution = func_results.index(max(func_results))
        self._solution = np.array([self._final_values[index_of_solution][i] for i in range(self.num_of_vars)])
        self._func_value = self._final_values[index_of_solution]['F']

        if self.log_mode in [FULL_LOG, MEDIUM_LOG]:
            print("\nSolution of the integer problem of linear programming:")
            print(np.around(self._solution, 3))
            print("The value of the function:")
            print(np.around(self._func_value, 3), "\n")

        return self._solution, self._func_value

    def _node_iteration(self, c_vec: np.ndarray, a_matrix: np.ndarray, b_vec: np.ndarray) -> None:
        """
        Performs calculations to the node, then starts branching left and right.

        :param c_vec: Coefficients of the equation.
        :param a_matrix: The left part of the restriction system.
        :param b_vec: The right part of the restriction system.
        :return: None.
        """
        simplex_method = SimplexMethod(c_vec, a_matrix, b_vec, var_tag=self.var_tag,
                                       func_tag=self.func_tag, log_mode=self.log_mode)
        simplex_method.solve()

        if not simplex_method.table.was_solved() and not simplex_method.table.has_optimal_solution():
            return

        is_integer_solution = True
        solution = simplex_method.get_solution(self.num_of_vars)
        for index, value in enumerate(solution):
            if round(value, 5) % 1 != 0:
                is_integer_solution = False

                new_a_row = np.zeros(self.c_vec.shape[0], dtype=np.float64)
                new_a_row[index] = 1
                a_matrix = np.vstack((a_matrix, new_a_row))

                b_vec = np.append(b_vec, int(value))
                if int(value) >= 0:
                    if self.log_mode in [FULL_LOG, MEDIUM_LOG]:
                        print(f"\nNew branch: x{index + 1} <= {int(value)}")
                    self._node_iteration(c_vec, a_matrix, b_vec)

                a_matrix[-1, index] = -1
                b_vec[-1] = -b_vec[-1] - 1

                if self.log_mode in [FULL_LOG, MEDIUM_LOG]:
                    print(f"New branch: x{index + 1} >= {int(value) + 1}")
                self._node_iteration(c_vec, a_matrix, b_vec)

        if is_integer_solution:
            values = {i: np.rint(v) for i, v in enumerate(solution)}
            values['F'] = simplex_method.get_func_value()
            self._final_values.append(values)

    def get_solution(self) -> np.ndarray:
        """
        Return solution of problem of linear programming.

        :return: Solution of problem of linear programming
        """
        return self._solution

    def get_func_value(self) -> np.float64:
        """
        Return the value of the function.

        :return: The value of the function.
        """
        return self._func_value
