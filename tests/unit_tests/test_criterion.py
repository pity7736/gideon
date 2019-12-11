from pytest import mark

from gideon.fields import CharField, IntegerField
from gideon.models import Model


string_values = (
    'hi',
    'world',
    1,
    2,
    3
)


@mark.parametrize('value', string_values)
def test_equal_string_comparison(value):
    class Test(Model):
        _name = CharField()

    criterion = Test.name == value

    assert criterion.get_sql() == f"name = $1"


def test_equal_two_values():
    class Test(Model):
        _name = CharField()
        _value = IntegerField()

    criterion = (Test.value == 1) & (Test.name == 'hi')

    assert criterion.get_sql() == f"value = $1 AND name = $2"
    assert criterion.values == (1, 'hi')
