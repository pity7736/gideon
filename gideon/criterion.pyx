from .complex_criterion cimport ComplexCriterion


cdef class Criterion:

    def __init__(self, field, value):
        self._field = field
        self._value = value

    cpdef get_sql(self):
        return f"{self._field.name} = $1"

    @property
    def field(self):
        return self._field

    @property
    def value(self):
        return self._value

    @property
    def values(self):
        return self._value,

    def __and__(self, other):
        return ComplexCriterion(comparator='AND', left=self, right=other)
