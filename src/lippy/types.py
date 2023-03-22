from typing import (
    List,
    NewType,
    Union
)

import numpy as np


Vector = NewType('Matrix', Union[List[int or float], np.ndarray])
Matrix = NewType('Matrix', Union[List[List[int or float]], np.ndarray])
