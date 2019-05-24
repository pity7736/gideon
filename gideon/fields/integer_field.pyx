from .field import Field


cdef class IntegerField(Field):

    _internal_type = int
