from google.appengine.api import users
from base_handler import *
import MySQLdb
import cgi

class EditUser(BaseHandler):
    def get(self):
        user = users.get_current_user()

	if user:
	    email = user.email()
	    
	    if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
		db = MySQLdb.connect(unix_socket='/cloudsql/hack-the-north-1:its-not-django', db='musicsite', user='root')
	    else:
		db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")
	
	    cursor = db.cursor()
	    cursor.execute('SELECT nickname FROM users WHERE email = "%s"' % email)
	    current_nickname = ''
	    for rows in cursor:
	        current_nickname = rows[0]

            template_messages={
                "confirm_message":'',
		"current_nickname":current_nickname
	    }
            self.render_response('edit_user_template.html',**template_messages)
	else:
            self.redirect(users.create_login_url(self.request.uri))
            
    def post(self):
        user = users.get_current_user()

	if user:
	    email = user.email()
	    
	    if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
		db = MySQLdb.connect(unix_socket='/cloudsql/hack-the-north-1:its-not-django', db='musicsite', user='root')
	    else:
		db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")
	
	    cursor = db.cursor()
	    
	    get_new_nickname = cgi.escape(self.request.get('new_nickname'))
	    cursor.execute('UPDATE users SET nickname="%s" WHERE email = "%s"' % (get_new_nickname, email))
	    db.commit()

            confirm_message = "Your nickname has been updated!"
            template_messages={
                "message":confirm_message,
		"current_nickname":get_new_nickname
	    }
            self.render_response('edit_user_template.html',**template_messages)
	else:
            self.redirect(users.create_login_url(self.request.uri))
