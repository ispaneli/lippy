from enum import Enum


class LogMode(Enum):
    """
    Enum of logging modes for solving linear programming problems.
    """
    LOG_OFF = 0
    MEDIUM_LOG = 1
    FULL_LOG = 2
