# setup.py

from setuptools import setup, find_packages

setup(
    name='spatial_data_app',
    version='0.1.0',
    description='Spatial Data App',
    author='Katarzyna Luszczewska',
    author_email='kasia.luszczewska13@gmail.com',
    url='https://github.com/luszczewskakasia/spatial_data_app',
    packages=find_packages(),
    install_requires=[
        'geopandas',
        'pandas',
        'pytest',
        'plotly',
        'dash',
        'dash-bootstrap-components',
        'plotly-express',
        'statistics', 
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
