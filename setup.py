#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tap-ringcentral',
      version='1.0.0',
      description='Singer.io tap for extracting data from the RingCentral API',
      author='Fishtown Analytics',
      url='http://fishtownanalytics.com',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_ringcentral'],
      install_requires=[
          'tap-framework==0.0.4',
      ],
      entry_points='''
          [console_scripts]
          tap-ringcentral=tap_ringcentral:main
      ''',
      packages=find_packages(),
      package_data={
          'tap_ringcentral': [
              'schemas/*.json'
          ]
      })
