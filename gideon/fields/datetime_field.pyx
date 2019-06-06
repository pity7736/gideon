import datetime

from .field cimport Field


cdef class DateTimeField(Field):

    _internal_type = datetime.datetime


    cpdef to_db(self, value):
        if isinstance(value, self._internal_type):
            return value

        if isinstance(value, str):
            return self._internal_type.fromisoformat(value)
