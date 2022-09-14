#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = f.read()

# package configuration - for reference see:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#id9
setup(
    name='ball.model',
    description="Model to simulate a ball falling through the air under gravity",
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'serve-app=ball.model.frontend.serve:main',
            'serve-production=ball.model.frontend.serve:production'
        ]
    },
    package_data={
        'ball.model.frontend': ['assets/*', 'assets/img/*'],
        'ball.model': ['data/*.csv']
    },
    include_package_data=True,
    zip_safe=False,
    keywords='ball.model',
    python_requires=">=3.7.*",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7'
    ],
    data_files=[('', ['README.md',
                      'requirements.txt',
                      ]),
                ],
)
