#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open('README.md') as f:
    readme = f.read()

with open('CHANGELOG.md') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()
    requirements = [x[:-1] for x in requirements]

with open('requirements_dev.txt') as test_requirements_file:
    test_requirements = test_requirements_file.readlines()
    test_requirements = [x[:-1] for x in test_requirements]

setup_requirements = ['setuptools >= 38.6.0', 'twine >= 1.11.0']

setup(
    author="Kyle Barron",
    author_email='kylebarron2@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Description ",
    entry_points={
        'console_scripts': [
            'keplergl_quickvis=keplergl_cli.cli:main',
            'kepler=keplergl_cli.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords=['keplergl', 'mapbox', 'cli'],
    name='keplergl_cli',
    packages=find_packages(include=['keplergl_cli', 'keplergl_cli.*']),
    package_data={'keplergl_cli': ['keplergl_config.json']},
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/kylebarron/keplergl_cli',
    version='0.3.1',
    zip_safe=False,
)
