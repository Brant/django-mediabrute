"""
Django-manage.py extension 
python manage.py mediabrute_clearcache
"""
import os

from django.core.management.base import BaseCommand

from mediabrute.context_processors import handlers
from mediabrute.util.dirs import generate_cache_dir, get_main_css_dir, get_main_js_dir


class Command(BaseCommand):
    """
    mediabrute_cache BaseCommand extension
    """
    def handle(self, *args, **options):
        """
        Cache Static Files
        """
        possible_js_cache = os.path.join(generate_cache_dir(get_main_js_dir()), "mediabrute_usefile")
        
        if os.path.isfile(possible_js_cache):
            os.unlink(possible_js_cache)
        
        js_urls = handlers.minify_js()
        js_file = open(possible_js_cache, "w")
        for url in js_urls:
            js_file.writelines(js_urls)
        js_file.close()
        
        
        possible_css_cache = os.path.join(generate_cache_dir(get_main_css_dir()), "mediabrute_usefile")
        
        if os.path.isfile(possible_css_cache):
            os.unlink(possible_css_cache)
        
        css_urls = handlers.minify_css()
        css_file = open(possible_css_cache, "w")
        for url in css_urls:
            css_file.writelines(css_urls)            
        css_file.close()
        