import random
from typing import List

import numpy as np
import prettytable


random.seed(43)


class _SimplexTable:
    """
    A table that provides a convenient interface for the operation of the Simplex method.
    """
    DECIMALS_FOR_AROUND = 3

    def __init__(self, func_vec: np.ndarray, conditions_matrix: np.ndarray,
                 constraints_vec: np.ndarray, var_tag: str, func_tag: str):
        """
        Initialization of an object of the "Simplex table" class.

        :param func_vec: Coefficients of the equation.
        :param conditions_matrix: The left part of the restriction system.
        :param constraints_vec: The right part of the restriction system.
        :param var_tag: The name of the variables, default is "x".
        :param func_tag: The name of the function, default is "F".
        """
        self.table: np.ndarray = NotImplemented

        self.var_tag = var_tag
        self.func_tag = func_tag

        self.column_tags: List[str] = NotImplemented
        self.row_tags: List[str] = NotImplemented

        self.column_indices: List[int] = NotImplemented
        self.row_indices: List[int] = NotImplemented

        self._has_optimal_solution = True
        self._was_solved = False

        self._set_table(func_vec, conditions_matrix, constraints_vec)

    def _set_table(self, c_vec: np.ndarray, a_matrix: np.ndarray, b_vec: np.ndarray) -> None:
        """
        Filling the class object with data.

        :param c_vec: Coefficients of the equation.
        :param a_matrix: The left part of the restriction system.
        :param b_vec: The right part of the restriction system.
        :return: None.
        """
        # 1. Check shapes of data.
        self._check_input_data(c_vec, a_matrix, b_vec)

        # 2. Set simplex-table.
        self.table = np.zeros([size + 1 for size in a_matrix.shape], dtype=np.float64)
        self.table[:-1, 1:] = a_matrix
        self.table[:-1, 0] = b_vec
        self.table[-1, 1:] = c_vec

        # 3. Set tags for print-ability.
        self.column_indices = [i for i in range(self.table.shape[1])]
        self.column_tags = [f"{self.var_tag}{i}" for i in self.column_indices]
        self.column_tags[0] = "S0"

        self.row_indices = [i + self.table.shape[1] for i in range(self.table.shape[0])]
        self.row_tags = [f"{self.var_tag}{i}" for i in self.row_indices]
        self.row_tags[-1] = self.func_tag

    @staticmethod
    def _check_input_data(c_vec: np.ndarray, a_matrix: np.ndarray, b_vec: np.ndarray) -> None:
        """
        Checking the dimensions of the input data for errors.

        :param c_vec: Coefficients of the equation.
        :param a_matrix: The left part of the restriction system.
        :param b_vec: The right part of the restriction system.
        :return: None.
        """
        if len(b_vec.shape) > 1:
            raise ValueError("The shape of constraints-vector must be of the form (m,).")
        if len(c_vec.shape) > 1:
            raise ValueError("The shape of function-vector must be of the form (n,).")
        if b_vec.shape[0] != a_matrix.shape[0]:
            raise ValueError("The shape of constraints-vector must be of the form (m,); "
                             "the shape of conditions-matrix must be of the form (m, n).")
        if c_vec.shape[0] != a_matrix.shape[1]:
            raise ValueError("The shape of function-vector must be of the form (n,); "
                             "the shape of conditions-matrix must be of the form (m, n).")

    def get_index_of_pivot_column(self) -> int:
        """
        Searches for a pivot column in the simplex table.

        :return: Index of a pivot column.
        """
        index_of_pivot_column = NotImplemented

        # 1. Поиск индекса разрешающего столбца в столбце пересечений S0 со строками с переменными.
        column_s0 = self.table[:-1, 0]
        for row_index, item_s0 in enumerate(column_s0):
            if item_s0 < 0:
                row_without_s0 = self.table[row_index, 1:]
                if row_without_s0.min() >= 0:
                    # System hasn't optimal solution.
                    self._has_optimal_solution = False
                    return -1
                if item_s0 == column_s0.min():
                    index_of_pivot_column = row_without_s0.argmin() + 1

        if index_of_pivot_column is not NotImplemented:
            return index_of_pivot_column

        # 2. Поиск индекса разрешающего столбца в строке пересечений F со столбцами с переменными.
        row_func = self.table[-1, 1:]
        if row_func.max() > 0:
            # find index of minimal positive value in row_func.
            index_of_min: np.ndarray = np.where(row_func == [min(row_func[row_func > 0])])[0]
            return int(index_of_min[0]) + 1

        # Optimal solution was found.
        self._was_solved = True
        return -1

    def get_index_of_pivot_row(self, i_pc: int) -> int:
        """
        Searches for a pivot row in the simplex table.

        :param i_pc: Index of a pivot column.
        :return: Index of a pivot row.
        """
        targets_of_rows = np.zeros((self.table.shape[0] - 1,), dtype=np.float64)

        for index, row in enumerate(self.table[:-1]):
            if row[i_pc] and row[0] / row[i_pc] > 0:
                targets_of_rows[index] = row[0] / row[i_pc]
            else:
                targets_of_rows[index] = np.inf

        indices_of_mins = np.where(targets_of_rows == np.amin(targets_of_rows))[0]
        return random.choice(indices_of_mins)

    def recalculate(self, i_pr: int, i_pc: int) -> None:
        """
        Performs one iteration of the recalculation of the simplex table for a pivot element.

        :param i_pr: Index of a pivot row.
        :param i_pc: Index of a pivot column.
        :return: None.
        """
        self.column_tags[i_pc], self.row_tags[i_pr] = self.row_tags[i_pr], self.column_tags[i_pc]
        self.column_indices[i_pc], self.row_indices[i_pr] = self.row_indices[i_pr], self.column_indices[i_pc]

        central_item = self.table[i_pr, i_pc]
        new_table = np.copy(self.table)
        for i_r, column in enumerate(self.table):
            for i_c, item in enumerate(column):
                if i_r == i_pr and i_c == i_pc:
                    new_table[i_r, i_c] = 1 / central_item
                elif i_r == i_pr:
                    new_table[i_r, i_c] = item / central_item
                elif i_c == i_pc:
                    new_table[i_r, i_c] = -item / central_item
                else:
                    new_table[i_r, i_c] = item - self.table[i_pr, i_c] * self.table[i_r, i_pc] / central_item

        self.table = new_table

    def __str__(self) -> str:
        """
        Returns a beautiful representation of a simplex table for printing.

        :return: Simplex table for print.
        """
        table_for_print = prettytable.PrettyTable(field_names=["", *self.column_tags])

        row_tags = np.array(self.row_tags).reshape((len(self.row_tags), 1))
        data = np.around(self.table, decimals=_SimplexTable.DECIMALS_FOR_AROUND)
        data = np.concatenate((row_tags, data), axis=1)
        table_for_print.add_rows(data)

        return table_for_print.__str__()

    def __repr__(self) -> str:
        """
        Returns representation of a simplex table for printing.

        :return: Simplex table as string.
        """
        return self.__str__()

    def has_optimal_solution(self) -> bool:
        """
        Answers the question: "Has the optimal solution been found?"

        :return: True or False.
        """
        return self._has_optimal_solution

    def was_solved(self) -> bool:
        """
        Answers the question: "Has the linear programming problem been solved?"

        :return: True or False.
        """
        return self._was_solved

    def get_solution(self, num_of_vars: int) -> np.ndarray:
        """
        Return solution of problem of linear programming.

        :return: Solution of problem of linear programming
        """
        solution = np.zeros(num_of_vars, dtype=np.float64)
        for var_index in range(1, num_of_vars + 1):
            if var_index in self.row_indices:
                solution[var_index - 1] = self.table[self.row_indices.index(var_index), 0]

        return solution

    def get_func_value(self) -> np.float64:
        """
        Return the value of the function.

        :return: The value of the function.
        """
        return -self.table[-1, 0]
