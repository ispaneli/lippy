import unittest

import src.lippy as lp


class TestCuttingPlaneMethod(unittest.TestCase):
    """
    Class for testing Cutting Plane Method (Gomory algorithm).
    """
    def test_usual_case(self):
        c_vec = [3, 3, 7]
        a_matrix = [
            [1, 1, 1],
            [1, 4, 0],
            [0, 0.5, 3]
        ]
        b_vec = [3, 5, 7]

        gomory = lp.CuttingPlaneMethod(c_vec, a_matrix, b_vec)
        gomory.solve()

        self.assertEqual(gomory.get_solution().tolist(), [1, 0, 2])
        self.assertEqual(gomory.get_func_value(), 17)
