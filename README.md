[![pypi version](https://img.shields.io/pypi/v/lippy)](https://pypi.org/project/lippy)

# LipPy
A module for solving **linear programming problems** on Python.

## Install
```shell script
pip install lippy
```

## How to use

### Import
```python3
import lippy as lp
```

### 1. Simplex method in primal linear programming:
```python3
c_vec = [6, 6, 6]
a_matrix = [[4, 1, 1],
            [1, 2, 0],
            [0, 0.5, 4]]
b_vec = [5, 3, 8]

simplex = lp.SimplexMethod(c_vec, a_matrix, b_vec)
solution, func_value = simplex.solve()
```

### 2. Simplex method in dual linear programming:
```python3
c_vec = [6, 6, 6]
a_matrix = [[4, 1, 1],
            [1, 2, 0],
            [0, 0.5, 4]]
b_vec = [5, 3, 8]

c_vec, a_matrix, b_vec = lp.primal_to_dual_lp(c_vec, a_matrix, b_vec)
simplex = lp.SimplexMethod(c_vec, a_matrix, b_vec)
solution, func_value = simplex.solve()
```
### 3. Branch and bound in integer linear programming:
```python3
c_vec = [3, 3, 7]
a_matrix = [[1, 1, 1],
            [1, 4, 0],
            [0, 0.5, 3]]
b_vec = [3, 5, 7]

bab = lp.BranchAndBound(c_vec, a_matrix, b_vec)
solution, func_value = bab.solve()
```

### 4. Brute force method in integer linear programming:
```python3
c_vec = [3, 3, 7]
a_matrix = [[1, 1, 1],
            [1, 4, 0],
            [0, 0.5, 3]]
b_vec = [3, 5, 7]

force = lp.BruteForce(c_vec, a_matrix, b_vec)
solution, func_value = force.solve()
```

### 5. Cutting-plane method in integer linear programming:
```python3
c_vec = [3, 3, 7]
a_matrix = [[1, 1, 1],
            [1, 4, 0],
            [0, 0.5, 3]]
b_vec = [3, 5, 7]

gomory = lp.CuttingPlaneMethod(c_vec, a_matrix, b_vec)
gomory.solve()
```

### 6. Zero-sum game in game theory (using Simplex method):
```python3
game_matrix = [[8, 1, 17, 8, 1],
               [12, 6, 11, 10, 16],
               [4, 19, 11, 15, 2],
               [17, 19, 6, 17, 16]]

game = lp.ZeroSumGame(game_matrix)
strategies = game.solve()
```

### p.s. Conclusion of the solution:

You can use three logging modes: lp.FULL_LOG, lp.MEDIUM_LOG and lp.LOG_OFF.

These values are passed to the parameters of the class you are using.
The default value is lp.LOG_OFF.

**Example:**
```python3
simplex = lp.SimplexMethod(c_vec, a_matrix, b_vec, log_mode=lp.LOG_OFF)
# or
bab = lp.BranchAndBound(c_vec, a_matrix, b_vec, log_mode=lp.LOG_OFF)
```

