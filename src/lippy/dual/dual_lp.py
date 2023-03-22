import numpy as np

from ..types import Vector, Matrix


def primal_to_dual_lp(
    func_vec: Vector,
    conditions_matrix: Matrix,
    constraints_vec: Vector
) -> (np.ndarray, np.ndarray, np.ndarray):
    """
    Converts a primal linear programming problem into a dual.

    :param Vector func_vec: Coefficients of the equation.
    :param Matrix conditions_matrix: The left part of the restriction system.
    :param Vector constraints_vec: The right part of the restriction system.
    :return: Formulation of a dual linear programming problem.
    :rtype: (np.ndarray, np.ndarray, np.ndarray)
    """
    func_vec = np.array(func_vec, dtype=np.float64)
    conditions_matrix = np.array(conditions_matrix, dtype=np.float64)
    constraints_vec = np.array(constraints_vec, dtype=np.float64)

    return -constraints_vec, -conditions_matrix.T, -func_vec
