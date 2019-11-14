import os

import asyncpg


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
        connection = await self._get_connection()
        records = await connection.fetch(
            f'select {self._fields} from {self._model.__table_name__} where {condition_fields}',
            *self._criteria.values()
        )
        await connection.close()
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
        con = await self._get_connection()
        record = await con.fetchrow(sql, *criteria.values())
        await con.close()
        if record:
            return self._model(**record)

    async def all(self):
        connection = await self._get_connection()
        records = await connection.fetch(f'select * from {self._model.__table_name__}')
        await connection.close()
        result = []
        for record in records:
            result.append(self._model(**record))
        return result

    def only(self, *fields):
        return QuerySet(self._model, self._criteria, ', '.join(fields))

    @staticmethod
    async def _get_connection():
        # TODO: refactor this. it should not be here
        return await asyncpg.connect(
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'],
            database=os.environ['DB_NAME']
        )
