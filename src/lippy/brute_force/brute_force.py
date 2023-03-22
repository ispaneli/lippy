import itertools
import numpy as np
import prettytable

from ..simplex import SimplexMethod
from ..enums import LogMode
from ..types import Vector, Matrix


class BruteForce:
    """
    In computer science, brute-force search or exhaustive search,
    also known as generate and test, is a very general problem-solving
    technique and algorithmic paradigm that consists of systematically
    enumerating all possible candidates for the solution and checking
    whether each candidate satisfies the problem's statement.

    It's used to solve integer linear programming problems.
    """
    def __init__(
        self,
        func_vec: Vector,
        conditions_matrix: Matrix,
        constraints_vec: Vector,
        var_tag: str = 'x',
        func_tag: str = 'F',
        log_mode: int = LogMode.LOG_OFF
    ):
        """
        Initialization of an object of the "Brute Force" class.

        :param Vector func_vec: Coefficients of the equation.
        :param Matrix conditions_matrix: The left part of the restriction system.
        :param Vector constraints_vec: The right part of the restriction system.
        :param str var_tag: The name of the variables (default: 'x').
        :param str func_tag: The name of the function (default: 'F').
        :param int log_mode: So much information about the solution to write
                             to the console (default: LogMode.LOG_OFF).
        """
        self.c_vec = np.array(func_vec, dtype=np.float64)
        self.a_matrix = np.array(conditions_matrix, dtype=np.float64)
        self.b_vec = np.array(constraints_vec, dtype=np.float64)
        self.num_of_vars = self.c_vec.shape[0]

        self.var_tag = var_tag
        self.func_tag = func_tag
        self.log_mode = log_mode

        self._nodes = list()
        self._solution = NotImplemented
        self._func_value = NotImplemented

    def solve(self) -> (np.ndarray, np.float64):
        """
        Solves the problem of integer linear programming by the method of full iteration.

        :return: The solution and the value of the function.
        :rtype: (np.ndarray, np.float64)
        """
        simplex = SimplexMethod(
            self.c_vec,
            self.a_matrix,
            self.b_vec,
            var_tag=self.var_tag,
            func_tag=self.func_tag,
            log_mode=self.log_mode
        )
        simplex.solve()

        simplex_func_value = simplex.get_func_value()
        self._func_value = -np.inf if simplex_func_value > 0 else np.inf
        limit_value = np.ceil(simplex_func_value / self.c_vec.min())
        if self.log_mode is LogMode.FULL_LOG:
            print(
                f"The upper bound of values for all variables {self.var_tag}: {limit_value}.\n"
            )

        for test_solution in itertools.product(np.arange(limit_value + 1), repeat=self.num_of_vars):
            test_solution_np = np.array(test_solution)

            if self._check_solution(test_solution_np):
                func_value = sum(test_solution_np * self.c_vec)
                new_node = [int(s) for s in test_solution] + [func_value]
                self._nodes.append(new_node)

                if (simplex_func_value > 0 and func_value > self._func_value)\
                        or (simplex_func_value <= 0 and func_value < self._func_value):
                    self._func_value = func_value
                    self._solution = test_solution_np

        if self.log_mode is LogMode.FULL_LOG:
            print("Table of solutions:")
            field_names = [f"{simplex.table.var_tag}{i + 1}" for i in range(self.c_vec.shape[0])]
            field_names.append(simplex.table.func_tag)
            solutions_table = prettytable.PrettyTable(field_names=field_names)
            solutions_table.add_rows(self._nodes)
            print(solutions_table, "\n")

        if self.log_mode in (LogMode.MEDIUM_LOG, LogMode.FULL_LOG):
            print("\nSolution of the integer problem of linear programming:")
            print(np.around(self._solution, 3))
            print("The value of the function:")
            print(np.around(self._func_value, 3), "\n")

        return self._solution, self._func_value

    def _check_solution(self, solution: np.ndarray) -> bool:
        """
        Checks the solution for compliance with a system of equations with constraints.

        :param np.ndarray solution: Integer values of variables.
        :return: Does the solution satisfy the constraint system?
        :rtype: bool
        """
        b_test = np.sum(self.a_matrix * solution, axis=1)
        vec_of_comparisons = (b_test <= self.b_vec)
        return vec_of_comparisons.sum() == vec_of_comparisons.shape[0]

    def get_solution(self) -> np.ndarray:
        """
        Return solution of problem of linear programming.

        :return: Solution of problem of linear programming.
        :rtype: np.ndarray
        """
        return self._solution

    def get_func_value(self) -> np.float64:
        """
        Return the value of the function.

        :return: The value of the function.
        :rtype: np.float64
        """
        return self._func_value
