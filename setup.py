from Cython.Build import cythonize
from setuptools import setup, find_packages, Extension


with open('requirements_dev.txt') as f:
    test_require = f.readlines()


model_extension = Extension(
    'gideon.models.model',
    ['gideon/models/model.pyx'],
)

field_extension = Extension(
    'gideon.models.fields.field',
    ['gideon/models/fields/field.pyx'],
)

date_field_extension = Extension(
    'gideon.models.fields.date_field',
    ['gideon/models/fields/date_field.pyx'],
)


cython_ext_modules = [model_extension, field_extension, date_field_extension]

setup(
    name='gideon-db',
    version='0.0.2',
    packages=find_packages(exclude='tests'),
    install_requires=['asyncpg==0.18.1', 'immutables==0.6'],
    author='Julián Cortés',
    author_email='pity7736@gmail.com',
    description='Async postgres data access layer',
    keywords='async asyncpg DAL',
    url='https://github.com/pity7736/gideon-db',
    tests_require=test_require,
    ext_modules=cythonize(cython_ext_modules)
)
