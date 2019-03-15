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


def test_model_name_with_two_words():
    class CreditCard(Model):
        pass

    assert CreditCard.__table_name__ == 'credit_card'


def test_mode_name_with_three_words():
    class HTTPResponseCode(Model):
        pass

    assert HTTPResponseCode.__table_name__ == 'http_response_code'


class M(Model):
    __table_name__ = 'Model'
    id = Field(name='id')
    name = Field(name='name')
    desc = Field(name='description')


def test_fields_without_data():
    m = M()

    assert m.id is None
    assert m.name is None
    assert m.desc is None


def test_fields_with_data_in_constructor():
    m = M(name='test', desc='description')

    assert m.id is None
    assert m.name == 'test'
    assert m.desc == 'description'


def test_wrong_fields():
    with raises(TypeError):
        M(name='test', non_existent_field='fail')
