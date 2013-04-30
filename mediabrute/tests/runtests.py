#!/usr/bin/env python
import os
import sys

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'mediabrute',
            'mediabrute.tests',
            'django.contrib.sites',
            'django_nose'
        ],
        SITE_ID = 1,
        STATIC_URL = '/static/',
        ROOT_URLCONF = 'mediabrute.tests.urls',
#         TEST_RUNNER = "django_nose.runner.NoseTestSuiteRunner",
        NOSE_ARGS = ["--with-xcoverage", "--cover-inclusive", "--with-xunit", "--exe", "--verbosity=3", "--cover-package=mediabrute"],
        NOSE_PLUGINS = [
            'nosexcover.XCoverage',
            "nose_exclude.NoseExclude"
        ],
    )


from django.test.simple import DjangoTestSuiteRunner
from django_nose.runner import NoseTestSuiteRunner

def runtests():
    runner = DjangoTestSuiteRunner()
    runner = NoseTestSuiteRunner()
    failures = runner.run_tests(['tests'])
    sys.exit(failures)

if __name__ == '__main__':
    runtests(*sys.argv[1:])

