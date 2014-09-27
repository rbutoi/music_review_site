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
	    cursor.execute('SELECT * FROM users WHERE email = "%s" AND invite_accepted=1 AND community_id=%s'%(email,community))
	    if (cursor.rowcount == 0):
		self.redirect('/communities')
	    else:
		#show the page
		FORM_HTML = '''<!DOCTYPE><html><head><title>Add Album</title></head><body><form action="/communities/%s" method="post">
		Album Name: <input type="text" name="album_name"><br />Album Year: <input type="text" name="album_year"><br />
		Album Artist: <input type="text" name="album_artist"><br />Album Genre: <input type="text" name="album_genre"><br />
		<input type="hidden" name="posted_by" value="%s"><input type="submit" value="Add Album">
		</form></body></html>''' % (community,email)

		self.response.write(FORM_HTML)
	else:
	    self.redirect('/communities')
