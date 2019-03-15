from gideon.models.fields.field cimport Field
from gideon.models.meta_model import MetaModel


class Model(metaclass=MetaModel):

    def __init__(self, **kwargs):
        cdef str key
        cdef Field field
        for key, field in self._fields.items():
            value = kwargs.get(key)
            setattr(self, key, value)

        for key, value in kwargs.items():
            if key not in self._fields.keys() and key not in vars(self):
                raise TypeError(f'Invalid field: {key} is not a field of {self.__class__}')
            setattr(self, key, value)
