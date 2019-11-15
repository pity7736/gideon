import os

import asyncpg


cdef class ConnectionPool:

    def __init__(self):
        self._pool = None

    async def acquire(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD'],
                host=os.environ['DB_HOST'],
                port=int(os.environ['DB_PORT']),
                database=os.environ['DB_NAME'],
                min_size=5,
                max_size=20,
            )
        return await self._pool.acquire()

    async def release(self, connection):
        assert self._pool
        await self._pool.release(connection)
