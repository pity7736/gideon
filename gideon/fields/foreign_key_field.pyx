from .field cimport Field


cdef class ForeignKeyField(Field):

    def __init__(self, to, **kwargs):
        assert kwargs.get('read_only', False) is False, 'ForeignKeyField not can be read only'
        super().__init__(**kwargs)
        self._to = to

    @property
    def internal_type(self):
        return int

    @property
    def to(self):
        return self._to
