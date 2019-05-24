from .field cimport Field


cdef class ForeignKeyField(Field):

    def __init__(self, to, str name):
        super().__init__(name=name)
        self._to = to

    @property
    def internal_type(self):
        return int
