from setuptools import setup, find_packages, Extension
try:
    from Cython.Build import cythonize
    USE_CYTHON = True
    ext = 'pyx'
except ImportError:
    USE_CYTHON = False
    ext = 'c'


with open('requirements_dev.txt') as f:
    test_require = f.readlines()


with open('requirements.txt') as f:
    install_requires = f.readlines()


model_extension = Extension(
    'gideon.models.model',
    [f'gideon/models/model.{ext}'],
)

field_extension = Extension(
    'gideon.fields.field',
    [f'gideon/fields/field.{ext}'],
)

date_field_extension = Extension(
    'gideon.fields.date_field',
    [f'gideon/fields/date_field.{ext}'],
)

foreign_key_extension = Extension(
    'gideon.fields.foreign_key_field',
    [f'gideon/fields/foreign_key_field.{ext}'],
)

char_field_extension = Extension(
    'gideon.fields.char_field',
    [f'gideon/fields/char_field.{ext}'],
)

integer_field_extension = Extension(
    'gideon.fields.integer_field',
    [f'gideon/fields/integer_field.{ext}'],
)

extensions = [
    model_extension,
    field_extension,
    date_field_extension,
    foreign_key_extension,
    char_field_extension,
    integer_field_extension
]

if USE_CYTHON:
    extensions = cythonize(
        extensions,
        compiler_directives={'language_level': 3}
    )


setup(
    name='gideon',
    version='0.0.1dev',
    packages=find_packages(exclude=('tests',)),
    install_requires=install_requires,
    author='Julián Cortés',
    author_email='pity7736@gmail.com',
    description='Async postgres data access layer',
    keywords='async asyncpg DAL',
    url='https://github.com/pity7736/gideon-db',
    tests_require=test_require,
    ext_modules=extensions
)
