import webapp2
import cgi
from google.appengine.api import users

class MainPage(webapp2.RequestHandler):
    def get(self):
	user = users.get_current_user()

	if user:
		MAIN_STRING = ('Welcome, %s! (<a href="%s">Click here to logout</a>)' %
			(user.nickname(), users.create_logout_url('/')))
		self.response.write('<html><body>%s</body></html>' % MAIN_STRING)
	
	else:
		self.redirect(users.create_login_url(self.request.uri))

application = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
