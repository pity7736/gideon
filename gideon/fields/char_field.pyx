from .field cimport Field


cdef class CharField(Field):

    _internal_type = str
