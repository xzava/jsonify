#!/usr/bin/env python3

import os
from setuptools import setup

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(name='jsonify',
      version='0.0.1',
      description='UI wrapper for flask.jsonify',
      author='Mike Hall - Kaurifund.com',
      license='MIT',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages = ['jsonify'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
      ],
      install_requires=['flask'],
      python_requires='>=3.8',
      extras_require={
        'testing': ["pytest"],
      },
      include_package_data=True)