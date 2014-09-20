from base_handler import *

class CreateCommunityPage(BaseHandler):
    def get(self):
        self.render_response('main_page.html')
