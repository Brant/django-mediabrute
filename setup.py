import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-mediabrute",
    version = ".2",
    url = 'http://github.com/Brant/django-mediabrute',
    license = 'GPL',
    description = "Django MediaBute Compresses and Consolidates CSS and JS Files for Django Applications",
    long_description = read('README.md'),

    author = 'Brant Steen',
    author_email = 'brant.steen@gmail.com',

    packages = find_packages('.'),
    package_dir = {'': '.'},

    install_requires = ['setuptools', 'django'],

    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
