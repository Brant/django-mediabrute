Introduction
============

Media Brute's purpose is to automatically collect, compile, minify, and cache all JS and CSS for a Django project. It then has context processors that allow that minified JS and CSS to be referenced in the templates.

It will crawl through a "main" js and css directory (2 different directories) which sits in the settings.MEDIA_ROOT. It will then crawl through all settings.INSTALLED_APPS looking for CSS and JS as well. Once it finds everything, it will compile everything that it has found, minify it, and cache it.

collect -> compile -> minify -> write to cache


It does timestamp checking, so it only updates the cache'd file when it finds a css or js file that has been modified since the cache'd file was created. (It does this for CSS and JS separately).

It is great for projects where only 1 js and/or css file needs to be cached for the entire site/project.

Important Configurations
========================

At the very least, these two settings should be added to your django settings file.

* CSS_DIR
    - e.g. CSS_DIR = "css"
    - Main CSS directory inside STATIC_ROOT (or MEDIA_ROOT),, 
    - Defaults to "css"
    - For example, if set to "theme/css", mediabrute will collect from "/path/to/media/root/theme/css" 


* JS_DIR 
    - e.g. JS_DIR = "js"
    -  Main JS directory inside STATIC_ROOT (or MEDIA_ROOT),
    - Defaults to "js"
    - For example, if set to "theme/js", mediabrute will collect from "/path/to/media/root/theme/js"

Usage
=====
Basic usage is just a matter of adding any one of the three context processors to your settings file. Then, the minified media can be accessed in your templates.

Context Processors
------------------

You can use the JS or CSS minifiers separately or just use the mini_media to have them both available

* mediabrute.context_processors.mini_media
* mediabrute.context_processors.mini_js
* mediabrute.context_processors.mini_css

Add to Templates
------------------
In your templates, then, you can access the cache'd files using the context processors.

    {% for sheet in MINI_CSS %}
    	<link rel="stylesheet" type="text/css" href="{{ sheet }}" />
    {% endfor %}

and

    {% for script in MINI_JS %}
    	<script src="{{ script }}"></script>
    {% endfor %}


Separation Configurations
=========================

You can configure mediabrute to separate out certain apps and cache their media (css, js) separately.

In order to do this, two things are needed.

1) Name the app in your URL conf 

    urlpatterns = patterns('', 
    	(r'^', include('some_app.urls', app_name="some_app"))
    )
    
	The app_name must match the name of the app, as written in the INSTALLED_APPS setting
	
2) Put the app_name in your settings, as part of SEPARATE_CSS and/or SEPARATE_JS
	
	SEPARATE_CSS : A list of apps (found in INSTALLED_APPS) that should be separated
		e.g. SEPARATE_CSS = ['some_app', 'some_other_app']
		default = []

	SEPARATE_JS : A list of apps (found in INSTALLED_APPS) that should be separated
		e.g. SEPARATE_JS = ['some_app', 'some_other_app']
		default = []

These apps will have their css/js cached separately and will be part of the context processor ONLY when a visitor is inside the app's url confs

Additional Configurations	
=========================

MEDIABRUTE_USE_STATIC
--------------------
* set to False if you are using MEDIA_ROOT for your static stuff instead of STATIC_ROOT
* Useful for apps that were created before Django 1.3, where STATIC stuff was introduced
* e.g. MEDIABRUTE_USE_STATIC = False
* defaults to True

APP_CSS
-------
* where app-specific CSS will sit in app directory
* e.g. : "media/css", 
* defaults to "css"
	
APP_JS
------
* where app-specific JS will sit in app directory
* e.g. : "media/js", 
* defaults to "js"
	
CSS_TOP_FILES
-------------
* the list of files that should go at the top of the final CSS file
* i.e. : things that should be overrideable
* e.g. css resets, other standard sheets
	
CSS_BOTTOM_FILES
----------------
* the list of filenames that should go at the bottom of the final CSS file
* i.e. : things that should have "the final say"
* e.g. files with lots of media queries for responsive design

JS_SETTINGS_TEMPLATE
--------------------
* location and name of a template for js settings
* This allows the project to auto-generate some settings for use in JS
* e.g. "templates/js/config.txt"
* defaults to not being used (None)

The template has django.conf.settings available to it as "settings"

So, you could do something like this:

	function siteVars(opt){
		switch (opt){
			case 'home':
				return '{% url website.views.hello_world %}';
				break;
			case 'media':
				return '{{settings.MEDIA_URL}}';
				break;
			case 'img':
				return siteVars('media') + 'img/';
				break; 
			case 'swf':
				return siteVars('media') + 'swf/';
				break; 
			default:
				return null;
				break;
		}
	}


Management commands
===================

There are a couple of management commands that can be called for mediabrute

### Clearing the Cache

Clears the cached CSS and JS files

    manage.py mediabrute_clearcache


### Generate JS settings

An alternative to allowing mediabrute to auto generate the js settings file

* If using this, simply do not add JS_SETTINGS_TEMPLATE setting
* see JS_SETTINGS_TEMPLATE setting above

The generated file can then simply be stuck into the js directory from which mediabrute normally pulls

    manage.py mediabrute_jssettings <filename>


API
===

from mediabrute import api

* api.clear_cache() : clears cached js and css files
* api.get_app_css_dirs() : get a list of css directories found inside apps (not inside the main css directory)
* api.get_app_js_dirs() : get a list of js directories found inside apps (not inside the main js directory)
* api.get_main_js_dir() : get the main js directory that mediabrute will pull from (this is the one inside MEDIA_ROOT)
* api.get_main_css_dir() : get the main css directory that mediabrute will pull from (this is the one inside MEDIA_ROOT)


	