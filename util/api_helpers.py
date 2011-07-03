"""
Helper functions for the public API
"""

from mediabrute.util import dirs
from mediabrute.context_processors import heavy_lifting

def clear_cache():
    """
    Clears out the cached media files
    """    
    js_dir = dirs.get_main_js_dir()
    css_dir = dirs.get_main_css_dir()
    
    heavy_lifting.unlink_cache(dirs.generate_cache_dir(js_dir), "js", unlink_all=True)
    heavy_lifting.unlink_cache(dirs.generate_cache_dir(css_dir), "css", unlink_all=True)