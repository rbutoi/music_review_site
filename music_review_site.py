import webapp2
import cgi
from google.appengine.api import users

MAIN_STRING = """\
<html>
  <body>
     <form action="/sign" method="post">
	<div><textarea name="content" rows="3" cols="60"></textarea></div>
	<div><input type="submit" value="Sign guestbook!"></div>
     </form>
  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
	self.response.write(MAIN_STRING)

class TestPage(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>You wrote: <pre>')
	self.response.write(cgi.escape(self.request.get('content')))
	self.response.write('</pre></body></html>')

application = webapp2.WSGIApplication([
    ('/', MainPage),('/sign', TestPage),
], debug=True)
