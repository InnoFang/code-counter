
import os
from setuptools import setup, find_packages

short_desc = "A command-line interface(CLI) utilty taht helps you count your code lines."

def read_readme(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name), encoding='utf-8') as f:
        return f.read()

setup(name='code-counter',
      version=__import__('code_counter').__version__,
      author="InnoFang",
      author_email="innofang@yeah.net",
      url='https://github.com/innofang/code-counter',  # homepage
      project_urls={
        'Documentation': 'https://github.com/InnoFang/code-counter/blob/master/README.md',
        'Source': 'https://github.com/InnoFang/code-counter',
        'Bug Reports': 'https://github.com/InnoFang/code-counter/issues',
      },
      description=short_desc,
      long_description=read_readme('README.md'),  # for PyPI
      packages=find_packages(),
      include_package_data=True,
      long_description_content_type="text/markdown",
      license='Apache License',
      install_requires = ["matplotlib", "numpy"],
      python_requires='>=3.5',
      classifiers=[
        'Development Status :: 4 - Beta'
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Environment :: Console',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
      entry_points={
          'console_scripts': [
              'codecount = code_counter.__main__:main'
          ]
      },
      keywords='code line file count counter',
)