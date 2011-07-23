"""
API for app programming use
"""

from mediabrute.util import dirs, api_helpers
from mediabrute.context_processors import heavy_lifting


def clear_cache():
    """
    Clears out cache
    """
    api_helpers.clear_cache()

def get_app_css_dirs():
    """
    Returns the list of CSS directories
    These are the directories that Media Brute pulls CSS from 
    """
    return dirs.APP_CSS_DIRS

def get_app_js_dirs():
    """
    Returns the list of JS directories
    These are the directories that Media Brute pulls JS from 
    """
    return dirs.APP_JS_DIRS


def get_main_css_dir():
    """
    Returns the main CSS directory
    
    This is where the cache directory/file will be placed
    """
    return dirs.get_main_css_dir()


def get_main_js_dir():
    """
    Returns the main JS directory
    
    This is where the cache directory/file will be placed
    """
    return dirs.get_main_js_dir()

def get_all_js_dirs():
    """
    Return a list of ALL javascript directories 
    that mediabrute pulls from
    """
    return get_app_js_dirs().append(get_main_js_dir())

def get_all_css_dirs():
    """
    Return a list of ALL css directories 
    that mediabrute pulls from
    """
    return get_app_css_dirs().append(get_main_css_dir())
    
