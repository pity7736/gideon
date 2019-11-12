from immutables import Map

from gideon.exceptions import PrivateField
from gideon.fields import Field, ForeignKeyField, IntegerField
from gideon.utils.strings import camel_case_to_snake_case


def create_getter(field_name):
    return lambda self: getattr(self, field_name)


def create_setter(name, field=None):
    def setter(self, value):
        if field:
            value = field.to_python(value)
        setattr(self, name, value)
    return setter


class MetaModel(type):

    def __new__(mcs, name, bases, namespace, **kwargs):
        table_name = namespace.get('__table_name__', name)
        namespace['__table_name__'] = camel_case_to_snake_case(table_name).replace(' ', '_')
        fields = Map()
        property_fields = {}
        MetaModel._set_id(namespace)
        annotations = {}
        for attr, value in namespace.items():
            if isinstance(value, Field):
                if not attr.startswith('_'):
                    raise PrivateField('Fields name must be private')

                fields = fields.set(attr, value)
                property_name = attr.replace('_', '', 1)
                property_fields[property_name] = MetaModel._resolve_getters_and_setters(
                    attr,
                    namespace,
                    property_fields,
                    value
                )
                annotations[property_name] = value.internal_type
                MetaModel._set_foreignkey_field(annotations, attr, property_fields, property_name, value)

        namespace['_fields'] = fields
        namespace.update(property_fields)
        namespace['__annotations__'] = annotations
        return super().__new__(mcs, name, bases, namespace)

    @staticmethod
    def _set_id(namespace):
        if '_id' not in namespace:
            namespace['_id'] = IntegerField(name='id')

    @staticmethod
    def _resolve_getters_and_setters(attr, namespace, property_fields, field):
        getter_name = f'get{attr}'
        getter = namespace.get(getter_name) or create_getter(attr)
        property_fields[getter_name] = getter
        setter = None
        if field.read_only is False:
            setter_name = f'set{attr}'
            setter = namespace.get(setter_name) or create_setter(attr, field)
            property_fields[setter_name] = setter

        return property(
            getter,
            setter
        )

    @staticmethod
    def _set_foreignkey_field(annotations, attr, property_fields, property_name, value):
        if isinstance(value, ForeignKeyField):
            property_foreign_name = f'{property_name}_id'
            property_fields[property_foreign_name] = property(
                create_getter(f'{attr}_id'),
                create_setter(f'{attr}_id')
            )
            annotations[property_name] = value.to
            annotations[property_foreign_name] = value.internal_type
