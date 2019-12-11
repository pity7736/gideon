cdef class ComplexCriterion:

    def __init__(self, comparator, left, right):
        self._comparator = comparator
        self._left = left
        self._right = right

    cpdef str get_sql(self):
        return f'{self._left.field.name} = $1 {self._comparator} {self._right.field.name} = $2'

    @property
    def values(self):
        return self._left.value, self._right.value
