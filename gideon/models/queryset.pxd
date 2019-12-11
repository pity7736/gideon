
cdef class QuerySet:
    cdef _model
    cdef _criteria
    cdef _fields
    cdef _get
    cdef _criterion
