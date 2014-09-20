import webapp2

class CreateCommunityPage(webapp2.RequestHandler):
    def get(self):
	self.response.write('<html>Create page</html>')
