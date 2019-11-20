from gideon.db.db_client cimport DBClient
from gideon.fields import ForeignKeyField
from gideon.fields.field cimport Field
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

    @classmethod
    def get(cls, **kwargs):
        return QuerySet(cls).get(**kwargs)

    @classmethod
    def filter(cls, **kwargs):
        return QuerySet(cls).filter(**kwargs)

    @classmethod
    def all(cls):
        return QuerySet(cls).all()

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
        db_client = DBClient()
        self._id = await db_client.run_insert(
            f'insert into {self.__table_name__}({fields}) values ({values}) RETURNING id'.replace("'", ''),
             *arguments
        )
