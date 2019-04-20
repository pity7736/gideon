from pytest import raises, mark

from gideon.exceptions import NonExistsField, PrivateField
from gideon.fields import Field
from gideon.models.model import Model

from tests.models import Category

table_names = (
    ('test_model', 'test_model'),
    ('test model', 'test_model'),
    ('TEST_MODEL', 'test_model'),
)


@mark.parametrize('table_name, expected_table_name', table_names)
def test_model_table_name(table_name, expected_table_name):
    class Test(Model):
        __table_name__ = table_name

    assert Test.__table_name__ == expected_table_name


def test_model_name():
    class CreditCard(Model):
        pass

    assert CreditCard.__table_name__ == 'credit_card'


def test_fields_must_be_private():
    with raises(PrivateField):
        class Example(Model):
            name = Field()


def test_fields_without_data():
    category = Category()

    assert category.id is None
    assert category.name is None
    assert category.description is None


def test_set_value_to_field():
    category = Category()
    category.name = 'hola'

    assert category.name == 'hola'


def test_fields_with_data_in_constructor():
    category = Category(name='test', description='description')

    assert category.id is None
    assert category.name == 'test'
    assert category.description == 'description'


def test_wrong_fields():
    with raises(NonExistsField):
        Category(name='test', non_existent_field='fail')
