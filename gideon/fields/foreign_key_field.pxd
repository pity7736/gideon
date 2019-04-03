from .field cimport Field


cdef class ForeignKeyField(Field):
    cdef public _to
