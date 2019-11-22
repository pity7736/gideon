import asyncpg
from asyncpg.pool import Pool


class ConnectionPool:

    __slots__ = ('_pool', '_connection')

    def __init__(self, user: str, password: str, host: str, port, database):
        self._pool = _ConnectionPoolWrapper(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
        self._connection = None

    async def __aenter__(self):
        return await self.acquire()

    async def acquire(self):
        self._connection = await self._pool.acquire()
        return self._connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.release()

    async def release(self):
        await self._pool.release(self._connection)


class _ConnectionPoolWrapper:

    _instance = None
    _pool = None
    __slots__ = ('_user', '_password', '_host', '_port', '_database')

    def __new__(cls, user: str, password: str, host: str, port, database):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._user = user
            cls._instance._password = password
            cls._instance._host = host
            cls._instance._port = port
            cls._instance._database = database
        return cls._instance

    async def acquire(self):
        if self.__class__._pool is None:
            self.__class__._pool: Pool = await asyncpg.create_pool(
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port,
                database=self._database,
                min_size=5,
                max_size=20,
            )
        return await self._pool.acquire()

    async def release(self, connection):
        assert self._pool
        await self._pool.release(connection)
