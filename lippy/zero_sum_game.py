from typing import List

import numpy as np

from .simplex_method import SimplexMethod
from ._log_modes import FULL_LOG, MEDIUM_LOG, LOG_OFF


class ZeroSumGame:
    """
    In game theory and economic theory, a zero-sum game is a mathematical representation
    of a situation in which an advantage that is won by one of two sides is lost by the other.
    If the total gains of the participants are added up, and the total losses are subtracted, they will sum to zero.
    """
    def __init__(self, matrix: List[List[int or float]] or np.ndarray, var_tag: str = "x",
                 func_tag: str = "F", log_mode: int = LOG_OFF):
        """
        Initialization of an object of the "Zero-sum game" class.

        :param matrix: Game's payoff matrix.
        :param var_tag: The name of the variables, default is "x".
        :param func_tag: The name of the function, default is "F".
        :param log_mode: So much information about the solution to write to the console.
        """
        self.matrix = np.array(matrix, dtype=np.float64)
        self.optimal_strategies = list()

        self.var_tag = var_tag
        self.func_tag = func_tag
        self.log_mode = log_mode

    def solve(self) -> [np.ndarray, np.ndarray]:
        """
        Finds optimal strategies for both players.

        :return: Optimal strategies.
        """
        self._solve_for_player(-np.ones(self.matrix.shape[0]), -self.matrix.T, -np.ones(self.matrix.shape[1]))
        if self.log_mode in [FULL_LOG, MEDIUM_LOG]:
            print(f"Winning strategy for the first player: {np.around(self.optimal_strategies[0], 3)}\n\n")

        self._solve_for_player(np.ones(self.matrix.shape[1]), self.matrix, np.ones(self.matrix.shape[0]))
        if self.log_mode in [FULL_LOG, MEDIUM_LOG]:
            print(f"Winning strategy for the second player: {np.around(self.optimal_strategies[1], 3)}\n\n")

        return self.optimal_strategies

    def _solve_for_player(self, c_vec: np.ndarray, matrix: np.ndarray, b_vec: np.ndarray) -> None:
        """
        Finds optimal strategies for a player.

        :param c_vec: Coefficients of the equation.
        :param matrix: Game's payoff matrix.
        :param b_vec: The right part of the restriction system.
        :return: None
        """
        simplex = SimplexMethod(c_vec, matrix, b_vec, var_tag=self.var_tag,
                                func_tag=self.func_tag, log_mode=self.log_mode)
        simplex.solve()

        h = abs(1 / simplex.get_func_value())
        if self.log_mode == FULL_LOG:
            print(f"h = {round(h, 3)}")
        solution = simplex.get_solution() * h
        self.optimal_strategies.append(solution)
