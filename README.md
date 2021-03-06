Mediabrute
==========

Media Brute's purpose is to automatically collect, compile, minify, and cache all JS and CSS for a Django project. It then has context processors that allow that minified JS and CSS to be referenced in the templates.

It will crawl through a "main" js and css directory (2 different directories) which sits in the settings.MEDIA_ROOT. It will then crawl through all settings.INSTALLED_APPS looking for CSS and JS as well. Once it finds everything, it will compile everything that it has found, minify it, and cache it.

collect -> compile -> minify -> write to cache


It does timestamp checking, so it only updates the cache'd file when it finds a css or js file that has been modified since the cache'd file was created. (It does this for CSS and JS separately).

It is great for projects where only 1 js and/or css file needs to be cached for the entire site/project.

Feel free to take a look at the [code coverage report](http://ci.podioadventures.com/view/Brant/job/mediabrute-tests/)


Usage
-----
Basic usage is just a matter of adding any one of the three context processors to your settings file. Then, the minified media can be accessed in your templates.

### Context Processors
You can use the JS or CSS minifiers separately or just use the mini_media to have them both available

- mediabrute.context_processors.mini_media
- mediabrute.context_processors.mini_js
- mediabrute.context_processors.mini_css

### Add to Templates
In your templates, then, you can access the cache'd files using the context processors.

    {% for sheet in MINI_CSS %}
    	<link rel="stylesheet" type="text/css" href="{{ sheet }}" />
    {% endfor %}

and

    {% for script in MINI_JS %}
    	<script src="{{ script }}"></script>
    {% endfor %}


Management commands
-------------------

There are a couple of management commands that can be called for mediabrute

### Cache Manually

	manage.py mediabrute_cache

This will generate a "lock" file in the cache directory of each static media type (e.g. "js/cache" and "css/cache"). This lock file will tell mediabrute's context processor what the name of the cache file is without letting mediabrute try to re-cache the files themselves. 

This can be useful when using mediabrute as part of a deployment process.

**NOTE:** When there is a lock file, the normal "on-the-fly" caching will stop. In order to clear the lock, either re-run mediabrute_cache or delete the lock file 


### Clearing the Cache

Clears the cached CSS and JS files

    manage.py mediabrute_clearcache


### Generate JS settings

An alternative to allowing mediabrute to auto generate the js settings file

- If using this, simply do not add JS_SETTINGS_TEMPLATE setting
- see JS_SETTINGS_TEMPLATE setting above

The generated file can then simply be stuck into the js directory from which mediabrute normally pulls

    manage.py mediabrute_jssettings <filename>


Configurations	
-------------------------

### CSS_DIR
- Main CSS directory inside STATIC_ROOT (or MEDIA_ROOT - see MEDIABRUTE_USE_STATIC configuration)
- For example, if set to "theme/css", mediabrute will collect from "/path/to/media/root/theme/css" 
- e.g. CSS_DIR = "css" 
- Defaults to "css"

### JS_DIR 
- Main JS directory inside STATIC_ROOT (or MEDIA_ROOT - see MEDIABRUTE_USE_STATIC configuration)
- For example, if set to "theme/js", mediabrute will collect from "/path/to/media/root/theme/js"
- e.g. JS_DIR = "js"
- Defaults to "js" 

### MEDIABRUTE_REMOVE_OLD
- setting for whether or not you want old cache files to be removed
- True will keep cache directories cleaned up, False will let them build over time
- Set to False if you are using server-side caching (like redis)
- e.g. MEDIABRUTE_REMOVE_OLD = False
- defaults to True

### MEDIABRUTE_USE_STATIC
- set to False if you are using MEDIA_ROOT for your static stuff instead of STATIC_ROOT
- Useful for apps that were created before Django 1.3, where STATIC stuff was introduced
- e.g. MEDIABRUTE_USE_STATIC = False
- defaults to True

### APP_CSS
- where app-specific CSS will sit in app directory
- e.g. : "media/css", 
- defaults to "css"
	
### APP_JS
- where app-specific JS will sit in app directory
- e.g. : "media/js", 
- defaults to "js"
	
### CSS_TOP_FILES
- the list of files that should go at the top of the final CSS file
- i.e. : things that should be overrideable
- e.g. css resets, other standard sheets
	
### CSS_BOTTOM_FILES
- the list of filenames that should go at the bottom of the final CSS file
- i.e. : things that should have "the final say"
- e.g. files with lots of media queries for responsive design

### MEDIABRUTE_CSS_URL_PATH
- Differentiates the URL path from the directory path
- defaults to CSS_DIR setting

### MEDIABRUTE_JS_URL_PATH
- Differentiates the URL path from the directory path
- defaults to JS_DIR setting

### JS_SETTINGS_TEMPLATE
- location and name of a template for js settings
- This allows the project to auto-generate some settings for use in JS
- e.g. "mediabrute/js/config.txt"
- defaults to not being used (None)

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


Separation Configurations
-------------------------

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


API
---

from mediabrute import api

- api.clear_cache() : clears cached js and css files
- api.get_app_css_dirs() : get a list of css directories found inside apps (not inside the main css directory)
- api.get_app_js_dirs() : get a list of js directories found inside apps (not inside the main js directory)
- api.get_main_js_dir() : get the main js directory that mediabrute will pull from (this is the one inside MEDIA_ROOT)
- api.get_main_css_dir() : get the main css directory that mediabrute will pull from (this is the one inside MEDIA_ROOT)

Serving static through runserver
--------------------------------

Mediabrute works best if you are running a separate server for your static files, not channeling static files through runserver.

But, we _can_ get it to work.

Assuming you have /path/to/static/ and inside there, you have css and js as dirs
..so: */path/to/static/css/* and */path/to/static/js/*

### First, configure STATIC_ROOT, STATICFILES_DIRS, and STATICFILES_FINDERS
	
	STATICFILES_FINDERS = ("django.contrib.staticfiles.finders.FileSystemFinder", ) 
	STATICFILES_DIRS = ( "/path/to/static/", )
	STATIC_ROOT = /path/to
Note that "STATICFILES_DIRS" and "STATIC_ROOT" are related, in that "STATICFILES_DIRS" should be a path all the way to the static directory, while "STATIC_ROOT" stops just before that same static diretory.
	

### Second, use a few hack configurations to get mediabrute to cooperate
	
	CSS_DIR = "static/css"
	JS_DIR = "static/js"
	MEDIABRUTE_CSS_URL_PATH = "css"
	MEDIABRUTE_JS_URL_PATH = "js"
