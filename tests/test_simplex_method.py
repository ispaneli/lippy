import unittest

import src.lippy as lp


class TestSimplexMethod(unittest.TestCase):
    """
    Class for testing Simplex Method.
    """
    def test_primal_linear_programming(self):
        c_vec = [6, 6, 6]
        a_matrix = [
            [4, 1, 1],
            [1, 2, 0],
            [0, 0.5, 4]
        ]
        b_vec = [5, 3, 8]

        simplex = lp.SimplexMethod(c_vec, a_matrix, b_vec)
        solution, func_value = simplex.solve()

        solution = [round(v, 3) for v in solution]
        self.assertEqual(solution, [0.474, 1.263, 1.842])

        func_value = round(func_value, 3)
        self.assertEqual(func_value, 21.474)

    def test_dual_linear_programming(self):
        c_vec = [6, 6, 6]
        a_matrix = [
            [4, 1, 1],
            [1, 2, 0],
            [0, 0.5, 4]
        ]
        b_vec = [5, 3, 8]

        c_vec, a_matrix, b_vec = lp.primal_to_dual_lp(c_vec, a_matrix, b_vec)
        simplex = lp.SimplexMethod(c_vec, a_matrix, b_vec)
        solution, func_value = simplex.solve()

        solution = [round(v, 3) for v in solution]
        self.assertEqual(solution, [0.947, 2.211, 1.263])

        func_value = round(func_value, 3)
        self.assertEqual(func_value, -21.474)

