import asyncpg
import os

from gideon.fields.field cimport Field
from gideon.exceptions import NonExistsField
from gideon.fields import ForeignKeyField
from gideon.models.meta_model import MetaModel


class Model(metaclass=MetaModel):

    def __init__(self, **kwargs):
        cdef str key
        cdef Field field
        for key, field in self._fields.items():
            value = kwargs.get(key)
            setattr(self, key, value)

        for key, value in kwargs.items():
            if f'_{key}' not in self._fields.keys() and key not in vars(self):
                raise NonExistsField(f'Invalid field: {key} is not a field of {self.__class__}')
            setattr(self, key, value)

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
        sql = f'insert into {self.__table_name__}({fields}) values ({values}) RETURNING id'.replace("'", '')
        self.id = await con.fetchval(sql, *arguments)
        await con.close()

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
