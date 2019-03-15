from pytest import mark

from gideon.utils.strings import camel_case_to_snake_case


strings = (
    ('Hello', 'hello'),
    ('CamelCase', 'camel_case'),
    ('HTTPResponseCode', 'http_response_code'),
    ('camelCase', 'camel_case')
)


@mark.parametrize('string, expected_string', strings)
def test_camel_case_to_snake_case(string, expected_string):
    result = camel_case_to_snake_case(string)
    assert result == expected_string
