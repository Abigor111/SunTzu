#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    "pip==19.2.3",
    "python>=3.7",
    "bump2version==0.5.11",
    "wheel==0.33.6",
    "watchdog==0.9.0",
    "flake8==3.7.8",
    "tox==3.14.0",
    "coverage==4.5.4",
    "Sphinx==1.8.5",
    "twine==1.14.0",
    "Click==7.1.2",
    "pandas==2.0.2",
    "xarray==2023.6.0",
    "pyarrow==12.0.1",
    "numpy==1.24.4",
    "jsonschema==4.17.3"
]


test_requirements = [""]

setup(
    author="Igor Coimbra Carvalheira",
    author_email='igorccarvalheira111@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description = "SunTzu is a Data Science Library that simplifies data tasks, empowering users with robust data science solutions for faster, meaningful analysis.",
    entry_points={
        'console_scripts': [
            'suntzu=suntzu.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='suntzu, datascience, data science',
    name='suntzu',
    packages=find_packages(include=['suntzu', 'suntzu.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Abigor111/suntzu',
    version='0.2.2',
    zip_safe=False,
)
