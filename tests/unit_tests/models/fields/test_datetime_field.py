import datetime

from pytest import mark

from gideon.fields import DateTimeField


now = datetime.datetime.now()
to_db_values = (
    (now, now),
    (None, None),
    ('2019-06-05T19:55:00', datetime.datetime(2019, 6, 5, 19, 55)),
    ('2019-06-05', datetime.datetime(2019, 6, 5))
)


@mark.parametrize('value, expected_value', to_db_values)
def test_to_db(value, expected_value):
    datetime_field = DateTimeField(name='test')

    assert datetime_field.to_db(value) == expected_value
