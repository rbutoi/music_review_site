from base_handler import *

class MainPage(BaseHandler):
    def get(self):
        self.render_response('main_page.html')
