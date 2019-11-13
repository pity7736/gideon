import os

import asyncpg


cdef class QuerySet:

    def __init__(self, model, criteria=None):
        self._model = model
        self._criteria = criteria or {}

    def __await__(self):
        return self._run_query().__await__()

    async def _run_query(self):
        print('criteria', self._criteria)
        fields = []
        for i, field in enumerate(self._criteria.keys(), start=1):
            fields.append(f'{field} = ${i}')

        fields = ' AND '.join(fields)
        connection = await self._get_connection()
        records = await connection.fetch(f'select * from {self._model.__table_name__} where {fields}', *self._criteria.values())
        await connection.close()
        result = []
        for record in records:
            result.append(self._model(**record))
        return result

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
