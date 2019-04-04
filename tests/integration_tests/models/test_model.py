import os
import subprocess

from pytest import mark

from tests.models import Category


@mark.asyncio
async def test_save():
    # the password is in .pgpass file
    subprocess.call(['psql', '-U', os.environ['DB_USER'], '-h', os.environ['DB_HOST'], '-f', '../db.sql'])
    category = Category(name='test category', description='test description')
    assert category.id is None
    await category.save()
    assert category.id


@mark.asyncio
async def test_get():
    subprocess.call(['psql', '-U', os.environ['DB_USER'], '-h', os.environ['DB_HOST'], '-f', '../db.sql'])
    category = Category(name='test get category', description='test description')
    await category.save()

    category2 = await Category.get(id=category.id)

    assert category.id == category2.id
    assert category.name == category2.name
    assert category.description == category2.description
