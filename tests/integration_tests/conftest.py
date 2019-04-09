import asyncpg
import os
import subprocess

from pytest import fixture

from tests.factories import CategoryFactory


@fixture(scope='session')
def create_db():
    print('creating database...')
    # the password is in .pgpass file
    subprocess.call(['psql', '-U', os.environ['DB_USER'], '-h', os.environ['DB_HOST'], '-f', '../db.sql'])


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
    await connection.execute('TRUNCATE categories, movements_tags, tags, movements;')
    await connection.close()


@fixture
async def category():
    cat = CategoryFactory()
    await cat.save()
    return cat
