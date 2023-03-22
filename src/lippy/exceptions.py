TABLE_CONST_VEC_ERROR = ValueError("The shape of constraints-vector must be of the form (m, ).")
TABLE_FUNC_VEC_ERROR = ValueError("The shape of function-vector must be of the form (n, ).")
TABLE_CONST_MATRIX_ERROR = ValueError(
    "The shape of constraints-vector must be of the form (m, ); "
    "the shape of conditions-matrix must be of the form (m, n)."
)
TABLE_FUNC_MATRIX_ERROR = ValueError(
    "The shape of function-vector must be of the form (n, ); "
    "the shape of conditions-matrix must be of the form (m, n)."
)
