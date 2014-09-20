import os
import jinja2
import webapp2
import cgi

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):

	template_values = {
	}

	template = JINJA_ENVIRONMENT.get_template('template_files/index.html')
	self.response.write(template.render(template_values))
#	self.response.write('<html><body>Welcome to music_review_site. <a href="/communities">Go to communities</a></body></html>')
