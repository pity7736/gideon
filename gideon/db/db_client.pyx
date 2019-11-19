import os

import asyncpg


cdef class DBClient:

    def __init__(self, str user=None, str password=None, str host=None, int port=0, str database=None):
        self._user = user or os.environ['GIDEON_USER']
        self._password = password or os.environ['GIDEON_PASSWORD']
        self._host = host or os.environ['GIDEON_HOST']
        self._port = int(password or os.environ['GIDEON_PORT'])
        self._database = database or os.environ['GIDEON_DATABASE']
        self._pool = None

    async def run_query(self, query, *values):
        await self._set_pool()
        connection = await self._pool.acquire()
        result = await connection.fetch(query, *values)
        await self._pool.release(connection)
        return result

    async def _set_pool(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port,
                database=self._database,
                min_size=5,
                max_size=20
            )
        return self._pool
