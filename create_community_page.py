from base_handler import *
import cgi
import os
import MySQLdb
from google.appengine.api import users;


class CreateCommunityPage(BaseHandler):
    def get(self):
        self.render_response('create_community_page.html')

    def post(self):
	name = cgi.escape(self.request.get('name'))
	user = users.get_current_user()
	email = user.email()

	if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
	    db = MySQLdb.connect(unix_socket='/cloudsql/your-project-id:your-instance-name', user='root')
	else:
            db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")

	cursor = db.cursor()
	result = cursor.execute('SELECT * FROM communities WHERE name = "%s";' % name)
	count = cursor.rowcount

	if (count == 0):
		#add the new community
		stringToExecute = 'INSERT INTO communities (name) VALUES ("%s");' % name		
		cursor.execute(stringToExecute)
		stringToExecute = 'INSERT INTO users (community_name, email, invite_accepted) VALUES ("%s","%s",%s);' % (name, email, "false")
		cursor.execute(stringToExecute)
		db.commit()
	else:
		#that community name already exists!
		self.response.write("That community aready exists!")

	db.close()
