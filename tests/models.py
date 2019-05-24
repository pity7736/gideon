from gideon.fields import ForeignKeyField, DateField, IntegerField, CharField
from gideon.models import Model


class Category(Model):
    __table_name__ = 'categories'
    _name = CharField(name='name')
    _description = CharField(name='description')


class Movement(Model):
    __table_name__ = 'movements'
    _type = CharField(name='type')
    _date = DateField(name='date')
    _value = IntegerField(name='value')
    _note = CharField(name='note')
    _category = ForeignKeyField(name='category', to=Category)
