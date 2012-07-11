"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import os
import inspect

from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command

from mediabrute.util import dirs, api_helpers, defaults
from mediabrute import api
from mediabrute.util import list_css_top_files, list_css_bottom_files
from mediabrute.context_processors import heavy_lifting


class ManagementTestCase(TestCase):
    """
    Tests for custom management commands
    """
    def test_jssettings(self):
        """
        Test the creation of a static JS settings file
        """
        settings_fullpath = os.path.join(dirs.get_main_js_dir(), "mediabrute-settings.js")
        
        if os.path.isfile(settings_fullpath):
            os.unlink(settings_fullpath)            
        self.assertFalse(os.path.isfile(settings_fullpath))
        
        call_command("mediabrute_jssettings")
        self.assertTrue(os.path.isfile(settings_fullpath))
        
        os.unlink(settings_fullpath)            
        self.assertFalse(os.path.isfile(settings_fullpath))
        
        custom_filename = "heyo.js"
        custom_fullpath = os.path.join(dirs.get_main_js_dir(), "heyo.js")
        
        if os.path.isfile(custom_fullpath):
            os.unlink(custom_fullpath)            
        self.assertFalse(os.path.isfile(custom_fullpath))
        
        call_command("mediabrute_jssettings", "heyo")
        self.assertTrue(os.path.isfile(custom_fullpath))
        
        os.unlink(custom_fullpath)            
        self.assertFalse(os.path.isfile(custom_fullpath))
        
        custom_filename = "heyo"
        custom_fullpath = os.path.join(dirs.get_main_js_dir(), "heyo.js")
        
        if os.path.isfile(custom_fullpath):
            os.unlink(custom_fullpath)            
        self.assertFalse(os.path.isfile(custom_fullpath))
        
        call_command("mediabrute_jssettings", "heyo")
        self.assertTrue(os.path.isfile(custom_fullpath))
        
        os.unlink(custom_fullpath)            
        self.assertFalse(os.path.isfile(custom_fullpath))
        

class CssOrderingTestCase(TestCase):
    """
    Tests relating to the proper ordering of CSS sheets
    """
    def setUp(self):
        """
        Setup for css ordering tests
        """
        self.fake_file_list = [
                             "/asdfs/gggg/yoyo/mobile.css",
                             "/asdf/gggg/yoyo2/mobile.css",
                             "/yayay/asdf/not/style.css",
                             "/hoooboy/yup.css",
                             "/ohyayay/reset.css",
                             ]
        
    def test_css_top_files_belong(self):
        """
        Make sure that all top files returned by the organize_css_files belong there
        """
        top, std, bottom = heavy_lifting.organize_css_files(self.fake_file_list)
        for fle in top:
            self.assertIn(os.path.basename(fle), list_css_top_files())
            
    def test_css_bottom_files_belong(self):
        """
        Make sure that all bottom files returned by the organize_css_files belong there
        """
        top, std, bottom = heavy_lifting.organize_css_files(self.fake_file_list)
        for fle in bottom:
            self.assertIn(os.path.basename(fle), list_css_bottom_files())
            
    def test_css_bottom_files_ordered(self):
        """
        Make sure that the
        
        This is only important if there are multiple
        settings.CSS_BOTTOM_FILES and matches found 
        
        TODO:Finish this test
        """
        
        top, std, bottom = heavy_lifting.organize_css_files(self.fake_file_list)
         
        if len(bottom) > 1 and len(list_css_bottom_files()) > 1:
            for found_file in bottom:
                found_file_name = os.path.basename(found_file)
                
                        
                for f_file_again in bottom:
                    f_file_again_name = os.path.basename(f_file_again)
                            
                    if not found_file_name == f_file_again_name:
                        if bottom.index(found_file) > bottom.index(f_file_again):
                            self.assertGreater(list_css_bottom_files().index(found_file_name), list_css_bottom_files().index(f_file_again_name))

                        if bottom.index(found_file) < bottom.index(f_file_again):
                            self.assertLess(list_css_bottom_files().index(found_file_name), list_css_bottom_files().index(f_file_again_name))
                
                
    def test_css_top_files_ordered(self):
        """
        Make sure that the
        
        This is only important if there are multiple
        settings.CSS_TOP_FILES and matches found
        
        TODO:Finish this test 
        """
        
        top, std, bottom = heavy_lifting.organize_css_files(self.fake_file_list)
        
        if len(top) > 1 and len(list_css_top_files()) > 1:
            for found_file in top:
                found_file_name = os.path.basename(found_file)
                
                        
                for f_file_again in top:
                    f_file_again_name = os.path.basename(f_file_again)
                            
                    if not found_file_name == f_file_again_name:
                        if top.index(found_file) > top.index(f_file_again):
                            self.assertGreater(list_css_top_files().index(found_file_name), list_css_top_files().index(f_file_again_name))

                        if top.index(found_file) < top.index(f_file_again):
                            self.assertLess(list_css_top_files().index(found_file_name), list_css_top_files().index(f_file_again_name))
                 

