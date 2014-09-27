import webapp2
from main_page import *
from community_page import *
from create_community_page import *
from join_community_page import *
from single_community_page import *
from manage_users import *
from add_album import *
from album_view import *
from add_comment import *
from edit_user import *

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/communities/?', CommunityPage),
    ('/create/?', CreateCommunityPage),
    ('/join/?', JoinCommunityPage),
    ('/communities/(.+)', SingleCommunityPage),
    ('/manage/(.+)', ManageUsers),
    ('/addalbum/(.+)', AddAlbum),
    ('/albums/(.+)', ViewAlbum),
    ('/addcomment/(.+)', AddComment),
    ('/edituser/?', EditUser)
    # debug
    # ('/up/?', TestUp)
], debug=True)
