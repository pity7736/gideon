from pytest import raises

from gideon.models.fields import Field
from gideon.models.model import Model


def test_table_name_attribute():
    with raises(AssertionError):
        class M(Model):
            pass


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
