from enum import EnumMeta, Enum

from cpython cimport bool


cdef class Field:

    _internal_type = None

    def __init__(self, str name='', bool read_only=False, choices=None):
        if choices and type(choices) is not EnumMeta:
            raise ValueError('choices must be Enum type')

        self._name = name
        self._read_only = read_only
        self._choices = choices

    @property
    def name(self):
        return self._name

    @property
    def read_only(self):
        return self._read_only

    @property
    def choices(self):
        return self._choices

    cpdef to_db(self, value):
        if value is None or type(value) is self.internal_type:
            return value

        if isinstance(value, Enum):
            return value.value

        return self._internal_type(value)

    @property
    def internal_type(self):
        return self._internal_type
