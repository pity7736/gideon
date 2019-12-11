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
            if value and isinstance(field, ForeignKeyField):
                setattr(self, f'{name}_id', value.id)
        setattr(self, name, value)
    return setter


class MetaModel(type):

    def __new__(mcs, name, bases, namespace, **kwargs):
        if name != 'Model':
            table_name = namespace.get('__table_name__', name)
            namespace['__table_name__'] = camel_case_to_snake_case(table_name).replace(' ', '_')
            fields = Map()
            property_fields = {}
            MetaModel._set_id(namespace)
            annotations = {}
            for attr, field in namespace.items():
                if isinstance(field, Field):
                    if not attr.startswith('_'):
                        raise PrivateField('Fields name must be private')

                    fields = fields.set(attr, field)
                    property_name = attr.replace('_', '', 1)
                    if field.name is None:
                        field.name = property_name

                    property_fields[property_name] = MetaModel._resolve_getters_and_setters(
                        attr,
                        namespace,
                        property_fields,
                        field
                    )
                    annotations[property_name] = field.internal_type
                    MetaModel._set_foreignkey_field(annotations, attr, property_fields, property_name, field)

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

    def __getattribute__(self, item):
        fields = type.__getattribute__(self, '_fields')
        field = fields.get(f'_{item}')
        if field:
            return field
        return type.__getattribute__(self, item)
