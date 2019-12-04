import asyncio

import os
import subprocess

from pytest import fixture

from gideon.db.connection_pool import ConnectionPool
from tests.factories import CategoryFactory
from tests.models import Movement, MovementType


@fixture(scope='session')
def create_db():
    print('creating database...')
    # the password is in .pgpass file
    subprocess.call(['psql', '-U', os.environ['GIDEON_USER'], '-h', os.environ['GIDEON_HOST'], '-f',
                    f'{os.path.dirname(__file__)}/db.sql'])


@fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@fixture
def connection_pool(create_db):
    return ConnectionPool(
        user=os.environ['GIDEON_USER'],
        password=os.environ['GIDEON_PASSWORD'],
        host=os.environ['GIDEON_HOST'],
        port=os.environ['GIDEON_PORT'],
        database=os.environ['GIDEON_DATABASE']
    )


@fixture
async def connection(connection_pool):
    yield await connection_pool.acquire()
    await connection_pool.release()


@fixture
async def db_transaction(connection):
    # TODO: refactor this for a better solution
    yield
    await connection.execute('TRUNCATE categories, movements_tags, tags, movements;')


@fixture
async def category_fixture(db_transaction):
    category = CategoryFactory.build()
    await category.save()
    return category


@fixture
async def movement_fixture(category_fixture):
    movement = Movement(type=MovementType.EXPENSE, date='2019-04-20', value=10000, note='test',
                        category=category_fixture)
    await movement.save()
    return movement
