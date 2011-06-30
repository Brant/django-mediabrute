"""
Code sitting behind context processors
"""
import os
from mediabrute.util import dirs
from mediabrute.context_processors.heavy_lifting import list_media_in_dirs
from mediabrute.context_processors.heavy_lifting import latest_timestamp
from mediabrute.context_processors.heavy_lifting import generate_cache_name
from mediabrute.context_processors.heavy_lifting import unlink_cache
from mediabrute.context_processors.heavy_lifting import organize_css_files
from mediabrute.context_processors.heavy_lifting import compile_files
from mediabrute.context_processors.heavy_lifting import get_js_settings
from django.conf import settings
from mediabrute import minify

def compile_and_cache_js(js_files, cache_dir, add_settings=False, app_name=None):
    """
    Return the cache_name of the compiled file
    
    It has been compiled and written to a cache file
    """
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

def minify_js(app_name):
    """
    {{ MINI_JS }} Context processor
    """
            
    js_dir = dirs.get_main_js_dir()
    cache_dir = dirs.generate_cache_dir(js_dir)
    
    app_js_files = list_media_in_dirs("js", dirs.APP_JS_DIRS)
    main_js_files = list_media_in_dirs("js", js_dir)
    
    cache_files = [compile_and_cache_js(app_js_files + main_js_files, cache_dir, add_settings=True),]
    
    if app_name:
        cache_files.append(compile_and_cache_js(app_js_files + main_js_files, cache_dir, app_name=app_name))    
    
        
    return ["%s%s/cache/%s" % (settings.MEDIA_URL, dirs.get_main_js_dir(full_path=False), cache_name) for cache_name in cache_files]
    

def minify_css(app_name):
    """
    {{ MINI_CSS }} Context processor
    """    
    css_dir = dirs.get_main_css_dir()
    
    cache_dir = dirs.generate_cache_dir(css_dir)
    
    app_css_files = list_media_in_dirs("css", dirs.APP_CSS_DIRS)
    main_css_files = list_media_in_dirs("css", css_dir)    
        
    timestamp = latest_timestamp(app_css_files + main_css_files)
    cache_name = generate_cache_name("css", timestamp)
    
    cache_fullpath = os.path.join(cache_dir, cache_name)
    
    if not os.path.isfile(cache_fullpath):
        css_top_files, css_std_files, css_bot_files = organize_css_files(app_css_files + main_css_files)
        
        full_list = css_top_files + css_std_files + css_bot_files
        
        css_contents = compile_files(full_list)
        
        css_contents = css_contents.replace('url(', 'url(../')
        css_contents = css_contents.replace('url (', 'url(../')
        css_contents = css_contents.replace('url(../http', 'url(http')
        
        unlink_cache(cache_dir, "css")
        cache_file = open(cache_fullpath, "w")
        cache_file.write(minify.cssmin(css_contents))
        cache_file.close()
        
    return "%s%s/cache/%s" % (settings.MEDIA_URL, dirs.get_main_css_dir(full_path=False), cache_name)

