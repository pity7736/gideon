import re

from immutables import Map

from gideon.models.fields import Field


class MetaModel(type):

    def __new__(mcs, name, bases, namespace, **kwargs):
        table_name = namespace.get('__table_name__', name)
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', table_name)
        namespace['__table_name__'] = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower().replace(' ', '_')
        fields = Map()
        for attr, value in namespace.items():
            if isinstance(value, Field):
                fields = fields.set(attr, value)

        namespace['_fields'] = fields
        return super().__new__(mcs, name, bases, namespace)
