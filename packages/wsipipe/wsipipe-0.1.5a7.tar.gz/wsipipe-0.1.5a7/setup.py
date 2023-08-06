#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
#from wsipipe import __version__
__version__ = '0.1.5a7'

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

setup_requirements = [ ]

test_requirements = [ ]

project = "wsipipe"

setup(
    author="David Morrison, Christina Fell",
    author_email='dm236@st-andrews.ac.uk, cmf21@st-andrews.ac.uk',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A set of tools for processing pathology whole slide images for deep learning.",
    entry_points={
        'console_scripts': [
            'wsipipe=wsipipe.cli:main',
        ],
    },
    install_requires=['scipy', 'scikit-image', 'pandas', 'numpy', 'opencv-python-headless==4.5.5.64', 'Pillow', 'openslide-python'],
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='wsipipe',
    name='wsipipe',
    packages=find_packages(include=['wsipipe', 'wsipipe.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/davemor/wsipipe',
    version=__version__,
    zip_safe=False,
)
