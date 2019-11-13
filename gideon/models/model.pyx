import asyncpg
import os

from gideon.fields import ForeignKeyField
from gideon.fields.field cimport Field
from gideon.models.meta_model import MetaModel
from gideon.models.queryset import QuerySet


class Model(metaclass=MetaModel):

    def __init__(self, **kwargs):
        cdef str key
        cdef Field field
        for key, field in self._fields.items():
            value = kwargs.pop(key.replace('_', '', 1), None)
            if value and field.choices:
                value = field.choices(value)

            setattr(self, key, value)
            if isinstance(field, ForeignKeyField):
                setattr(self, f'{key}_id', kwargs.pop(f'{key}_id'.replace('_', '', 1), None))

    @classmethod
    def get(cls, **kwargs):
        return QuerySet(cls).get(**kwargs)

    async def save(self):
        fields = []
        values = []
        arguments = []
        i = 1
        for field in self._fields.values():
            field_name = field.name
            if field_name != 'id':
                if isinstance(field, ForeignKeyField):
                    instance = getattr(self, field_name)
                    field_name = f'{field_name}_id'
                    if instance:
                        setattr(self, field_name, instance.id)

                fields.append(field_name)
                values.append(f'${i}')
                arguments.append(field.to_db(getattr(self, field_name)))
                i += 1

        fields = ', '.join(fields)
        values = ', '.join(values)
        con = await self._get_connection()
        self._id = await con.fetchval(
            f'insert into {self.__table_name__}({fields}) values ({values}) RETURNING id'.replace("'", ''),
             *arguments
        )
        await con.close()

    @classmethod
    def filter(cls, **kwargs):
        return QuerySet(cls).filter(**kwargs)

    @classmethod
    async def all(cls):
        connection = await cls._get_connection()
        records = await connection.fetch(f'select * from {cls.__table_name__}')
        await connection.close()
        result = []
        for record in records:
            result.append(cls(**record))
        return result

    @staticmethod
    async def _get_connection():
        # TODO: refactor this. it should not be here
        return await asyncpg.connect(
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'],
            database=os.environ['DB_NAME']
        )
