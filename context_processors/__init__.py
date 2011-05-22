"""
Media Brute Context Processors

use mini_media for CSS and JS,
or use mini_js/mini_css separately
"""



from mediabrute.context_processors.handlers import minify_css, minify_js

def mini_media(*args, **kwargs):
    """
    Context processor to expose {{ MINI_JS }} and {{ MINI_CSS }}
    """

    minis.update(mini_css())
    minis.update(mini_js())
    return minis

def mini_js():
    """
    {{ MINI_JS }} Context Processor
    
    Gives a full URL to the minified, cached JS
    """

    return {"MINI_JS": minify_js()}

def mini_css():
    """
    {{ MINI_CSS }} Context Processor
    
    Gives a full URL to the minified, cached CSS
    """
    return {"MINI_CSS": minify_css()}