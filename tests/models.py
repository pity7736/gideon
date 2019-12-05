from enum import Enum

from gideon.fields import ForeignKeyField, DateField, IntegerField, CharField
from gideon.models import Model


class Category(Model):
    __table_name__ = 'categories'
    _name = CharField()
    _description = CharField()


class MovementType(Enum):
    EXPENSE = 'expense'
    INCOME = 'income'


class Movement(Model):
    __table_name__ = 'movements'
    _type = CharField(choices=MovementType)
    _date = DateField()
    _value = IntegerField()
    _note = CharField()
    _category = ForeignKeyField(to=Category)
