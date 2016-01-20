#
# Database access functions for the web forum.
# 

import time, psycopg2

## Database connection
DB = []
try:
    conn = psycopg2.connect("dbname=forum")
except:
    print "I am unable to connect to the database"
c = conn.cursor()


## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    c.execute("""SELECT content, time, id FROM posts ORDER BY time DESC""")
    
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    posts.sort(key=lambda row: row['time'], reverse=True)
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    c.execute("""INSERT INTO posts VALUES ('%s')""") #% (content)
    #t = time.strftime('%c', time.localtime())
    #DB.append((t, content))
