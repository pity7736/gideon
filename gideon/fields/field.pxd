cdef class Field:
    cdef public str name

    cpdef public to_db(self, value)
