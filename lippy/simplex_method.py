import numpy as np
from typing import List

from ._simplex_table import _SimplexTable
from ._log_modes import FULL_LOG, MEDIUM_LOG, LOG_OFF


class SimplexMethod:
    """
    In mathematical optimization, Dantzig's simplex algorithm
    (or simplex method) is a popular algorithm for linear programming.
    """
    def __init__(self, func_vec: List[int or float] or np.ndarray,
                 conditions_matrix: List[List[int or float]] or np.ndarray,
                 constraints_vec: List[int or float] or np.ndarray,
                 var_tag: str = "x", func_tag: str = "F", log_mode: int = LOG_OFF):
        """
        Initialization of an object of the SimplexMethod-class.

        :param func_vec: Coefficients of the equation.
        :param conditions_matrix: The left part of the restriction system.
        :param constraints_vec: The right part of the restriction system.
        :param var_tag: The name of the variables, default is "x".
        :param func_tag: The name of the function, default is "F".
        :param log_mode: So much information about the solution to write to the console.
        """
        self.c_vec = np.array(func_vec, np.float64)
        self.a_matrix = np.array(conditions_matrix, np.float64)
        self.b_vec = np.array(constraints_vec, np.float64)

        self.log_mode = log_mode

        self.table = _SimplexTable(self.c_vec, self.a_matrix, self.b_vec, var_tag, func_tag)

    def solve(self) -> (np.ndarray, np.float64):
        """
        Solve the problem of linear programming by the simplex method.

        :return: The solution and the value of the function.
        """
        if not self.table.has_optimal_solution():
            if self.log_mode in [FULL_LOG, MEDIUM_LOG]:
                print("Linear program has not optimal solution.")
            return
        if self.table.was_solved():
            if self.log_mode in [FULL_LOG, MEDIUM_LOG]:
                print("Linear program was solved.")
            return

        if self.log_mode == FULL_LOG:
            print(f"Input data:\nc = {self.c_vec}\nA = {self.a_matrix}\nb = {self.b_vec}\n")

        if self.log_mode in [FULL_LOG, MEDIUM_LOG]:
            print("Start table:")
            print(self.table, "\n")
        while self.one_iteration():
            if self.log_mode == FULL_LOG:
                print(self.table, "\n")

        if self.log_mode in [FULL_LOG, MEDIUM_LOG]:
            print("\nSolution of the problem of linear programming:")
            print(np.around(self.get_solution(), 3))
            print("The value of the function:")
            print(np.around(self.get_func_value(), 3), "\n")

        return self.get_solution(), self.get_func_value()

    def one_iteration(self) -> bool:
        """
        Performs one iteration of the simplex method.

        :return: If the problem of linear programming was solved - False; else - True.
        """
        index_of_pivot_column = self.table.get_index_of_pivot_column()
        if index_of_pivot_column == -1:
            return False

        index_of_pivot_row = self.table.get_index_of_pivot_row(index_of_pivot_column)
        if index_of_pivot_row == -1:
            return False

        if self.log_mode in [FULL_LOG, MEDIUM_LOG]:
            print(f"The pivot column: {self.table.column_tags[index_of_pivot_column]}; "
                  f"the pivot row: {self.table.row_tags[index_of_pivot_row]}:")

        self.table.recalculate(index_of_pivot_row, index_of_pivot_column)
        return True

    def get_solution(self, _num_of_vars: int = None) -> np.ndarray:
        """
        Return solution of problem of linear programming.

        :param _num_of_vars: The number of variables in the equation.
        :return: Solution of problem of linear programming
        """
        if _num_of_vars is None:
            _num_of_vars = self.c_vec.shape[0]
        return self.table.get_solution(_num_of_vars)

    def get_func_value(self) -> np.float64:
        """
        Return the value of the function.

        :return: The value of the function.
        """
        return self.table.get_func_value()

    def print_solution_check(self, _num_of_vars: int = None) -> None:
        """
        Arithmetically checks the solution that was obtained by the simplex method.

        :param _num_of_vars: The number of variables in the equation.
        :return: None.
        """
        if _num_of_vars is None:
            _num_of_vars = self.c_vec.shape[0]
        solution = self.get_solution(_num_of_vars)

        # 1. Checking the equation.
        around_solution = np.around(solution, 3)
        var_tags = [f"{self.table.var_tag}{i + 1}" for i in range(_num_of_vars)]

        equation_1 = " + ".join([f"{c}*{v}" for c, v in zip(self.c_vec, var_tags)])
        equation_2 = " + ".join([f"{c}*{v}" for c, v in zip(self.c_vec, around_solution)])
        func_value = round(sum([c * v for c, v in zip(self.c_vec, around_solution)]), 3)

        print("Solution check:\n1. Function:")
        print(f"      • {self.table.func_tag} = {equation_1} = {equation_2} = {func_value}")

        # 2. Checking the restriction system.
        print("2. Restriction system:")

        b_test = np.sum(self.a_matrix * solution, axis=1)
        vec_of_comparisons = (b_test <= self.b_vec)

        for a_row_i, b_i, answer in zip(self.a_matrix, self.b_vec, vec_of_comparisons):
            equation_i = list()
            for x_i, a_i in zip(around_solution, a_row_i):
                if x_i != 0 and a_i != 0:
                    equation_i.append(f"{a_i}*{x_i}")

            print("      • " + " + ".join(equation_i) + f" <= {b_i}, <-- {bool(answer)}")

