from base_handler import *
import cgi
import MySQLdb
from google.appengine.api import users
import os

class JoinCommunityPage(BaseHandler):
    def get(self):
	user = users.get_current_user()
	email = user.email()

	if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
		db = MySQLdb.connect(unix_socket='/cloudsql/your-project-id:your-instance-name', user='root')
	else:
		db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")

	cursor = db.cursor()
	result = cursor.execute('SELECT community_name FROM users WHERE email = "%s" AND invite_accepted = 0;' % email)
	count = cursor.rowcount

	if (count == 0):
		template_messages={
			"message": "You have no pending invites!"
		}
	else:
		pendinglist = []
		for row in cursor:
			pendinglist.append(row[0])
		invitelist = ""
		template_messages={
			"message": "You have %s pending invite(s)!" % count,
			"invites": pendinglist
		}

        self.render_response('join_community_page.html', **template_messages)
	
