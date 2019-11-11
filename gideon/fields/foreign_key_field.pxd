from .field cimport Field


cdef class ForeignKeyField(Field):
    cdef readonly _to
