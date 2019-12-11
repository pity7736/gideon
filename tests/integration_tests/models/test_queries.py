from pytest import mark

from tests.factories import CategoryFactory
from tests.models import Category


@mark.asyncio
async def test_criteria(db_transaction, category_fixture):
    c = CategoryFactory.build(name='qwerty')
    await c.save()
    print(Category.name, 'asdasd')
    categories = await Category.filter(Category.name == 'test name')
    category = categories[0]

    assert len(categories) == 1
    assert category == category_fixture
