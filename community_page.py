from google.appengine.api import users
from base_handler import *

class CommunityPage(BaseHandler):
    def get(self):
        user = users.get_current_user()

	if user:
            # MAIN_STRING = ('Welcome, %s! (<a href="%s">Click here to logout</a>)' %
            # 	(user.nickname(), users.create_logout_url('/')))
            self.render_response('community_page.html', **{'logout_url': users.create_logout_url('/')})
	else:
            self.redirect(users.create_login_url(self.request.uri))
