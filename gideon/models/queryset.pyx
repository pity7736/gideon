from gideon.db.db_client cimport DBClient


cdef class QuerySet:
    _client = DBClient()

    def __init__(self, model, criteria=None, fields=()):
        self._model = model
        self._criteria = criteria or {}
        self._fields = fields or '*'
        # self._client = DBClient()

    def __await__(self):
        return self._run_query().__await__()

    async def _run_query(self):
        cdef int i
        cdef str field
        condition_fields = ' AND '.join([f'{field} = ${i}' for i, field in enumerate(self._criteria.keys(), start=1)])
        records = await self._client.run_query(
            f'select {self._fields} from {self._model.__table_name__} where {condition_fields}',
            *self._criteria.values()
        )
        return [self._model(**record) for record in records]

    def filter(self, **criteria):
        new_criteria = self._criteria.copy()
        new_criteria.update(criteria)
        return QuerySet(self._model, new_criteria)

    async def get(self, **criteria):
        fields = []
        for i, key in enumerate(criteria.keys(), start=1):
            fields.append(f'{key} = ${i}')

        fields = ' AND '.join(fields)
        sql = f'select * from {self._model.__table_name__} where {fields}'
        records = await self._client.run_query(sql, *criteria.values())
        if records:
            return self._model(**records[0])

    async def all(self):
        records = await self._client.run_query(f'select * from {self._model.__table_name__}')
        result = []
        for record in records:
            result.append(self._model(**record))
        return result

    def only(self, *fields):
        return QuerySet(self._model, self._criteria, ', '.join(fields))
