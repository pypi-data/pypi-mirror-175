from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.1'
DESCRIPTION = 'Calculates test drug patients good or not'
LONG_DESCRIPTION = 'A package that calculates test drug patients good or not'

# Setting up
setup(
    name="stats_drug_test_patients",
    version=VERSION,
    author="PunGrumpy",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'statistics', 'education'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
