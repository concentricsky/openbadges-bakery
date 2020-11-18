import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='openbadges_bakery',
    version='1.2.2',
    packages=['openbadges_bakery'],
    include_package_data=True,
    license='Apache License 2.0',
    description='A python utility for baking and extracting Open Badges metadata from images.',
    long_description=README,
    url='http://info.badgr.io/',
    author='Concentric Sky',
    author_email='notto@concentricsky.com',
    classifiers=[
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Education',
        'Topic :: Utilities',
        'Intended Audience :: Developers'
    ],
    install_requires=[
        'Click >= 6.6',
        'pypng==0.0.20',
        'defusedxml==0.5.0'
    ],
    entry_points="""
        [console_scripts]
        bakery=openbadges_bakery.cli:cli
    """
)
