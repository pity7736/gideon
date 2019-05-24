
cdef class Field:

    _internal_type = None

    def __init__(self, str name=''):
        self.name = name

    cpdef to_db(self, value):
        if value is None or type(value) is self.internal_type:
            return value
        return self._internal_type(value)

    @property
    def internal_type(self):
        return self._internal_type
