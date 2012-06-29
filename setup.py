from setuptools import setup, find_packages

setup(
    name = "django-mediabrute",
    version = ".3",
    url = 'http://github.com/Brant/django-mediabrute',
    license = 'GPL',
    description = "Django MediaBute Compresses and Consolidates CSS and JS Files for Django Applications",
    long_description = open('README.rst').read(),

    author = 'Brant Steen',
    author_email = 'brant.steen@gmail.com',

    packages = find_packages(exclude=('socialprofile_demo', 'tests', )),
    include_package_data = True,
    zip_safe = False,

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
