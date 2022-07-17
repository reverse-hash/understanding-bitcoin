from setuptools import setup

setup(name='understanding-bitcoin',
      version='0.1',
      install_requires=[
          'coverage',
          'parametrized',  # Used for parameterized unit tests
          'pillow',
          'pylint'
      ])
