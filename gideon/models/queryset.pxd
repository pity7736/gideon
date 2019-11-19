
cdef class QuerySet:
    cdef readonly _model
    cdef readonly _criteria
    cdef readonly _fields
    cdef _client
