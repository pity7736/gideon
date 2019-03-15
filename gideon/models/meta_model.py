from immutables import Map

from gideon.models.fields import Field
from gideon.utils.strings import camel_case_to_snake_case


class MetaModel(type):

    def __new__(mcs, name, bases, namespace, **kwargs):
        table_name = namespace.get('__table_name__', name)
        namespace['__table_name__'] = camel_case_to_snake_case(table_name).replace(' ', '_')
        fields = Map()
        for attr, value in namespace.items():
            if isinstance(value, Field):
                fields = fields.set(attr, value)

        namespace['_fields'] = fields
        return super().__new__(mcs, name, bases, namespace)
