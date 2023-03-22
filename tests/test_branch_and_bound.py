import unittest

import src.lippy as lp


class TestBranchAndBound(unittest.TestCase):
    """
    Class for testing Branch and Bound algorithm.
    """
    def test_usual_case(self):
        c_vec = [3, 3, 7]
        a_matrix = [
            [1, 1, 1],
            [1, 4, 0],
            [0, 0.5, 3]
        ]
        b_vec = [3, 5, 7]

        bab = lp.BranchAndBound(c_vec, a_matrix, b_vec)
        solution, func_value = bab.solve()

        self.assertEqual(solution.tolist(), [0, 1, 2])
        self.assertEqual(func_value, 17)
