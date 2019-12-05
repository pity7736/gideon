from pytest import raises

from gideon.fields import Field


def test_field_attributes():
    field = Field(name='test_name')

    assert field.name == 'test_name'


def test_rename_field():
    field = Field(name='test_name')
    with raises(ValueError):
        field.name = 'new name'
