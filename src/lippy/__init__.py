from .bnb import BranchAndBound
from .brute_force import BruteForce
from .dual import primal_to_dual_lp
from .game import ZeroSumGame
from .gomory import CuttingPlaneMethod
from .simplex import SimplexMethod

from .enums import LogMode


__author__ = 'ispaneli'
__email__ = 'ispanelki@gmail.com'

__version__ = '0.0.5'

__doc__ = """
Lippy
=====

Provides:
  1. Simplex method in primal linear programming
  2. Simplex method in dual linear programming
  3. Branch and bound in integer linear programming
  4. Brute force method in integer linear programming
  5. Cutting-plane method in integer linear programming
  6. Zero-sum game in game theory (using Simplex method)
----------------------------

Author: @ispaneli
E-mail: ispanelki@gmail.com
GitHub repository: <https://github.com/ispaneli/lippy>

p.s. During the development, the materials of N.S.Konnova (BMSTU, IU-8) were used.
"""




