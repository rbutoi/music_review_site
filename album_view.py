from base_handler import *
import cgi
import MySQLdb
from google.appengine.api import users
import os

class ViewAlbum(BaseHandler):
    def get(self,album_id):
	user = users.get_current_user()
	community_id = 0
	if user:
		email = user.email()
		if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
		    db = MySQLdb.connect(unix_socket='/cloudsql/hack-the-north-1:its-not-django', db='musicsite', user='root')
		else:
		    db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")
		cursor = db.cursor()
		cursor.execute('SELECT community_id FROM albums WHERE album_id = %s' % album_id)
		for rows in cursor:
		    community_id = rows[0]

		cursor.execute('SELECT * FROM users WHERE email = "%s" AND invite_accepted=1 AND community_id=%s'%(email,community_id))
		if (cursor.rowcount == 0):
		    self.redirect('/communities')
		else:

	else:
	    self.redirect('/communities')

    def post(self,album_id):
	user = users.get_current_user()
	community_id = 0
	if user:
		email = user.email()
		if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
		    db = MySQLdb.connect(unix_socket='/cloudsql/hack-the-north-1:its-not-django', db='musicsite', user='root')
		else:
		    db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")
		cursor = db.cursor()
		cursor.execute('SELECT community_id FROM albums WHERE album_id = %s' % album_id)
		for rows in cursor:
		    community_id = rows[0]

		cursor.execute('SELECT * FROM users WHERE email = "%s" AND invite_accepted=1 AND community_id=%s'%(email,community_id))
		if (cursor.rowcount == 0):
		    self.redirect('/communities')
		else:
		    self.response.write('Post request processed')

	else:
	    self.redirect('/communities')
