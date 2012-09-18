"""
Django-manage.py extension 
python manage.py mediabrute_clearcache
"""
import os

from django.core.management.base import BaseCommand

from mediabrute.context_processors import handlers
from mediabrute.util.dirs import generate_cache_dir

class Command(BaseCommand):
    """
    mediabrute_cache BaseCommand extension
    """
    def handle(self, *args, **options):
        """
        Cache Static Files
        """
        js_urls = handlers.minify_js()
        js_file = open(os.path.join(generate_cache_dir("js"), "mediabrute_usefile"), "w")
        js_file.write(["%s\n" % url for url in js_urls])
        js_file.close()
        
        css_urls = handlers.minify_css()
        css_file = open(os.path.join(generate_cache_dir("css"), "mediabrute_usefile"), "w")
        css_file.write(css_urls)
        css_file.close(["%s\n" % url for url in css_urls])
        