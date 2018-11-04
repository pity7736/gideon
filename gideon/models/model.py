from gideon.models.meta_model import MetaModel


class Model(metaclass=MetaModel):

    __table_name__ = ''

    def __init__(self, **kwargs):
        for key, field in self._fields.items():
            value = kwargs.get(key)
            setattr(self, key, value)

        for key, value in kwargs.items():
            if key not in self._fields.keys() and key not in vars(self):
                raise TypeError(f'Invalid field: {key} is not a field of {self.__class__}')
            setattr(self, key, value)
