import webapp2
import cgi

class MainPage(webapp2.RequestHandler):
    def get(self):
	self.response.write('<html><body>Welcome to music_review_site. <a href="/communities">Go to communities</a></body></html>')
