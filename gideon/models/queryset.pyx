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
        sql = f'select {self._fields} from {self._model.__table_name__}'
        if condition_fields:
            sql += f' where {condition_fields}'

        records = [self._model(**record) for record in await self._client.run_query(sql, *self._criteria.values())]
        if self._get is True and records:
            records = records[0]
        return records

    def all(self):
        return self.filter()

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

    def only(self, *fields):
        queryset = QuerySet(self._model)
        queryset._criteria = self._criteria
        queryset._fields = ', '.join(fields)
        return queryset
