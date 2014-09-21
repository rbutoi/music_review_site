import webapp2
from main_page import *
from community_page import *
from create_community_page import *
from join_community_page import *
from single_community_page import *

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/communities/?', CommunityPage),
    ('/create/?', CreateCommunityPage),
    ('/join/?', JoinCommunityPage),
    ('/communities/(.+)', SingleCommunityPage),
    # debug
    # ('/up/?', TestUp)
], debug=True)
