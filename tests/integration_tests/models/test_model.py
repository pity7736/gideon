from pytest import mark, raises

from tests.factories import CategoryFactory
from tests.models import Category


@mark.asyncio
async def test_save(create_db, db_transaction, connection):
    category = Category(name='test category', description='test description')
    await category.save()

    record = await connection.fetchrow(
        'select * from categories where id = $1',
        category.id
    )

    assert category.id == record['id']
    assert category.name == record['name']
    assert category.description == record['description']


@mark.asyncio
async def test_get_by_id(create_db, db_transaction, category):
    record = await Category.get(id=category.id)

    assert record != category
    assert record.id == category.id
    assert record.name == category.name
    assert record.description == category.description


@mark.asyncio
async def test_get_by_name(create_db, db_transaction, category):
    record = await Category.get(name=category.name)

    assert record != category
    assert record.id == category.id
    assert record.name == category.name
    assert record.description == category.description


@mark.asyncio
async def test_get_by_id_and_name(create_db, db_transaction, category):
    record = await Category.get(id=category.id, name=category.name)

    assert record != category
    assert record.id == category.id
    assert record.name == category.name
    assert record.description == category.description


@mark.asyncio
async def test_filter_by_name_with_not_existing_categories(create_db, db_transaction):
    categories = await Category.filter(name='test name')
    assert categories == []


@mark.asyncio
async def test_filter_by_id(create_db, db_transaction):
    fixture = CategoryFactory(name='qwerty')
    await fixture.save()
    categories = await Category.filter(id=fixture.id)
    record = categories[0]

    assert record.id == fixture.id
    assert record.name == 'qwerty'


@mark.asyncio
async def test_filter_by_description(create_db, db_transaction, category):
    categories = await Category.filter(description='test description')
    record = categories[0]

    assert record.id == category.id
    assert record.description == 'test description'


@mark.asyncio
async def test_filter_without_params():
    with raises(AssertionError):
        await Category.filter()