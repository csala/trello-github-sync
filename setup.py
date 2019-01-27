#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()


with open('HISTORY.md') as history_file:
    history = history_file.read()


install_requires = [
    'py-trello==0.14.0',
    'PyGithub==1.43.4',
    'appdirs==1.4.3',
    'configobj==5.0.6',
]


tests_require = [
    'pytest>=3.4.2',
    'pytest-cov>=2.6.0',
]


setup_requires = [
    'pytest-runner>=2.11.1',
]


development_requires = [
    # general
    'bumpversion>=0.5.3',
    'pip>=9.0.1',
    'watchdog>=0.8.3',

    # docs
    'm2r>=0.2.0',
    'Sphinx>=1.7.1',
    'sphinx_rtd_theme>=0.2.4',
    'graphviz==0.9',
    'ipython==6.5.0',
    'matplotlib==2.2.3',
    'recommonmark>=0.4.0',

    # style check
    'flake8>=3.5.0',
    'isort>=4.3.4',

    # fix style issues
    'autoflake>=1.2',  # keep this after flake8 to avoid
    'autopep8>=1.3.5', # version incompatibilities with flake8

    # distribute on PyPI
    'twine>=1.10.0',
    'wheel>=0.30.0',

    # Advanced testing
    'tox>=2.9.1',
    'coverage>=4.5.1',
]

setup(
    author="Carles Sala",
    author_email='carles@pythiac.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Synchronize Github Issues, Pull Requests and Milestones as Trello cards.",
    entry_points={
        'console_scripts': [
            'tghs=tghs.cli:main',
        ],
    },
    extras_require={
        'test': tests_require,
        'dev': development_requires + tests_require,
    },
    include_package_data=True,
    install_requires=install_requires,
    keywords='tghs Trello Github Sync',
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    name='tghs',
    packages=find_packages(include=['tghs', 'tghs.*']),
    python_requires='>=3.5',
    setup_requires=setup_requires,
    test_suite='tests',
    tests_require=tests_require,
    url='https://github.com/csala/trello-github-sync',
    version='0.1.0-dev',
    zip_safe=False,
)
