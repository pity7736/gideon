from immutables import Map

from gideon.exceptions import PrivateField
from gideon.fields import Field, ForeignKeyField, IntegerField
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
        if '_id' not in namespace:
            namespace['_id'] = IntegerField(name='id')

        annotations = {}
        for attr, value in namespace.items():
            if isinstance(value, Field):
                if not attr.startswith('_'):
                    raise PrivateField('Fields name must be private')

                fields = fields.set(attr, value)
                property_name = attr.replace('_', '', 1)
                property_fields[property_name] = property(
                    create_property_field(attr),
                    create_set_property_field(attr)
                )
                annotations[property_name] = value.internal_type
                if isinstance(value, ForeignKeyField):
                    property_foreign_name = f'{property_name}_id'
                    property_fields[property_foreign_name] = property(
                        create_property_field(f'{attr}_id'),
                        create_set_property_field(f'{attr}_id')
                    )
                    annotations[property_name] = value.to
                    annotations[property_foreign_name] = value.internal_type

        namespace['_fields'] = fields
        namespace.update(property_fields)
        model = super().__new__(mcs, name, bases, namespace)
        model.__annotations__ = annotations
        return model
