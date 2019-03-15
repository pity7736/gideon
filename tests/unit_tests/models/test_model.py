from pytest import raises, mark

from gideon.models.fields import Field
from gideon.models.model import Model


def test_model_without_table_name():
    class M(Model):
        pass

    assert M.__table_name__ == 'm'


table_names = (
    ('test_model', 'test_model'),
    ('test model', 'test_model'),
    ('TEST_MODEL', 'test_model'),
)


@mark.parametrize('table_name, expected_table_name', table_names)
def test_mode_table_name(table_name, expected_table_name):
    class M(Model):
        __table_name__ = table_name

    assert M.__table_name__ == expected_table_name


def test_model_name():
    class CreditCard(Model):
        pass

    assert CreditCard.__table_name__ == 'credit_card'


def test_fields_must_be_private():
    with raises(ValueError):
        class Example(Model):
            name = Field()


class M(Model):
    __table_name__ = 'Model'
    _id = Field(name='id')
    _name = Field(name='name')
    _desc = Field(name='description')


def test_fields_without_data():
    m = M()

    assert m.id is None
    assert m.name is None
    assert m.desc is None


def test_set_value_to_field():
    m = M()
    m.name = 'hola'

    assert m.name == 'hola'


def test_fields_with_data_in_constructor():
    m = M(name='test', desc='description')

    assert m.id is None
    assert m.name == 'test'
    assert m.desc == 'description'


def test_wrong_fields():
    with raises(TypeError):
        M(name='test', non_existent_field='fail')
