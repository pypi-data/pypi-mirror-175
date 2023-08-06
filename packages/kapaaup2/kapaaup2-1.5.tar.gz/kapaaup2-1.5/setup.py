from distutils.core import setup
import setuptools
packages = ['kapaaup2']
setup(name='kapaaup2',
	version='1.5',
	author='szblack',
    packages=packages, 
    package_dir={'requests': 'requests'},)