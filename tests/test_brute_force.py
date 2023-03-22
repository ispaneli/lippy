import unittest

import src.lippy as lp


class TestBruteForce(unittest.TestCase):
    """
    Class for testing Brute force algorithm.
    """
    def test_usual_case(self):
        c_vec = [3, 3, 7]
        a_matrix = [
            [1, 1, 1],
            [1, 4, 0],
            [0, 0.5, 3]
        ]
        b_vec = [3, 5, 7]

        force = lp.BruteForce(c_vec, a_matrix, b_vec)
        solution, func_value = force.solve()

        self.assertEqual(solution.tolist(), [0, 1, 2])
        self.assertEqual(func_value, 17)
