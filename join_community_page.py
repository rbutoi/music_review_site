import webapp2

class JoinCommunityPage(webapp2.RequestHandler):
    def get(self):
	self.response.write('<html>Join page</html>')
