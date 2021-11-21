import unittest

import lippy as lp


class TestZeroSumGame(unittest.TestCase):
    """Class for testing Zero-sum game."""
    def test_usual_case(self):
        game_matrix = [[8, 1, 17, 8, 1],
                       [12, 6, 11, 10, 16],
                       [4, 19, 11, 15, 2],
                       [17, 19, 6, 17, 16]]

        game = lp.ZeroSumGame(game_matrix)
        strategies = game.solve()
        strategy_1 = [round(v, 3) for v in strategies[0]]
        strategy_2 = [round(v, 3) for v in strategies[1]]

        self.assertEqual(strategy_1, [0.051, 0.668, 0.281, 0.0])
        self.assertEqual(strategy_2, [0.063, 0.201, 0.586, 0.0, 0.15])
