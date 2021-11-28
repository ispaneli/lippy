from typing import List, Tuple

import numpy as np


def primal_to_dual_lp(func_vec: List[List[int or float]] or np.ndarray,
                      conditions_matrix: List[List[int or float]] or np.ndarray,
                      constraints_vec: List[List[int or float]] or np.ndarray) -> Tuple[np.ndarray, np.ndarray,
                                                                                        np.ndarray]:
    """
    Converts a primal linear programming problem into a dual.

    :param func_vec: Coefficients of the equation.
    :param conditions_matrix: The left part of the restriction system.
    :param constraints_vec: The right part of the restriction system.
    :return: Formulation of a dual linear programming problem.
    """
    func_vec = np.array(func_vec, dtype=np.float64)
    conditions_matrix = np.array(conditions_matrix, dtype=np.float64)
    constraints_vec = np.array(constraints_vec, dtype=np.float64)

    return -constraints_vec, -conditions_matrix.T, -func_vec
