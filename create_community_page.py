from base_handler import *
import cgi
import os
import MySQLdb
from google.appengine.api import users;


class CreateCommunityPage(BaseHandler):
    def get(self):
        self.render_response('create_community_page.html')

    def post(self):
	password = cgi.escape(self.request.get('password'))
	name = cgi.escape(self.request.get('name'))

	if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
	    db = MySQLdb.connect(unix_socket='/cloudsql/your-project-id:your-instance-name', user='root')
	else:
            db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")

	cursor = db.cursor()
	result = cursor.execute('SELECT * FROM communities WHERE name = ' + name)
	count = result.rowcount
	if (rowcount == 0):
		#add the new community
		cursor.execute('INSERT INTO communities (name, pin_password) VALUES ('+name+','+password+');')
	else:
		#that community name already exists!
		self.response.write("That community aready exists!")
