from .field import Field


cdef class CharField(Field):

    _internal_type = str
