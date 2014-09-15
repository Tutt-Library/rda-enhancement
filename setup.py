"""
RDA Enhancement
---------------
This module provides RDA enhancements of MARC21 record for catalogs built using
the Catalog Pull Platform.

"""
from setuptools import find_packages, setup

__author__ = "Jeremy Nelson"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)

setup(
    name='rda_enhancement',
    version=__version__,
    url='https://github.com/Tutt-Library/rda-enhancement',
    license='MIT License',
    author=__author__,
    author_email='jeremy.nelson@coloradocollege.edu',
    description='Library for RDA enhancing of Tutt Library MARC21 records',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'pymarc'
    ],
    test_suite="rda_enhancement.tests",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)