from gideon.models.fields import Field


def test_field_attributes():
    field = Field(name='test_name')

    assert field.name == 'test_name'
