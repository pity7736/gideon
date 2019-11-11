from .field cimport Field


cdef class IntegerField(Field):

    _internal_type = int
