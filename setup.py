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


with open('README.md') as f:
    long_description = f.read()


extensions = [
    ('gideon.models.model', f'gideon/models/model.{ext}'),
    ('gideon.fields.field', f'gideon/fields/field.{ext}'),
    ('gideon.fields.date_field', f'gideon/fields/date_field.{ext}'),
    ('gideon.fields.datetime_field', f'gideon/fields/datetime_field.{ext}'),
    ('gideon.fields.foreign_key_field', f'gideon/fields/foreign_key_field.{ext}'),
    ('gideon.fields.char_field', f'gideon/fields/char_field.{ext}'),
    ('gideon.fields.integer_field', f'gideon/fields/integer_field.{ext}')
]


if USE_CYTHON:
    extensions = cythonize(
        [extension[1] for extension in extensions],
        compiler_directives={'language_level': 3}
    )
else:
    extensions = [Extension(name=name, sources=[extension]) for name, extension in extensions]


setup(
    name='gideon',
    version='0.0.0.a1',
    packages=find_packages(exclude=('tests',)),
    install_requires=install_requires,
    author='Julián Cortés',
    author_email='pity7736@gmail.com',
    description='Async postgres data access layer',
    long_description=long_description,
    keywords='async asyncpg DAL',
    url='https://github.com/pity7736/gideon',
    tests_require=test_require,
    ext_modules=extensions,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Database',

    ]
)
