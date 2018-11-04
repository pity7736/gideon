from setuptools import setup, find_packages


with open('requirements_dev.txt') as f:
    test_require = f.readlines()


setup(
    name='gideon-db',
    version='0.0.1',
    packages=find_packages(exclude='tests'),
    install_requires=['asyncpg==0.18.1'],
    author='Julián Cortés',
    author_email='pity7736@gmail.com',
    description='Async postgres data access layer',
    lincense='LGPLv3',
    keywords='async asyncpg DAL',
    url='https://github.com/pity7736/gideon-db',
    test_require=test_require
)
