cdef class ComplexCriterion:
    cdef _comparator
    cdef _left
    cdef _right

    cpdef str get_sql(self)
