from enum import Enum

from pytest import raises, mark

from gideon.exceptions import NonExistsField, PrivateField, InvalidChoice
from gideon.fields import CharField, IntegerField, ForeignKeyField
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
            name = CharField()


def test_fields_without_data():
    category = Category()

    assert category.id is None
    assert category.name is None
    assert category.description is None


def test_set_value_to_field():
    category = Category()
    category.name = 'hello'

    assert category.name == 'hello'


def test_fields_with_data_in_constructor():
    category = Category(name='test', description='description')

    assert category.id is None
    assert category.name == 'test'
    assert category.description == 'description'


@mark.skip(reason='Do we really need this validation?')
def test_wrong_fields():
    with raises(NonExistsField):
        Category(name='test', non_existent_field='fail')


def test_annotations():
    class TestAnnotation(Model):
        _name = CharField(name='name')
        _value = IntegerField(name='value')
        _test = CharField(name='test')
        _category = ForeignKeyField(to=Category, name='category')

    assert TestAnnotation.__annotations__ == {
        'id': int,
        'name': str,
        'value': int,
        'test': str,
        'category': Category,
        'category_id': int
    }


def test_read_only_field():
    class ReadOnly(Model):
        _name = CharField(name='name')
        _immutable = IntegerField(name='immutable', read_only=True)

    read = ReadOnly()

    read.name = 'test'
    with raises(AttributeError):
        read.immutable = 'test'


def test_foreign_key_cannot_be_read_only():
    with raises(AssertionError):
        class ForeignReadOnly(Model):
            _name = CharField(name='name')
            _category = ForeignKeyField(to=Category, name='category', read_only=True)


def test_getter():
    class TestModel(Model):
        _name = CharField(name='name')

    test = TestModel(name='qwerty')

    assert test.name == 'qwerty'
    assert test.get_name() == 'qwerty'


def test_setter():
    class TestModel(Model):
        _name = CharField(name='name')

    test = TestModel()
    test.set_name('qwerty')

    assert test.get_name() == 'qwerty'


def test_setter_with_foreign_field():
    class Model1(Model):
        _name = CharField(name='name')

    class Model2(Model):
        _model1 = ForeignKeyField(Model)

    instance1 = Model1()
    instance2 = Model2()
    instance2.model1 = instance1

    assert instance2.model1 == instance1


def test_override_setter():
    class TestModel(Model):
        _name = CharField(name='name')
        _password = CharField(name='password')

        def set_password(self, raw_password):
            self.name = raw_password
            self._password = raw_password

    test = TestModel()
    test.set_password('hello')
    assert test.name == 'hello'
    assert test.password == 'hello'
    test.password = 'world'
    assert test.name == 'world'
    assert test.password == 'world'


def test_override_getter():
    class TestModel(Model):
        _name = CharField(name='name')
        _password = CharField(name='password')

        def get_password(self):
            return f'{self.name} - {self._password}'

    test = TestModel()
    test.name = 'name'
    test.password = 'password'
    assert test.get_password() == 'name - password'
    assert test.password == 'name - password'


def test_choices():
    class Choices(Enum):
        VALUE1 = '1'
        VALUE2 = '2'

    class TestModel(Model):
        _test = CharField(choices=Choices)

    instance = TestModel(test=Choices.VALUE1)

    assert instance.test == Choices.VALUE1


def test_enum_type_in_choices():
    choices = (
        ('value1', '1'),
        ('value2', '2')
    )

    with raises(ValueError):
        class TestModel(Model):
            _test = CharField(choices=choices)


def test_set_invalid_choice():
    class Choices(Enum):
        VALUE1 = '1'
        VALUE2 = '2'

    class TestModel(Model):
        _test = CharField(choices=Choices)

    test_instance = TestModel()
    with raises(InvalidChoice):
        test_instance.test = 'invalid value'


def test_field_auto_name():
    class TestModel(Model):
        _value = CharField()

    assert TestModel._value.name == 'value'
