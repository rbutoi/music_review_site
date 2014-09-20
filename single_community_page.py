from base_handler import *
from google.appengine.api import users

class SingleCommunityPage(BaseHandler):
    def get(self, community):
        user = users.get_current_user()

	if user:
            self.response.write(community)
        else:
            self.redirect('/')
