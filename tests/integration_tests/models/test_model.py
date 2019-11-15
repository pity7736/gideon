from pytest import mark, raises

from tests.factories import CategoryFactory
from tests.models import Category, Movement, MovementType


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
async def test_with_choices(create_db, db_transaction, connection, category):
    mov = Movement(type=MovementType.EXPENSE, date='2019-04-20', value=10000, note='test', category=category)
    await mov.save()

    record = await connection.fetchrow(
        'select * from movements where id = $1',
        mov.id
    )

    assert record['type'] == 'expense'
    assert mov.type.value == record['type']


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


@mark.asyncio
async def test_all(create_db, db_transaction):
    categories = CategoryFactory.build_batch(5)
    for category in categories:
        await category.save()

    assert len(await Category.all()) == 5


@mark.asyncio
async def test_get_with_foreign_key(create_db, db_transaction, category):
    mov = Movement(type=MovementType.EXPENSE, date='2019-04-20', value=10000, note='test', category=category)
    await mov.save()
    movement = await Movement.get(id=mov.id)

    assert movement.id == mov.id
    assert movement.category is None
    assert movement.category_id == category.id


@mark.asyncio
async def test_get_with_foreign_key_id(create_db, db_transaction, category):
    mov = Movement(type=MovementType.EXPENSE, date='2019-04-20', value=10000, note='test', category_id=category.id)
    await mov.save()
    movement = await Movement.get(id=mov.id)

    assert movement.id == mov.id
    assert movement.category is None
    assert movement.category_id == category.id


@mark.asyncio
async def test_get_with_choices(create_db, db_transaction, connection, category):
    mov = Movement(type=MovementType.EXPENSE, date='2019-04-20', value=10000, note='test', category=category)
    await mov.save()

    movement = await Movement.get(id=mov.id)

    assert mov.type.value == 'expense'
    assert movement.type == mov.type


@mark.asyncio
async def test_filter_by_name_and_description_with_two_different_filter_calls(create_db, db_transaction, category):
    cat = CategoryFactory.build(description='another description')
    await cat.save()
    queryset = Category.filter(description='test description')
    queryset = queryset.filter(name='test name')
    categories = await queryset
    record = categories[0]

    assert len(categories) == 1
    assert record.id == category.id
    assert record.description == 'test description'


@mark.asyncio
async def test_only_fields(create_db, db_transaction, category):
    categories = await Category.filter(name='test name').only('name')
    category = categories[0]

    assert len(categories) == 1
    assert category.id == category.id
    assert category.name == 'test name'
    assert category.description is None
