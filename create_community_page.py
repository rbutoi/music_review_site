from base_handler import *

class CreateCommunityPage(BaseHandler):
    def get(self):
        self.render_response('create_community_page.html')
