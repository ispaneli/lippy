import numpy as np

from ..simplex import SimplexMethod
from ..enums import LogMode
from ..types import Matrix


class ZeroSumGame:
    """
    In game theory and economic theory, a zero-sum game
    is a mathematical representation of a situation in which
    an advantage that is won by one of two sides is lost by the other.

    If the total gains of the participants are added up,
    and the total losses are subtracted, they will sum to zero.
    """
    def __init__(
        self,
        matrix: Matrix,
        var_tag: str = 'x',
        func_tag: str = 'F',
        log_mode: int = LogMode.LOG_OFF
    ):
        """
        Initialization of an object of the "Zero-sum game" class.

        :param Matrix matrix: Game's payoff matrix.
        :param str var_tag: The name of the variables (default: 'x').
        :param str func_tag: The name of the function (default: 'F').
        :param int log_mode: So much information about the solution to write
                             to the console (default: LogMode.LOG_OFF).
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
        :rtype: [np.ndarray, np.ndarray]
        """
        self._solve_for_player(
            -np.ones(self.matrix.shape[0]),
            -self.matrix.T,
            -np.ones(self.matrix.shape[1])
        )
        if self.log_mode in (LogMode.MEDIUM_LOG, LogMode.FULL_LOG):
            print(
                f"Winning strategy for the first player: {np.around(self.optimal_strategies[0], 3)}\n\n"
            )

        self._solve_for_player(np.ones(self.matrix.shape[1]), self.matrix, np.ones(self.matrix.shape[0]))
        if self.log_mode in (LogMode.MEDIUM_LOG, LogMode.FULL_LOG):
            print(
                f"Winning strategy for the second player: {np.around(self.optimal_strategies[1], 3)}\n\n"
            )

        return self.optimal_strategies

    def _solve_for_player(
        self,
        c_vec: np.ndarray,
        matrix: np.ndarray,
        b_vec: np.ndarray
    ) -> None:
        """
        Finds optimal strategies for a player.

        :param np.ndarray c_vec: Coefficients of the equation.
        :param np.ndarray matrix: Game's payoff matrix.
        :param np.ndarray b_vec: The right part of the restriction system.
        :return: None
        """
        simplex = SimplexMethod(
            c_vec,
            matrix,
            b_vec,
            var_tag=self.var_tag,
            func_tag=self.func_tag,
            log_mode=self.log_mode
        )
        simplex.solve()

        h = abs(1 / simplex.get_func_value())
        if self.log_mode is LogMode.FULL_LOG:
            print(f"h = {round(h, 3)}")
        solution = simplex.get_solution() * h
        self.optimal_strategies.append(solution)
