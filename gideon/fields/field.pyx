
cdef class Field:

    def __init__(self, str name=''):
        self.name = name

    cpdef to_db(self, value):
        return value
