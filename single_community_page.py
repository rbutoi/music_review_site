import os
from base_handler import *
from google.appengine.api import users

class SingleCommunityPage(BaseHandler):
    def get(self, community):
        user = users.get_current_user()

	if user:
            if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
                db = MySQLdb.connect(unix_socket='/cloudsql/your-project-id:your-instance-name', user='root')
            else:
                db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")

            cursor = db.cursor()
            
            db.close()
            
        else:
            self.redirect('/')
