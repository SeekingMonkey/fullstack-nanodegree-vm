#
# Database access functions for the web forum.
# 

import time, psycopg2




## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    ## Database connection
    try:
        DB = psycopg2.connect("dbname=forum")
    except:
        print "I am unable to connect to the database"
    c = DB.cursor()
    c.execute("""DELETE FROM table WHERE content LIKE '%spam%'""")
    DB.commit()
    c.execute("""DELETE FROM table WHERE content LIKE '%cheese%'""")
    DB.commit()
    c.execute("""SELECT * FROM posts ORDER BY time DESC""")
    DBdata = c.fetchall()
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DBdata]
    DB.close()
    return posts

## Add a post to the database.
def AddPost(post):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    try:
        DB = psycopg2.connect("dbname=forum")
    except:
        print "I am unable to connect to the database"
    c = DB.cursor()
    print "content is: %s" % post
    c.execute("INSERT INTO posts(content) VALUES (%s)", (post,))
    DB.commit()
    DB.close()

