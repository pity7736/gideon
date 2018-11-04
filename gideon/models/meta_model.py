from immutables import Map

from gideon.models.fields import Field


class MetaModel(type):

    def __new__(mcs, name, bases, namespace, **kwargs):
        assert '__table_name__' in namespace, 'All model must have a __table_name__ attribute'
        fields = Map()
        for attr, value in namespace.items():
            if isinstance(value, Field):
                fields = fields.set(attr, value)

        namespace['_fields'] = fields
        return super().__new__(mcs, name, bases, namespace)
