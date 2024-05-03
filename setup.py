"""Set up or install package."""

from json import load
from os import getenv
from os.path import dirname, join

from setuptools import find_namespace_packages, setup, find_packages


def read_pipenv_dependencies(fname):
    """Get default dependencies from Pipfile.lock."""
    filepath = join(dirname(__file__), fname)
    with open(filepath) as lockfile:
        lockjson = load(lockfile)
        return [dependency for dependency in lockjson.get('default')]


def read_readme(fname):
    """Get readme markdown file."""
    filepath = join(dirname(__file__), fname)
    with open(filepath, encoding='utf-8') as readme:
        readme.read()


if __name__ == '__main__':
    setup(
        name='lyrpy',

        #version=getenv('PACKAGE_VERSION', '1.0.dev0'),
        version='1.0.0.0',

        author='Lisitsin Y.R.',
        author_email='lisitsinyr@gmail.com',

        #url='https://github.com/the-gigi/conman',
        #license='MIT',

        description='Just a packaging lyr project.',
        long_description_content_type='text/markdown',

        long_description=read_readme('README.md'),
        #long_description=open('README.md').read(),

        package_dir={'': 'src'},

        packages=find_namespace_packages('src', include=['lyr*']),
        #packages=find_packages(exclude=['tests']),

        #zip_safe=False,
        #setup_requires=['nose>=1.0'],
        #test_suite='nose.collector')

        install_requires=read_pipenv_dependencies('Pipfile.lock'),
        entry_points={
            'console_scripts': [
                'fibo=demo.main:cli'
            ]
        },
        data_files=[
            ('data', ['data/text.txt'])
        ]
    )
