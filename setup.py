from setuptools import setup, find_packages
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


extensions = [
    f'gideon/models/model.{ext}',
    f'gideon/fields/field.{ext}',
    f'gideon/fields/date_field.{ext}',
    f'gideon/fields/foreign_key_field.{ext}',
    f'gideon/fields/char_field.{ext}',
    f'gideon/fields/integer_field.{ext}'
]

if USE_CYTHON:
    extensions = cythonize(
        extensions,
        compiler_directives={'language_level': 3}
    )


setup(
    name='gideon',
    version='0.0.2dev',
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
