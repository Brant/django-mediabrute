"""
Media Brute Context Processors

use mini_media for CSS and JS,
or use mini_js/mini_css separately
"""
from mediabrute.context_processors.handlers import minify_css, minify_js

def mini_media(request):
    """
    Context processor to expose {{ MINI_JS }} and {{ MINI_CSS }}
    """
    minis = {}
    minis.update(mini_css(request))
    minis.update(mini_js(request))
    return minis

def mini_js(request):
    """
    {{ MINI_JS }} Context Processor
    
    Gives a full URL to the minified, cached JS
    """
    return {"MINI_JS": minify_js()}

def mini_css(request):
    """
    {{ MINI_CSS }} Context Processor
    
    Gives a full URL to the minified, cached CSS
    """
    return {"MINI_CSS": minify_css()}