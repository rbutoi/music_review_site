import webapp2
from main_page import *
from community_page import *

application = webapp2.WSGIApplication([
    ('/', MainPage), ('/communities', CommunityPage)
], debug=True)
