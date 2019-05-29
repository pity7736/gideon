from cpython cimport bool


cdef class Field:
    cdef readonly str _name
    cdef readonly bool _read_only

    cpdef public to_db(self, value)
