import datetime

from .field cimport Field


cdef class DateField(Field):

    _internal_type = datetime.date

    cpdef to_db(self, value):
        if isinstance(value, datetime.date) or value is None:
            return value

        if isinstance(value, str):
            return datetime.datetime.strptime(value, '%Y-%m-%d').date()
