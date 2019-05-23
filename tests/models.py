from gideon.fields import Field, ForeignKeyField, DateField
from gideon.models import Model


class Category(Model):
    __table_name__ = 'categories'
    _name = Field(name='name')
    _description = Field(name='description')


class Movement(Model):
    __table_name__ = 'movements'
    _type = Field(name='type')
    _date = DateField(name='date')
    _value = Field(name='value')
    _note = Field(name='note')
    _category = ForeignKeyField(name='category', to=Category)
