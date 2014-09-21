from base_handler import *
from google.appengine.api import users
import MySQLdb

class AddAlbum(BaseHandler):
    def get(self, community):
        user = users.get_current_user()
	if user:
	    email = user.email()
            if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
                db = MySQLdb.connect(unix_socket='/cloudsql/hack-the-north-1:its-not-django',db='musicsite', user='root')
            else:
                db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")

            cursor = db.cursor()
            self.response.write("Page in Progress")
	else:
	    self.redirect('/communities')
