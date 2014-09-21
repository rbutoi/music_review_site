from base_handler import *
import cgi
import MySQLdb
from google.appengine.api import users
import os

class ManageUsers(BaseHandler):
    def get(self,id):
	if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
	    db = MySQLdb.connect(unix_socket='/cloudsql/hack-the-north-1:its-not-django', db='musicsite', user='root')
	else:
	    db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")


	cursor = db.cursor()
	cursor.execute('SELECT name FROM communities WHERE id = %s'%id)

	community_name = ""
	for row in cursor:
		community_name = row[0]
	self.response.write('Add new user email: <form action="" method="post"><input type="hidden" name="community_name" value="%s"><input type="text" name="email"><input type="submit" value="Add User"></form>'%community_name)
	cursor.execute('SELECT email FROM users WHERE community_id = %s'%id)
	self.response.write("Current members in %s:"%community_name)
	for row in cursor:
	    self.response.write('<br>%s' % (row[0]))

    def post(self,id):
	if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
	    db = MySQLdb.connect(unix_socket='/cloudsql/hack-the-north-1:its-not-django', db='musicsite', user='root')
	else:
	    db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")

	community_id = cgi.escape(self.request.get('id'))
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
