from base_handler import *
import cgi
import MySQLdb
from google.appengine.api import users
import os

class AddComment(BaseHandler):
    def get(self,album_id):
	user = users.get_current_user()
	community_id = 0
	if user:
		email = user.email()
		if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
		    db = MySQLdb.connect(unix_socket='/cloudsql/hack-the-north-1:its-not-django', db='musicsite', user='root')
		else:
		    db = MySQLdb.connect(host='localhost', user='root', passwd="htndjango",db="musicsite")
		cursor = db.cursor()
		cursor.execute('SELECT community_id FROM albums WHERE id = %s' % album_id)
		for rows in cursor:
		    community_id = rows[0]

		cursor.execute('SELECT * FROM users WHERE email = "%s" AND invite_accepted=1 AND community_id=%s'%(email,community_id))
		if (cursor.rowcount == 0):
		    self.redirect('/communities')
		else:
                    #user has permission to view the page
                    cursor.execute('SELECT comment,rating FROM comments WHERE posted_by = "%s" AND parent_album_id = %s'%(email,album_id))
                    if (cursor.rowcount == 0):
                        #this is user's first comment
		        template_messages={
                            "album_id":album_id,
                            "previous_comment_text":''
	                }
		        self.render_response('add_comment.html', **template_messages)
		    
                    else:
                        #populate the forms with their previous data
                        for rows in cursor:
                            previous_comment_text = rows[0]
                            previous_comment_rating = rows[1]
                        
      		        template_messages={
                            "album_id":album_id,
                            "previous_comment_text":previous_comment_text
	                }
		        self.render_response('add_comment.html', **template_messages)

	            
	else:
	    self.redirect('/communities')
