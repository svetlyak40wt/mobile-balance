#!/usr/bin/env python

from setuptools import setup

setup(
    name='mobile-balance',
    version='0.6.0',
    description='A set of utilities to retrive a balance from some Russian mobile operators.',
    author='Alexander Artemenko',
    author_email='svetlyak.40wt@gmail.com',
    url='https://github.com/svetlyak40wt/mobile-balance',
    packages=[
        'mobile_balance',
    ],
    entry_points={
        'console_scripts': [
            'mobile-balance = mobile_balance.main:main',
        ]
    },
    install_requires=[
        'requests<2.3.0',
        'docopt<0.7.0',
        'pyopenssl',
        'ndg-httpsclient',
        'pyasn1'
    ],
    license='BSD',
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='mobile, balance, utility'
)
