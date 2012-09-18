"""
Code sitting behind context processors
"""
import os

from mediabrute.util import dirs
from mediabrute.context_processors.compilers import compile_and_cache_js, compile_and_cache_css
from mediabrute.context_processors.heavy_lifting import list_media_in_dirs

def minify_js(app_name=None):
    """
    {{ MINI_JS }} Context processor
    """
    js_dir = dirs.get_main_js_dir()
    cache_dir = dirs.generate_cache_dir(js_dir)
        
    js_dirs = [js_dir, dirs.APP_JS_DIRS]
    """
    js_files = []
    js_files_only = []
    for js_dir in js_dirs:
        js_files += list_media_in_dirs("js", js_dir)
    
    for js_file in js_files:
        js_files_only.append(js_file.split("/")[-1])
    
    return ["%s/%s" % (dirs.get_js_url(), js_file) for js_file in js_files_only]
    """
    cache_files = [compile_and_cache_js(js_dirs, cache_dir, add_settings=True),]
    
    if app_name and app_name in dirs.get_separated_apps("js"):
        cache_files.append(compile_and_cache_js([dirs.get_separated_js(app_name), ], cache_dir, app_name=app_name))    
        
    return ["%s/cache/%s" % (dirs.get_js_url(), cache_name) for cache_name in cache_files]
    

def minify_css(app_name=None):
    """
    {{ MINI_CSS }} Context processor
    """    
    css_dir = dirs.get_main_css_dir()
    cache_dir = dirs.generate_cache_dir(css_dir)
    
    possible_cache = os.path.join(cache_dir, "mediabrute_usefile")
    if os.path.isfile():
        txt = open(possible_cache)
        css_urls = txt.readlines()
    
    print css_urls
    
    return [url for url in css_urls if url != ""]    
    
    css_dirs = [css_dir, dirs.APP_CSS_DIRS]
    
    cache_files = [compile_and_cache_css(css_dirs, cache_dir), ]
    
    if app_name and app_name in dirs.get_separated_apps("css"):
        cache_files.append(compile_and_cache_css([dirs.get_separated_css(app_name), ], cache_dir, app_name=app_name))
    
    return ["%s/cache/%s" % (dirs.get_css_url(), cache_name) for cache_name in cache_files]

