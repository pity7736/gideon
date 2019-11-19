import os

import asyncpg


cdef class ConnectionPool:

    cdef _pool

    def __init__(self):
        self._pool = None

    async def acquire(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                user=os.environ['GIDEON_USER'],
                password=os.environ['GIDEON_PASSWORD'],
                host=os.environ['GIDEON_HOST'],
                port=int(os.environ['GIDEON_PORT']),
                database=os.environ['GIDEON_DATABASE'],
                min_size=5,
                max_size=20,
            )
        return await self._pool.acquire()

    async def release(self, connection):
        assert self._pool
        await self._pool.release(connection)
