from pytest import mark

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
async def test_update_with_save(create_db, db_transaction, category_fixture):
    cat = await Category.get(name='test name')
    cat.name = 'test new name'
    await cat.save()

    c1 = await Category.get(name='test new name')
    c2 = await Category.get(name='test name')

    assert c1.name == 'test new name'
    assert c2 == []


@mark.asyncio
async def test_update_save_with_foreign_key(create_db, db_transaction, movement_fixture):
    new_category = await Category.create(name='test new category', description='test new description')
    movement_fixture.category = new_category
    await movement_fixture.save()

    m = await Movement.get(id=movement_fixture.id)

    assert m.category_id == new_category.id


@mark.asyncio
async def test_update_save_with_foreign_key_id(create_db, db_transaction, movement_fixture):
    new_category = await Category.create(name='test new category', description='test new description')
    movement_fixture.category_id = new_category.id
    await movement_fixture.save()

    m = await Movement.get(id=movement_fixture.id)

    assert m.category_id == new_category.id


@mark.asyncio
async def test_with_choices(create_db, db_transaction, connection, movement_fixture):
    record = await connection.fetchrow(
        'select * from movements where id = $1',
        movement_fixture.id
    )

    assert record['type'] == 'expense'
    assert movement_fixture.type.value == record['type']


@mark.asyncio
async def test_get_by_id(create_db, db_transaction, category_fixture):
    record = await Category.get(id=category_fixture.id)

    assert record != category_fixture
    assert record.id == category_fixture.id
    assert record.name == category_fixture.name
    assert record.description == category_fixture.description


@mark.asyncio
async def test_get_by_name(create_db, db_transaction, category_fixture):
    record = await Category.get(name=category_fixture.name)

    assert record != category_fixture
    assert record.id == category_fixture.id
    assert record.name == category_fixture.name
    assert record.description == category_fixture.description


@mark.asyncio
async def test_get_by_id_and_name(create_db, db_transaction, category_fixture):
    record = await Category.get(id=category_fixture.id, name=category_fixture.name)

    assert record != category_fixture
    assert record.id == category_fixture.id
    assert record.name == category_fixture.name
    assert record.description == category_fixture.description


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
async def test_filter_by_description(create_db, db_transaction, category_fixture):
    categories = await Category.filter(description='test description')
    record = categories[0]

    assert record.id == category_fixture.id
    assert record.description == 'test description'


@mark.asyncio
async def test_all(create_db, db_transaction):
    categories = CategoryFactory.build_batch(5)
    for category in categories:
        await category.save()

    assert len(await Category.all()) == 5


@mark.asyncio
async def test_get_with_foreign_key(create_db, db_transaction, movement_fixture):
    movement = await Movement.get(id=movement_fixture.id)

    assert movement.id == movement_fixture.id
    assert movement.category is None
    assert movement.category_id == movement_fixture.category.id


@mark.asyncio
async def test_get_with_foreign_key_id(create_db, db_transaction, movement_fixture):
    movement = await Movement.get(id=movement_fixture.id)

    assert movement.id == movement_fixture.id
    assert movement.category is None
    assert movement.category_id == movement_fixture.category.id


@mark.asyncio
async def test_get_with_choices(create_db, db_transaction, connection, movement_fixture):
    movement = await Movement.get(id=movement_fixture.id)

    assert movement_fixture.type.value == 'expense'
    assert movement.type == movement_fixture.type


@mark.asyncio
async def test_filter_by_name_and_description_with_two_different_filter_calls(create_db, db_transaction,
                                                                              category_fixture):
    cat = CategoryFactory.build(description='another description')
    await cat.save()
    queryset = Category.filter(description='test description')
    queryset = queryset.filter(name='test name')
    categories = await queryset
    record = categories[0]

    assert len(categories) == 1
    assert record.id == category_fixture.id
    assert record.description == 'test description'


@mark.asyncio
async def test_only_fields(create_db, db_transaction, category_fixture):
    categories = await Category.filter(name='test name').only('name')
    category = categories[0]

    assert len(categories) == 1
    assert category.id == category.id
    assert category.name == 'test name'
    assert category.description is None


@mark.asyncio
async def test_create(create_db, db_transaction, movement_fixture):
    movement = await Movement.get(id=movement_fixture.id)

    assert movement.id == movement_fixture.id
    assert movement.category is None
    assert movement.category_id == movement_fixture.category.id


@mark.asyncio
async def test_filter_after_get(create_db, db_transaction, category_fixture):
    await CategoryFactory.build().save()
    await CategoryFactory.build(description='another description').save()
    queryset = Category.get(description='test description')
    queryset = queryset.filter(name='test name')
    record = await queryset

    assert record.name == 'test name'
    assert record.description == 'test description'
