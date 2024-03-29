#!/usr/bin/env python
""" Package install script. """

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


f = open(os.path.join(os.path.dirname(__file__), "README.md"))
readme = f.read()
f.close()

setup(
    name="pdfjinja",
    version="1.0.1",
    author="Elliot Gilmore",
    author_email="elliot@make.mz",
    url="http://github.com/rammie/pdfjinja/",
    description='Use jinja templates to fill and sign pdf forms.',
    long_description=readme,
    py_modules=["pdfjinja"],
    entry_points={"console_scripts": ["pdfjinja = pdfjinja:main"]},
    install_requires=[
        "fdfgen>=0.13.0",
        "jinja2>=2.8",
        "pdfminer.six==20181108",
        "Pillow>=3.2.0",
        "PyPDF2>=2.0.0",
        "reportlab>=3.3.0"
    ])
