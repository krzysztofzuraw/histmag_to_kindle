import os
from distutils.core import setup

setup(
    name='Histmag_to_kindle',
    version='0.0.1',
    license='MIT',
    author='Krzysztof Żuraw',
    author_email='krzysztof.zuraw@gmail.com',
    long_description=open('README.md').read(),
    install_requires=[
        'lxml',
        'dominate',
        'requests'
    ]
)