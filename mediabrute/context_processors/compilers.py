"""
Compilers for mediabrute
"""

import os

from mediabrute.context_processors.heavy_lifting import generate_cache_name
from mediabrute.context_processors.heavy_lifting import unlink_cache
from mediabrute.context_processors.heavy_lifting import compile_files
from mediabrute.context_processors.heavy_lifting import list_media_in_dirs
from mediabrute.context_processors.heavy_lifting import latest_timestamp
from mediabrute.context_processors.heavy_lifting import get_js_settings
from mediabrute.context_processors.heavy_lifting import organize_css_files

from mediabrute import minify


def compile_and_cache_css(css_dirs, cache_dir, app_name=None):
    """
    Return the cache_name of the compiled file
    
    It has been compiled and written to a cache file
    """
    css_files = []
    
    for css_dir in css_dirs:
        css_files += list_media_in_dirs("css", css_dir)
    
    if not app_name:
        app_name = "css"
    
    timestamp = latest_timestamp(css_files)
    
    cache_name = generate_cache_name("css", timestamp, app_name)    
    cache_fullpath = os.path.join(cache_dir, cache_name)
    
    top, mid, bottom = organize_css_files(css_files)
    css_files = top + mid + bottom
    
    if not os.path.isfile(cache_fullpath):
        
        css_contents = compile_files(css_files)
        
        abs_path = dirs.get_css_url()
        if not abs_path.endswith("/"):
            abs_path += "/"
            
        # remove spaces
        css_contents = css_contents.replace("url (", "url(")
        
        # regex an absolute path into URLs that qualify        
        css_contents = re.sub(r'url\(("|\')?([^"\'(https?\:)(//)])([^")]+)("|\')?\)', r'url("%s\2\3")' % abs_path, css_contents)
        
        # remove any double quotes at the end of url lines
        css_contents = css_contents.replace("'\")","\")")
        
        unlink_cache(cache_dir, "css", app_name)
        cache_file = open(cache_fullpath, "w")
        cache_file.write(minify.cssmin(css_contents))
        cache_file.close()
    
    return cache_name

def compile_and_cache_js(js_dirs, cache_dir, add_settings=False, app_name=None):
    """
    Return the cache_name of the compiled file
    
    It has been compiled and written to a cache file
    """    
    js_files = []
    
    for js_dir in js_dirs:
        js_files += list_media_in_dirs("js", js_dir)    
    
    if not app_name:
        app_name = "js"
    
    timestamp = latest_timestamp(js_files)
    
    cache_name = generate_cache_name("js", timestamp, app_name)    
    cache_fullpath = os.path.join(cache_dir, cache_name)
    
    if not os.path.isfile(cache_fullpath):
        unlink_cache(cache_dir, "js", app_name)
        cache_file = open(cache_fullpath, "w")  
        js_contents = compile_files(js_files)
        
        if add_settings:
            js_contents = "%s\n%s" % (get_js_settings(), js_contents)
        
        cache_file.write(minify.jsmin(js_contents))
        cache_file.close()
    
    return cache_name