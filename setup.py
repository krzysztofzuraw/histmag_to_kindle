"""Setup.py for histmag_to_kindle."""
from setuptools import setup

setup(
    name='Histmag_to_kindle',
    version='0.0.1',
    license='MIT',
    author='Krzysztof Żuraw',
    packages=['histmag_to_kindle'],
    author_email='krzysztof.zuraw@gmail.com',
    long_description=open('README.md').read(),
    install_requires=[
        'lxml',
        'py',
        'requests'
    ]
)
