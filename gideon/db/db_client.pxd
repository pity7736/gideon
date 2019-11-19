
cdef class DBClient:
    cdef str _user
    cdef str _password
    cdef str _host
    cdef int _port
    cdef str _database
    cdef _pool
