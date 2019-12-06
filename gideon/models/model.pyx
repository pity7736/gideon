from gideon.db.db_client cimport DBClient

from gideon.exceptions import NonExistsField
from gideon.fields.field cimport Field
from gideon.fields.foreign_key_field cimport ForeignKeyField
from gideon.models.meta_model import MetaModel
from gideon.models.queryset cimport QuerySet


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

    def __repr__(self):
        return f'<{self}>'

    def __str__(self):
        if self.id:
            return f'{self.__class__.__name__}: {self.id}'
        return self.__class__.__name__

    def __eq__(self, other):
        if type(self) is type(other) and self.id and other.id:
            return self.id == other.id
        return False

    @classmethod
    def get(cls, **kwargs):
        return QuerySet(cls).get(**kwargs)

    @classmethod
    def filter(cls, **kwargs):
        return QuerySet(cls).filter(**kwargs)

    @classmethod
    def all(cls):
        return QuerySet(cls).all()

    @classmethod
    async def create(cls, **kwargs):
        obj = cls(**kwargs)
        await obj.save()
        return obj

    async def save(self, update_fields=()):
        if self._id is None and not update_fields:
            return await self._insert()
        return await self._update(update_fields)

    async def _insert(self):
        db_client = DBClient()
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
        self._id = await db_client.run_insert(
            f'insert into {self.__table_name__}({fields}) values ({values}) RETURNING id'.replace("'", ''),
             *arguments
        )

    async def _update(self, update_fields):
        db_client = DBClient()
        values = []
        fields = []
        i = 1
        cdef str field_name
        cdef Field field
        if update_fields:
            for field_name in update_fields:
                field = self._fields.get(f'_{field_name}')
                if field is None:
                    raise NonExistsField(f'field {field_name} does not exists!')

                if isinstance(field, ForeignKeyField):
                    field_name = f'{field_name}_id'

                fields.append(f'{field_name} = ${i}')
                values.append(field.to_db(getattr(self, field_name)))
                i += 1
        else:
            for field in self._fields.values():
                field_name = field.name
                if field_name != 'id':
                    if isinstance(field, ForeignKeyField):
                        field_name = f'{field_name}_id'

                    fields.append(f'{field_name} = ${i}')
                    values.append(field.to_db(getattr(self, field_name)))
                    i += 1

        fields = ', '.join(fields)
        values.append(self._id)
        sql = f'UPDATE {self.__table_name__} SET {fields} WHERE id = ${i}'
        await db_client.run_query(sql, *values)
