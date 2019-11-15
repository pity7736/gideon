from gideon import connection_pool


cdef class QuerySet:

    def __init__(self, model, criteria=None, fields=()):
        self._model = model
        self._criteria = criteria or {}
        self._fields = fields or '*'

    def __await__(self):
        return self._run_query().__await__()

    async def _run_query(self):
        cdef int i
        cdef str field
        condition_fields = ' AND '.join([f'{field} = ${i}' for i, field in enumerate(self._criteria.keys(), start=1)])
        connection = await connection_pool.acquire()
        records = await connection.fetch(
            f'select {self._fields} from {self._model.__table_name__} where {condition_fields}',
            *self._criteria.values()
        )
        await connection_pool.release(connection)
        return [self._model(**record) for record in records]

    def filter(self, **criteria):
        assert criteria, 'keyword arguments are obligatory. If you want all records, use all method instead.'
        self._criteria.update(criteria)
        return QuerySet(self._model, self._criteria)

    async def get(self, **criteria):
        fields = []
        for i, key in enumerate(criteria.keys(), start=1):
            fields.append(f'{key} = ${i}')

        fields = ' AND '.join(fields)
        sql = f'select * from {self._model.__table_name__} where {fields}'
        connection = await connection_pool.acquire()
        record = await connection.fetchrow(sql, *criteria.values())
        await connection_pool.release(connection)
        if record:
            return self._model(**record)

    async def all(self):
        connection = await connection_pool.acquire()
        records = await connection.fetch(f'select * from {self._model.__table_name__}')
        await connection_pool.release(connection)
        result = []
        for record in records:
            result.append(self._model(**record))
        return result

    def only(self, *fields):
        return QuerySet(self._model, self._criteria, ', '.join(fields))
