from cpython cimport bool


cdef class Field:

    _internal_type = None

    def __init__(self, str name='', bool read_only=False):
        self._name = name
        self._read_only = read_only

    @property
    def name(self):
        return self._name

    @property
    def read_only(self):
        return self._read_only

    cpdef to_db(self, value):
        if value is None or type(value) is self.internal_type:
            return value
        return self._internal_type(value)

    @property
    def internal_type(self):
        return self._internal_type
