from gideon.fields import Field
from gideon.models import Model


class Category(Model):
    __table_name__ = 'categories'
    _id = Field(name='id')
    _name = Field(name='name')
    _description = Field(name='description')
