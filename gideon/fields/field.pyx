from enum import EnumMeta, Enum

from cpython cimport bool

from gideon.exceptions import InvalidChoice

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

    @property
    def internal_type(self):
        return self._internal_type

    cpdef to_db(self, value):
        if value is None or type(value) is self._internal_type:
            return value

        if isinstance(value, Enum):
            return value.value

        return self._internal_type(value)

    cpdef to_python(self, value):
        if value and self._choices:
            try:
                return self._choices(value)
            except ValueError:
                choices = ', '.join([i.value for i in self._choices.__members__.values()])
                raise InvalidChoice(f'{value} is not a valid choice. Choices are {choices}')

        if value is None or type(value) is self._internal_type:
            return value

        return self._internal_type(value)
