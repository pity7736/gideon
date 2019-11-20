import os

from .connection_pool import ConnectionPool


cdef class DBClient:

    def __init__(self, str user=None, str password=None, str host=None, int port=0, str database=None):
        self._connection_data = {
            'user': user  or os.environ['GIDEON_USER'],
            'password': password or os.environ['GIDEON_PASSWORD'],
            'host': host or os.environ['GIDEON_HOST'],
            'port': int(port or os.environ['GIDEON_PORT']),
            'database': database or os.environ['GIDEON_DATABASE']
        }

    async def run_query(self, query, *values):
        async with ConnectionPool(**self._connection_data) as connection:
            return await connection.fetch(query, *values)

    async def run_insert(self, query, *values):
        async with ConnectionPool(**self._connection_data) as connection:
            return await connection.fetchval(query, *values)
