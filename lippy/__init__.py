from .simplex_method import SimplexMethod
from .branch_and_bound import BranchAndBound
from .brute_force import BruteForce
from .cutting_plane_method import CuttingPlaneMethod
from .zero_sum_game import ZeroSumGame
from ._log_modes import FULL_LOG, MEDIUM_LOG, LOG_OFF
from .dual_lp import primal_to_dual_lp


__version__ = "0.0.1"
__doc__ = """
LipPy
=====

Provides
  1. Solving primal linear programming problems
  2. Solving dual linear programming problems
  3. Solving integer linear programming problems
  4. Solving zero-sum games
----------------------------

@Medvate was developed.
GitHub repository: <https://github.com/Medvate/lippy>
Materials written by N.S.Konnova used in the development.
"""



