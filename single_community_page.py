import os
from base_handler import *
from google.appengine.api import users
import MySQLdb

class SingleCommunityPage(BaseHandler):
    def get(self, community):
        user = users.get_current_user()
	if user:
	    email = user.email()
            if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
                db = MySQLdb.connect(unix_socket='/cloudsql/hack-the-north-1:its-not-django',db='musicsite', user='root')
            else:
                db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")

            cursor = db.cursor()
	    cursor.execute('SELECT * FROM users WHERE email = "%s" AND invite_accepted=1 AND community_id=%s'%(email,community))
	    if (cursor.rowcount == 0):
		self.redirect('/communities')
	    else:
		#show the page
		self.response.write("<a href='/manage/%s'><button>Manage this community</button></a>"%community)
	else:
	    self.redirect('/communities')
