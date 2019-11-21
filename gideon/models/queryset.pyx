from gideon.db.db_client cimport DBClient


cdef class QuerySet:
    _client = DBClient()

    def __init__(self, model):
        self._model = model
        self._criteria = {}
        self._fields = '*'
        self._get = False

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
        records = [self._model(**record) for record in records]
        if self._get is True and records:
            records = records[0]
        return records

    def filter(self, **criteria):
        queryset = QuerySet(self._model)
        queryset._criteria = self._get_new_criteria(**criteria)
        queryset._get = self._get
        queryset._fields = self._fields
        return queryset

    def get(self, **criteria):
        queryset = QuerySet(self._model)
        queryset._criteria = self._get_new_criteria(**criteria)
        queryset._get = True
        queryset._fields = self._fields
        return queryset

    def _get_new_criteria(self, **criteria):
        new_criteria = self._criteria.copy()
        new_criteria.update(**criteria)
        return new_criteria

    async def all(self):
        records = await self._client.run_query(f'select * from {self._model.__table_name__}')
        result = []
        for record in records:
            result.append(self._model(**record))
        return result

    def only(self, *fields):
        queryset = QuerySet(self._model)
        queryset._criteria = self._criteria
        queryset._fields = ', '.join(fields)
        return queryset
