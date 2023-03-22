import unittest

import src.lippy as lp


class TestZeroSumGame(unittest.TestCase):
    """Class for testing Zero-sum game."""
    def test_usual_case_1(self):
        game_matrix = [
            [1, 3, 9, 6],
            [2, 6, 2, 3],
            [7, 2, 6, 5]
        ]

        game = lp.ZeroSumGame(game_matrix)
        optimal_strategies = game.solve()
        optimal_strategies_1 = [round(v, 3) for v in optimal_strategies[0]]
        optimal_strategies_2 = [round(v, 3) for v in optimal_strategies[1]]

        self.assertEqual(optimal_strategies_1, [0.071, 0.5, 0.429])
        self.assertEqual(optimal_strategies_2, [0.143, 0.405, 0.0, 0.452])

    def test_usual_case_2(self):
        game_matrix = [
            [8, 1, 17, 8, 1],
            [12, 6, 11, 10, 16],
            [4, 19, 11, 15, 2],
            [17, 19, 6, 17, 16]
        ]

        game = lp.ZeroSumGame(game_matrix)
        optimal_strategies = game.solve()
        optimal_strategies_1 = [round(v, 3) for v in optimal_strategies[0]]
        optimal_strategies_2 = [round(v, 3) for v in optimal_strategies[1]]

        self.assertEqual(optimal_strategies_1, [0.15, 0.422, 0.21, 0.218])
        self.assertEqual(optimal_strategies_2, [0.063, 0.201, 0.586, 0.0, 0.15])
