# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from distutils.core import Extension

VERSION = '0.1.0'
PACKAGES = find_packages()
LONG_DESCRIPTION = open('README.md', encoding="utf8").read()

setup(name='epanet2tk',
      version=VERSION,
      packages=PACKAGES,
      description='Epanet toolkit wrapper',
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      author='Andrés García Martínez',
      author_email='ppnoptimizer@gmail.com',
      license='GPL 2.0',
      url='https://github.com/andresgciamtez/epanet2tk')
