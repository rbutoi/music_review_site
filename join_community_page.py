from base_handler import *

class JoinCommunityPage(BaseHandler):
    def get(self):
        self.render_response('join_community_page.html')