class PublicApiTestCase(TestCase):
    """
    Tests relating to mediabrute.api
    """
    def tearDown(self):
        """
        Execute this after each test
        """
        api.clear_cache()
    
    def test_parameterless_calls(self):
        """
        find and call all API functions
        that require no arguments
        """
        for attr in dir(api):
            func = getattr(api, attr)
            if callable(func):                
                spec = inspect.getargspec(func)
                if not spec.args and not spec.varargs and not spec.keywords and not spec.defaults:
                    func()
                    
    def test_get_cached_css(self):
        """
        Test the "get cached css" api call
        
        should return a file name in a list
        """
        self.assertEquals(len(api.get_cached_css()), 1)
        
    def test_get_cached_js(self):
        """
        Test the "get cached css" api call
        
        should return a file name in a list
        """
        self.assertEquals(len(api.get_cached_js()), 1)
        

class URLsTestCase(TestCase):
    """
    Test some things regarding auto-generated URLs
    """
    def test_get_serving_url(self):
        """
        Test our serving url
        """
        self.assertEquals(dirs.get_serving_url(), settings.STATIC_URL)
        
        with self.settings(MEDIABRUTE_USE_STATIC=False):
            self.assertEquals(dirs.get_serving_url(), settings.MEDIA_URL)
    
    def test_css_url(self):
        """
        Test auto-generated CSS urls
        """
        self.assertEquals(dirs.get_css_url(), "%s%s" % (settings.STATIC_URL, "css"))
        
        with self.settings(MEDIABRUTE_USE_STATIC=False):
            self.assertEquals(dirs.get_css_url(), "%s%s" % (settings.MEDIA_URL, "css"))
            
        with self.settings(MEDIABRUTE_CSS_URL_PATH="heyo/yoyo"):
            self.assertEquals(dirs.get_css_url(), "%s%s" % (settings.STATIC_URL, "heyo/yoyo"))
    
        with self.settings(MEDIABRUTE_USE_STATIC=False, MEDIABRUTE_CSS_URL_PATH="heyo/yoyo"):
            self.assertEquals(dirs.get_css_url(), "%s%s" % (settings.MEDIA_URL, "heyo/yoyo"))
    
    def test_js_url(self):
        """
        Test auto-generated JS urls
        """
        self.assertEquals(dirs.get_js_url(), "%s%s" % (settings.STATIC_URL, "js"))
        
        with self.settings(MEDIABRUTE_USE_STATIC=False):
            self.assertEquals(dirs.get_js_url(), "%s%s" % (settings.MEDIA_URL, "js"))
        
        with self.settings(MEDIABRUTE_JS_URL_PATH="heyo/yoyo"):
            self.assertEquals(dirs.get_js_url(), "%s%s" % (settings.STATIC_URL, "heyo/yoyo"))
    
        with self.settings(MEDIABRUTE_USE_STATIC=False, MEDIABRUTE_JS_URL_PATH="heyo/yoyo"):
            self.assertEquals(dirs.get_js_url(), "%s%s" % (settings.MEDIA_URL, "heyo/yoyo"))
       
        
