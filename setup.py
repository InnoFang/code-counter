#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import os
from setuptools import setup, find_packages

short_desc = "A command-line interface (CLI) utility " \
             "that can help you easily count code lines and display detailed results."


def read_readme(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name), encoding='utf-8') as f:
        return f.read()


setup(name='code-counter',
      version=__import__('code_counter').__version__,
      author="Inno Fang",
      author_email="innofang@yeah.net",
      url='https://github.com/InnoFang/code-counter',  # homepage
      project_urls={
          'Documentation': 'https://github.com/InnoFang/code-counter/blob/master/README.md',
          'Source': 'https://github.com/InnoFang/code-counter',
          'Bug Reports': 'https://github.com/InnoFang/code-counter/issues',
      },
      description=short_desc,
      long_description=read_readme('README.md'),
      packages=find_packages(),
      include_package_data=True,
      long_description_content_type="text/markdown",
      license='Apache License',
      install_requires=["matplotlib", "numpy"],
      python_requires='>=3.7',
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Environment :: Console',
          'Topic :: Utilities',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
      ],
      entry_points={
          'console_scripts': [
              'cocnt = code_counter.__main__:main'
          ]
      },
      keywords='code count line file counter',
      )
