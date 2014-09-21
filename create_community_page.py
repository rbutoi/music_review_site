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
	nickname = user.nickname()

	if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
	    db = MySQLdb.connect(unix_socket='/cloudsql/your-project-id:your-instance-name', user='root')
	else:
            db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")

	cursor = db.cursor()
	stringToExecute = 'INSERT INTO communities (name) VALUES ("%s");' % name		
	cursor.execute(stringToExecute)
	db.commit()
	community_id = cursor.lastrowid
	stringToExecute = 'INSERT INTO users (community_id, community_name, email, invite_accepted, nickname, invite_hidden) VALUES ("%s","%s","%s",%s,"%s",%s);' % (community_id, name, email, "false", nickname, "false")
	cursor.execute(stringToExecute)
	db.commit()
	db.close()
