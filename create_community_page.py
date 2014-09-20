from base_handler import *
import cgi
import os
import MySQLdb

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
