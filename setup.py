import sys
from setuptools import setup, find_packages


install_requires = [
    'PyQt5>=5.15.4',
    'pyqt5-plugins>=5.15.4.2.2',
    'PyQt5-Qt5>=5.15.4',
    'PyQt5-sip>=12.9.0',
    'mariadb>=1.0.8'
]

setup(
    name="Brion Gahl CS 430 Project",
    version='1.0',
    description='none',
    python_requires='>=3.7.0',
    install_requires=install_requires
)