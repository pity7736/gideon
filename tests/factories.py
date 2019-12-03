import factory

from tests.models import Category


class CategoryFactory(factory.Factory):
    name = 'test name'
    description = 'test description'

    class Meta:
        model = Category
