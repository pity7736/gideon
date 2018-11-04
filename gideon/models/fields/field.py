import datetime


class Field:

    __slots__ = ('name',)

    def __init__(self, name=''):
        self.name = name

    def to_db(self, value):
        return value


class DateField(Field):

    def to_db(self, value):
        if isinstance(value, datetime.date) or value is None:
            return value

        if isinstance(value, str):
            return datetime.datetime.strptime(value, '%Y-%m-%d').date()
