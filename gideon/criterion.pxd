
cdef class Criterion:

    cdef _value
    cdef _field

    cpdef get_sql(self)
