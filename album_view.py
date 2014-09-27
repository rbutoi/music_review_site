from base_handler import *
import cgi
import MySQLdb
from google.appengine.api import users
import os

class ViewAlbum(BaseHandler):
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
		    cursor.execute('SELECT album_name, album_artist, album_genre, album_year, posted_by FROM albums WHERE id = %s' % album_id)
		    for rows in cursor:
		        album_name = rows[0]
		        album_artist = rows[1]
		        album_genre = rows[2]
		        album_year = rows[3]
		        album_posted_by = rows[4]
		    
		    action = ''
		    cursor.execute('SELECT * FROM comments WHERE parent_album_id = %s AND posted_by = "%s"'%(album_id,email))
		    if (cursor.rowcount == 0):
		       action = 'Add'
		    else:
		       action = 'Edit'
		       
		    cursor.execute('SELECT nickname FROM users WHERE email = "%s"' % album_posted_by)
		    for rows in cursor:
		        album_posted_by = rows[0]
		    
		    template_messages={
		        "album_name":album_name,
		        "album_artist":album_artist,
		        "album_genre":album_genre,
		        "album_year":album_year,
		        "album_posted_by":album_posted_by,
		        "album_id":album_id,
		        "community_id":community_id,
		        "action":action
	            }
		    self.render_response('album_info.html', **template_messages)
		    
		    html_string = ""
		    cursor.execute('SELECT posted_by,comment,last_edit,rating FROM comments WHERE parent_album_id = %s' % album_id)
		    cursor2 = db.cursor()
		    for rows in cursor:
		        comment_posted_by = rows[0]
                        cursor2.execute('SELECT nickname FROM users WHERE email = "%s"' % comment_posted_by)
                        for row2 in cursor2:
                            comment_posted_by = row2[0]
		        comment_text = rows[1]
		        comment_last_edit = rows[2]
		        comment_rating = rows[3]
		        comment_html = """<div><p><font size="5">%s:</font> %s<p></div>""" % (comment_posted_by, comment_text)
		        
		        html_string = html_string + comment_html
		        
	            self.response.write(html_string)
	            self.response.write('</div></body></html>')
	            
	else:
	    self.redirect('/communities')

    def post(self,album_id):
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
		    get_comment_text = cgi.escape(self.request.get('post_comment_text'))
		    get_comment_rating = cgi.escape(self.request.get('post_comment_rating'))
		    
		    cursor.execute('SELECT * FROM comments WHERE parent_album_id = %s AND posted_by = "%s"' % (album_id,email))
		    if (cursor.rowcount == 0):
                        #this is a new comment
                        cursor.execute('INSERT INTO comments (posted_by, parent_album_id, comment, last_edit, rating) VALUES ("%s",%s,"%s",NOW(),%s)'%(email,album_id,get_comment_text,get_comment_rating))
                        db.commit()
                    else:
                        #this is an edit to an existing comment
                        cursor.execute('UPDATE comments SET comment = "%s",rating=%s,last_edit=NOW() WHERE posted_by="%s" AND parent_album_id=%s'%(get_comment_text,get_comment_rating,email,album_id))
                        db.commit()
                        
		    cursor.execute('SELECT album_name, album_artist, album_genre, album_year, posted_by FROM albums WHERE id = %s' % album_id)
		    for rows in cursor:
		        album_name = rows[0]
		        album_artist = rows[1]
		        album_genre = rows[2]
		        album_year = rows[3]
		        album_posted_by = rows[4]
		    
		    action = ''
		    cursor.execute('SELECT * FROM comments WHERE parent_album_id = %s AND posted_by = "%s"'%(album_id,email))
		    if (cursor.rowcount == 0):
		       action = 'Add'
		    else:
		       action = 'Edit'
		    
		    cursor.execute('SELECT nickname FROM users WHERE email = "%s"' % album_posted_by)
		    for rows in cursor:
		        album_posted_by = rows[0]
		    
		    template_messages={
		        "album_name":album_name,
		        "album_artist":album_artist,
		        "album_genre":album_genre,
		        "album_year":album_year,
		        "album_posted_by":album_posted_by,
		        "album_id":album_id,
		        "community_id":community_id,
		        "action":action
	            }
		    self.render_response('album_info.html', **template_messages)
		    
		    html_string = ""
		    cursor.execute('SELECT posted_by,comment,last_edit,rating FROM comments WHERE parent_album_id = %s' % album_id)
		    cursor2 = db.cursor()
		    for rows in cursor:
		        comment_posted_by = rows[0]
                        cursor2.execute('SELECT nickname FROM users WHERE email = "%s"' % comment_posted_by)
                        for row2 in cursor2:
                            comment_posted_by = row2[0]
		        comment_text = rows[1]
		        comment_last_edit = rows[2]
		        comment_rating = rows[3]
		        comment_html = """<div><p><font size="5">%s:</font> %s<p></div>""" % (comment_posted_by, comment_text)
		        
		        html_string = html_string + comment_html
		        
	            self.response.write(html_string)
	            self.response.write('</div></body></html>')
                    
	else:
	    self.redirect('/communities')
