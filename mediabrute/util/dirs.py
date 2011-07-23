"""
Build CSS and JS directory lists at compile

Based on how django builds list of template directories
"""

import os
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from mediabrute.util import defaults

APP_CSS_DIRS = []
APP_JS_DIRS = []

    

def join_em(mod, ext):
    """
    Join app directory and "extension" directory
    """
    return os.path.join(os.path.dirname(mod.__file__), ext)

def generate_cache_dir(media_dir):
    """
    generate the cache directory,
    
    create directory if needed
    """
    try:
        ext = settings.MEDIA_CACHE_DIR
    except AttributeError:
        ext = defaults.MEDIA_CACHE_DIR
    
    fullpath = os.path.join(media_dir, ext)
    if not os.path.isdir(fullpath):
        os.makedirs(fullpath)
    
    return fullpath

def attempt_app_import(app):
    """
    Make sure that the app exists, or raise error
    
    TODO: Look into whether this is needed...
    It is repeated logic from the template dirs... 
    presumably this will have already been checked by django...
    """
    try:
        mod = import_module(app)
        return mod
    except ImportError, err:
        raise ImproperlyConfigured('ImportError %s: %s' % (app, err.args[0]))  


def get_main_css_dir(full_path=True):
    """
    return the main CSS directory
    
    This is where the cache will exist
    """
    try:
        css_dir = settings.CSS_DIR
    except AttributeError:
        css_dir = defaults.CSS_DIR
        
    if full_path:
        return os.path.join(settings.MEDIA_ROOT, css_dir)
        
    return css_dir    
    

def get_main_js_dir(full_path=True):
    """
    return the main JS directory
    
    This is where the cache will exist
    """
    try:
        js_dir = settings.JS_DIR
    except AttributeError:
        js_dir = defaults.JS_DIR
        
    if full_path:
        return os.path.join(settings.MEDIA_ROOT, js_dir)
        
    return js_dir    

def find_app_media_dirs():
    """
    Finds all the APP media directories
    
    makes them lists as "constants" so that the list
    doesn't need to be generated repeatedly during requests
    """
    fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
    
    try:
        css_ext = settings.APP_CSS
    except AttributeError:
        css_ext = defaults.APP_CSS
        
    try:
        js_ext = settings.APP_JS
    except AttributeError:
        js_ext = defaults.APP_JS
        
    for app in settings.INSTALLED_APPS:
        mod = attempt_app_import(app) 
        
        css_dir = join_em(mod, css_ext)
        js_dir = join_em(mod, js_ext)
        
        if os.path.isdir(css_dir):
            APP_CSS_DIRS.append(css_dir.decode(fs_encoding))
        
        if os.path.isdir(js_dir):
            APP_JS_DIRS.append(js_dir.decode(fs_encoding))
    
find_app_media_dirs()   

    
    

