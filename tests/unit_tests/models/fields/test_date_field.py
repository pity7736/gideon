import datetime

from pytest import mark

from gideon.models.fields import DateField


to_db_values = (
    ('2018-10-20', datetime.date(2018, 10, 20)),
    (None, None),
    (datetime.date.today(), datetime.date.today())
)


@mark.parametrize('value, expected_value', to_db_values)
def test_to_db(value, expected_value):
    date_field = DateField(name='test')

    assert date_field.to_db(value) == expected_value
