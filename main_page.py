import os
import jinja2
import webapp2
import cgi
from base_handler import *

class MainPage(BaseHandler):
    def get(self):
        self.render_response('main_page.html')
