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
		cursor.execute('SELECT name FROM communities WHERE id = %s'%community)
		community_name = ""
		for row in cursor:
		    community_name = row[0]

		html_string=""		    
	        cursor.execute('SELECT id, album_name, album_artist FROM albums WHERE community_id = %s' % community)
	        for row in cursor:
	            album_name = row[1]
	            album_artist = row[2]
	            album_id = row[0]
	            album_string = """<div class="album">
                                          <a href="/albums/%s">
                                            <img class="album_art" src="http://placekitten.com/g/250/250" alt="%s">
                                          </a>
                                          <p><b>%s</b><br />%s</p>
                                        </div>""" % (album_id, album_name, album_name, album_artist)
	            html_string = html_string + album_string
	            
		template_messages={
			"community_id":community,
			"community_name":community_name
		}
		self.render_response('community_albums.html', **template_messages)
	        self.response.write(html_string)
	        self.response.write('</div></div></body></html>')
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
		cursor.execute('SELECT name FROM communities WHERE id = %s'%community)
		community_name = ""
		for row in cursor:
		    community_name = row[0]
		
		html_string = ""
		template_messages={
			"community_id":community,
			"community_name":community_name,
			"message":html_string
		}
		self.render_response('community_albums.html', **template_messages)
	else:
	    self.redirect('/communities')
