#=======================================================================================
# Template_main_01.py
"""Скрипт Setup.py для проекта по упаковке."""
#=======================================================================================

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import sys

from setuptools import setup, find_packages
import json
import os

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import argparse
import datetime

#------------------------------------------
#БИБЛИОТЕКА LU
#------------------------------------------
import LUConst
import LUStrings
import LUSupport
#------------------------------------------

#------------------------------------------
# Разбор аргументов
#------------------------------------------
parser = argparse.ArgumentParser(description='Параметры')
parser.add_argument('-P1', type=str, nargs='?', default='', dest='P1', help='P1')
args = parser.parse_args()
print('-P1=',args.P1)
#------------------------------------------
P1 = ''
if args.P1 != '':
    P1 = args.P1
#endif
#------------------------------------------

#-------------------------------------------------------------------------------
# Template (A1: str, A2: str): -> str
#-------------------------------------------------------------------------------
def read_pipenv_dependencies(fname):
#beginfunction
    """Получаем из Pipfile.lock зависимости по умолчанию."""
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath) as lockfile:
        lockjson = json.load(lockfile)
        return [dependency for dependency in lockjson.get('default')]
    pass
#endfunction

#------------------------------------------
# main():
#------------------------------------------
def main():
#beginfunction
    setup(
        name='PY_demo',
        version=os.getenv('PACKAGE_VERSION', '0.0.dev0'),
        package_dir={'': 'PROJECTS'},
        packages=find_packages('PROJECTS', include=[
           'version*'
        ]),
        description='A demo PYpackage.',
        install_requires=[
             *read_pipenv_dependencies('Pipfile.lock'),
        ]
    )
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
