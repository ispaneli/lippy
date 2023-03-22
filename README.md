<p align="center">
  <a href="https://pypi.org/project/lippy">
    <img src="https://raw.githubusercontent.com/ispaneli/lippy/master/docs/img/logo.png" alt="Lippy">
  </a>
</p>
<p align="center">
  <em>Lippy - solving linear programming problems.</em>
</p>
<p align="center">
  <a href="https://github.com/ispaneli/lippy/actions?query=workflow%3ATests+event%3Apush+branch%3Amaster" target="_blank">
      <img src="https://github.com/ispaneli/lippy/workflows/Tests/badge.svg?event=push&branch=master" alt="Tests">
  </a>
  <a href="https://pypi.org/project/lippy" target="_blank">
    <img src="https://img.shields.io/pypi/v/lippy?color=%2334D058&label=pypi%20package" alt="Package version">
  </a>
  <a href="https://pypi.org/project/lippy" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/lippy.svg?color=%2334D058" alt="Supported Python versions">
  </a>
  <a href="https://pypi.org/project/lippy" target="_blank">
    <img src="https://static.pepy.tech/personalized-badge/lippy?period=total&units=none&left_color=grey&right_color=brightgreen&left_text=Downloads" alt="Total downloads">
  </a>
</p>

---

**Source Code**:
<a href="https://github.com/ispaneli/lippy" target="_blank">
  https://github.com/ispaneli/lippy
</a>

---

**Lippy** is a module for solving **linear programming problems** on Python.

Provides:
1. [Simplex method in primal linear programming](#simplex-method-in-primal-linear-programming)
2. [Simplex method in dual linear programming](#simplex-method-in-dual-linear-programming)
3. [Branch and bound in integer linear programming](#branch-and-bound-in-integer-linear-programming)
4. [Brute force method in integer linear programming](#brute-force-method-in-integer-linear-programming)
5. [Cutting-plane method in integer linear programming](#cutting-plane-method-in-integer-linear-programming)
6. [Zero-sum game in game theory using Simplex method](#zero-sum-game-in-game-theory-using-simplex-method)

---

## Simplex method in primal linear programming

```python
import lippy as lp


c_vec = [6, 6, 6]
a_matrix = [
    [4, 1, 1],
    [1, 2, 0],
    [0, 0.5, 4]
]
b_vec = [5, 3, 8]

simplex = lp.SimplexMethod(c_vec, a_matrix, b_vec)
solution, func_value = simplex.solve()
```

---

## Simplex method in dual linear programming

```python
import lippy as lp


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
```

---

## Branch and bound in integer linear programming

```python
import lippy as lp


c_vec = [3, 3, 7]
a_matrix = [
    [1, 1, 1],
    [1, 4, 0],
    [0, 0.5, 3]
]
b_vec = [3, 5, 7]

bab = lp.BranchAndBound(c_vec, a_matrix, b_vec)
solution, func_value = bab.solve()
```

---

## Brute force method in integer linear programming

```python
import lippy as lp


c_vec = [3, 3, 7]
a_matrix = [
    [1, 1, 1],
    [1, 4, 0],
    [0, 0.5, 3]
]
b_vec = [3, 5, 7]

force = lp.BruteForce(c_vec, a_matrix, b_vec)
solution, func_value = force.solve()
```

---

## Cutting-plane method in integer linear programming

```python
import lippy as lp


c_vec = [3, 3, 7]
a_matrix = [
    [1, 1, 1],
    [1, 4, 0],
    [0, 0.5, 3]
]
b_vec = [3, 5, 7]

gomory = lp.CuttingPlaneMethod(c_vec, a_matrix, b_vec)
gomory.solve()
```

---

## Zero-sum game in game theory using Simplex method

```python
import lippy as lp


game_matrix = [
    [8, 1, 17, 8, 1],
    [12, 6, 11, 10, 16],
    [4, 19, 11, 15, 2],
    [17, 19, 6, 17, 16]
]

game = lp.ZeroSumGame(game_matrix)
strategies = game.solve()
```

---

## Logging

Existing logging modes:
1. FULL_LOG
2. MEDIUM_LOG
3. LOG_OFF *(default)*

Logging is set when initializing a class object.

For example:

```python
simplex = lp.SimplexMethod(c_vec, a_matrix, b_vec, log_mode=lp.LogMode.FULL_LOG)
```

```python
bab = lp.BranchAndBound(c_vec, a_matrix, b_vec, log_mode=lp.LogMode.MEDIUM_LOG)
```

---

## License

This project is licensed under the terms of the [MIT license](https://github.com/ispaneli/lippy/blob/master/LICENSE).
