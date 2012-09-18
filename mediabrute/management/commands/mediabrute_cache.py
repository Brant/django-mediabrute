"""
Django-manage.py extension 
python manage.py mediabrute_clearcache
"""
from django.core.management.base import BaseCommand

from mediabrute.context_processors import handlers


class Command(BaseCommand):
    """
    mediabrute_cache BaseCommand extension
    """
    def handle(self, *args, **options):
        """
        Cache Static Files
        """
        handlers.minify_js()
        handlers.minify_css()
        