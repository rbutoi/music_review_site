from google.appengine.api import users
from base_handler import *
import MySQLdb
import connectgae
from connectgae import DBConnection

class CommunityPage(BaseHandler):
    def get(self):
        user = users.get_current_user()

	if user:
	    email = user.email()
	    if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
		db = MySQLdb.connect(unix_socket='/cloudsql/hack-the-north-1:its-not-django', db='musicsite', user='root')

	    else:
		db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")
	
	    cursor = db.cursor()
	    cursor.execute('SELECT community_name,community_id FROM users WHERE email = "%s" AND invite_accepted=1' % email)

            template_messages={
		"logout_url":users.create_logout_url('/'),
	    }
            self.render_response('community_page.html',**template_messages)
	    self.response.write('<ul>')
	    for row in cursor:
	        self.response.write('<li><a href="communities/%s">%s</a></li>' % (row[1],row[0]))
    	    self.response.write('</ul>')
	else:
            self.redirect(users.create_login_url(self.request.uri))
