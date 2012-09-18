"""
Django-manage.py extension 
python manage.py mediabrute_clearcache
"""
import os

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
        js_urls = handlers.minify_js()
        js_file = open(os.path.join(generate_cache_dir("js"), "mediabrute_usefile"))
        js_file.write(["%s\n" % url for url in js_urls])
        js_file.close()
        
        css_urls = handlers.minify_css()
        css_file = open(os.path.join(generate_cache_dir("css"), "mediabrute_usefile"))
        css_file.write(css_urls)
        css_file.close(["%s\n" % url for url in css_urls])
        