from base_handler import *
import cgi
import MySQLdb
from google.appengine.api import users
import os

class ManageUsers(BaseHandler):
    def get(self,id):
	user = users.get_current_user()
	if user:
		email = user.email()
		if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
		    db = MySQLdb.connect(unix_socket='/cloudsql/hack-the-north-1:its-not-django', db='musicsite', user='root')
		else:
		    db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")
		self.response.write('<a href="/communities"><button>Return to Community list</button></a><br>')
		self.response.write('<a href="/communities/%s"><button>Go to Community</button></a><br>'%id)
		self.response.write('<form action="" method="post"><input type="hidden" name="leaveboolean" value="1"><input type="submit" value="Leave community"></form>')
	
		cursor = db.cursor()
		cursor.execute('SELECT * FROM users WHERE email = "%s" AND invite_accepted=1 AND community_id=%s'%(email,id))
		if (cursor.rowcount == 0):
			self.redirect('/communities')
		else:
			cursor.execute('SELECT name FROM communities WHERE id = %s'%id)

			community_name = ""
			for row in cursor:
				community_name = row[0]
			self.response.write('Add new user email: <form action="" method="post"><input type="hidden" name="community_name" value="%s"><input type="text" name="email"><input type="submit" value="Add User"></form>'%community_name)
			cursor.execute('SELECT email FROM users WHERE community_id = %s'%id)
			self.response.write("Current members in %s:"%community_name)
			for row in cursor:
			    self.response.write('<br>%s' % (row[0]))
	else:
	    self.redirect('/communities')
    def post(self,id):
	user = users.get_current_user()
	if user:
		email = user.email()
		if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
		    db = MySQLdb.connect(unix_socket='/cloudsql/hack-the-north-1:its-not-django', db='musicsite', user='root')
		else:
		    db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")

		cursor = db.cursor()
		cursor.execute('SELECT * FROM users WHERE email = "%s" AND invite_accepted=1 AND community_id=%s'%(email,id))
		if (cursor.rowcount == 0):
			self.redirect('/communities')
		else:
			leavestatus = cgi.escape(self.request.get('leaveboolean'))
			community_id = cgi.escape(self.request.get('id'))
			if (leavestatus == "1"):
				self.response.write("You have left this community.<br><a href='/communities'><button>Return to Communities</button></a>")
				cursor = db.cursor()
				cursor.execute('UPDATE users SET invite_hidden=1, invite_accepted=0 WHERE community_id = %s AND email = "%s"' % (id,email))
				db.commit()
			else:
				self.response.write('<a href="/communities"><button>Return to Community list</button></a><br>')
				self.response.write('<a href="/communities/%s"><button>Go to Community</button></a><br>'%id)
				self.response.write('<form action="" method="post"><input type="hidden" name="leaveboolean" value="1"><input type="submit" value="Leave community"></form>')
				email = cgi.escape(self.request.get('email'))
				self.response.write('%s has been invited!<br><br>' % email)

				cursor = db.cursor()
				cursor.execute('SELECT name FROM communities WHERE id = %s'%id)
				community_name = ""
				for row in cursor:
					community_name = row[0]
				cursor.execute('INSERT INTO users VALUES (%s,"%s","%s","%s",0,0)'%(id,community_name,email,email))
				db.commit()
				self.response.write('Add new user email: <form action="" method="post"><input type="hidden" name="community_name" value="%s"><input type="text" name="email"><input type="submit" value="Add User"></form>'%community_name)
				cursor.execute('SELECT email FROM users WHERE community_id = %s'%id)
				self.response.write("Current members in %s:"%community_name)
				for row in cursor:
				    self.response.write('<br>%s' % (row[0]))
	else:
	    self.redirect('/communities')
