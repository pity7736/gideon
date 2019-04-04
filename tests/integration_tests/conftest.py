import asyncpg
import os

from pytest import fixture


@fixture
async def connection():
    con = await asyncpg.connect(
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT'],
        database=os.environ['DB_NAME']
    )
    yield con
    await con.close()


@fixture
async def db_transaction(connection):
    # TODO: refactor this for a better solution
    yield
    await connection.execute('TRUNCATE categories, movements_tags, tags, movements, test_model;')
    await connection.close()
