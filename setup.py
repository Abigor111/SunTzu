#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

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
    description="Library Fusion in Python for Data Analysis: Streamlining data analysis workflows by combining and enhancing Python libraries.",
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
    version='0.1.0',
    zip_safe=False,
)
