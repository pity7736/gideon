from immutables import Map

from gideon.exceptions import PrivateField
from gideon.fields import Field, ForeignKeyField
from gideon.utils.strings import camel_case_to_snake_case


def create_property_field(field_name):
    return lambda self: getattr(self, field_name)


def create_set_property_field(field_name):
    return lambda self, value: setattr(self, field_name, value)


class MetaModel(type):

    def __new__(mcs, name, bases, namespace, **kwargs):
        table_name = namespace.get('__table_name__', name)
        namespace['__table_name__'] = camel_case_to_snake_case(table_name).replace(' ', '_')
        fields = Map()
        property_fields = {}
        for attr, value in namespace.items():
            if isinstance(value, Field):
                if not attr.startswith('_'):
                    raise PrivateField('Fields name must be private')

                fields = fields.set(attr, value)
                property_fields[attr.replace('_', '', 1)] = property(
                    create_property_field(attr),
                    create_set_property_field(attr)
                )
                if isinstance(value, ForeignKeyField):
                    property_fields[f'{attr}_id'] = None
                    property_fields[f'{attr.replace("_", "", 1)}_id'] = property(
                        create_property_field(attr),
                        create_set_property_field(attr)
                    )

        namespace['_fields'] = fields
        namespace.update(property_fields)
        return super().__new__(mcs, name, bases, namespace)
