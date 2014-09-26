from base_handler import *
import cgi
import MySQLdb
from google.appengine.api import users
import os

class JoinCommunityPage(BaseHandler):
    def get(self):
	user = users.get_current_user()
	if not user:
		self.redirect('/')
	else:
		email = user.email()

		if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
			db = MySQLdb.connect(unix_socket='/cloudsql/hack-the-north-1:its-not-django', db='musicsite', user='root')
		else:
			db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")

		cursor = db.cursor()
		result = cursor.execute('SELECT community_name,community_id FROM users WHERE email = "%s" AND invite_accepted = 0 AND invite_hidden=0;' % email)
		count = cursor.rowcount

		if (count == 0):
			template_messages={
				"message": "You have no pending invites!"
			}
		else:
			#known bug where if you have two pending invites of the same name, accepting will cause you to accept both
			pendinglist = []
			for row in cursor:
				pendinglist.append(row[0])
			template_messages={
				"message": "You have %s pending invite(s)!" % count,
				"invites": pendinglist
			}
		db.close()

		self.render_response('join_community_page.html', **template_messages)

    def post(self):
	community = cgi.escape(self.request.get('community'))
	user = users.get_current_user()
	if not user:
		self.redirect('/')
	else:
		email = user.email()

		if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
			db = MySQLdb.connect(unix_socket='/cloudsql/hack-the-north-1:its-not-django', db='musicsite', user='root')
		else:
			db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")

		cursor = db.cursor()
		result = cursor.execute('UPDATE users SET invite_accepted=1 WHERE email="%s" AND community_name="%s";' % (email,community))
		db.commit()

		result = cursor.execute('SELECT community_name,community_id FROM users WHERE email = "%s" AND invite_accepted = 0 AND invite_hidden=0;' % email)
		count = cursor.rowcount
		if (count == 0):
			template_messages={
				"message": "%s has been joined successfully! You have no pending invites!" % community
			}
		else:
			pendinglist = []
			for row in cursor:
				pendinglist.append(row[0])
			invitelist = ""
			template_messages={
				"message": "%s has been joined successfully! You have %s pending invite(s)!" % (community,count),
				"invites": pendinglist
			}
		db.close()
		self.render_response('join_community_page.html', **template_messages)
