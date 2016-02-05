"""
To install:

    python setup.py install

to test:

    python setup.py nosetests
"""
from setuptools import setup


setup(
    name='testre',
    description='Temporary rethinkdb databases for',
    long_description=open('README.md').read(),
    version='0.1.0',
    author='Brendan Curran-Johnson',
    author_email='brendan.curran.johnson@invenia.ca',
    license='MPL 2.0',
    url='https://github.com/invenia/testre',
    packages=('testre',),
    package_requires=(
        'pathlib',
        'rethinkdb',
    ),
    tests_require=(
        'codecov',
        'coverage',
        'nose',
    ),
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Database",
        "Topic :: Software Development",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
    ),
)
