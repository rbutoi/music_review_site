import os
from base_handler import *
from google.appengine.api import users
import MySQLdb
import cgi

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
		self.response.write("<a href='/addalbum/%s'><button>Add new album</button></a><hr>"%community)

	else:
	    self.redirect('/communities')

    def post(self, community):
	#used to process post requests from /addalbums
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
		album_name = cgi.escape(self.request.get('album_name'))
		album_year = cgi.escape(self.request.get('album_year'))
		album_genre = cgi.escape(self.request.get('album_genre'))
		album_artist = cgi.escape(self.request.get('album_artist'))
		posted_by = cgi.escape(self.request.get('posted_by'))
		
		cursor.execute('INSERT INTO albums (album_name,album_year,album_genre,album_artist,posted_by,addition_date,community_id) VALUES ("%s",%s,"%s","%s","%s",NOW(),%s);' % (album_name,album_year,album_genre,album_artist,posted_by,community))
		db.commit()
		
		#show the page
		self.response.write("<a href='/manage/%s'><button>Manage this community</button></a>"%community)
		self.response.write("<a href='/addalbum/%s'><button>Add new album</button></a><hr>"%community)
	else:
	    self.redirect('/communities')