class DefaultSettingsTestCase(TestCase):
    """
    Test cases for default settings
    """
    def test_get_root(self):
        """
        dirs.get_root
        """
        self.assertEquals(dirs.get_root(), settings.STATIC_ROOT)
        
        with self.settings(MEDIABRUTE_USE_STATIC=False):
            self.assertEquals(dirs.get_root(), settings.MEDIA_ROOT)
        
    def test_css_dir(self):
        """
        Main CSS directory default setting test
        
        should match either settings.CSS_DIR or just "css"
        Test that it works as a fullpath AND standalone
        """
        fullpath = dirs.get_main_css_dir()
        ext_only = dirs.get_main_css_dir(full_path=False)
        
        try:
            ext_compare = settings.CSS_DIR
        except AttributeError:
            ext_compare = defaults.CSS_DIR
            
        fullpath_compare = os.path.join(dirs.get_root(), ext_compare)
        
        self.assertEquals(fullpath_compare, fullpath)
        self.assertEquals(ext_compare, ext_only)
        
    def test_js_dir(self):
        """
        Main JS directory default setting test
        
        should match either settings.JS_DIR or just "js"
        Test that it works as a fullpath AND standalone
        """
        fullpath = dirs.get_main_js_dir()
        ext_only = dirs.get_main_js_dir(full_path=False)
        
        try:
            ext_compare = settings.JS_DIR
        except AttributeError:
            ext_compare = defaults.JS_DIR
            
        fullpath_compare = os.path.join(dirs.get_root(), ext_compare)
        
        self.assertEquals(fullpath_compare, fullpath)
        self.assertEquals(ext_compare, ext_only)
        
    def test_css_top_files_list(self):
        """
        Make sure that list_css_top_files matches 
        either settings.CSS_TOP_FILES or an empty list
        """
        try:
            self.assertEquals(settings.CSS_TOP_FILES, list_css_top_files())
        except AttributeError:
            self.assertEquals([], list_css_top_files())
    
    def test_css_bottom_files_list(self):
        """
        Make sure that list_css_bottom_files matches 
        either settings.CSS_BOTTOM_FILES or an empty list
        """
        try:
            self.assertEquals(settings.CSS_BOTTOM_FILES, list_css_bottom_files())
        except AttributeError:
            self.assertEquals([], list_css_bottom_files())
            
    def test_css_app_dirs(self):
        """
        First, look for an APP_CSS setting,
        otherwise, default to "css"
        """
        try:
            ext = settings.APP_CSS
        except AttributeError:
            ext = defaults.APP_CSS
        
        for app, directory in dirs.APP_CSS_DIRS:
            self.assertIn("/%s" % ext, directory)
    
    def test_clear_cache(self):
        """
        Test that clearing the cache works
        i.e. does not raise an error
        """
        api_helpers.clear_cache()
        
       
    def test_js_app_dirs(self):
        """
        First, look for an APP_JS setting,
        otherwise, default to "js"
        """
        try:
            ext = settings.APP_JS
        except AttributeError:
            ext = defaults.APP_JS
        
        for app, directory in dirs.APP_JS_DIRS:
            self.assertIn("/%s" % ext, directory)
            
    def test_separated_apps(self):
        """
        Test what is separated by default
        """
        self.assertEquals(dirs.get_separated_apps("css"), [])
        self.assertEquals(dirs.get_separated_apps("js"), [])
        
        with self.settings(SEPARATE_CSS=["something"]):
            self.assertIn("something", dirs.get_separated_apps("css"))
            self.assertEquals(len(dirs.get_separated_apps("css")), 1)
            
        with self.settings(SEPARATE_JS=["something"]):
            self.assertIn("something", dirs.get_separated_apps("js"))
            self.assertEquals(len(dirs.get_separated_apps("js")), 1)
            
class MiscTestCase(TestCase):
    """
    Tests for some misc. stuff
    """
    def test_import_app(self):
        """
        Test our little app import function
        """
        dirs.attempt_app_import("mediabrute")
        with self.assertRaises(ImproperlyConfigured):
            dirs.attempt_app_import("NONONONONO")
        