import webapp2
import cgi
from google.appengine.api import users

class CommunityPage(webapp2.RequestHandler):
    def get(self):
	user = users.get_current_user()

	if user:
		MAIN_STRING = ('Welcome, %s! (<a href="%s">Click here to logout</a>)' %
			(user.nickname(), users.create_logout_url('/')))
		self.response.write('<html><body>%s' % MAIN_STRING)
		self.response.write('<br /><a href="/create">Create a community</a>')
		self.response.write('<br /><a href="/join">Join a community</a>')
		self.response.write('<br /><hr>Your currently joined communities:')
		self.response.write('</body></html>')
	
	else:
		self.redirect(users.create_login_url(self.request.uri))
