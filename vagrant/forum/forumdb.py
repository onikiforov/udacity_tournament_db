# "Database code" for the DB Forum.

import datetime
import psycopg2, bleach

POSTS = [("This is the first post.", datetime.datetime.now())]


def get_posts():
    """Return all posts from the 'database', most recent first."""
    db = psycopg2.connect(database="forum")
    c = db.cursor()
    c.execute("select content, time from posts order by time desc")
    posts = c.fetchall()
    db.close()
    return posts


def add_post(content):
    """Add a post to the 'database' with the current timestamp."""
    db = psycopg2.connect(database="forum")
    c = db.cursor()
    c.execute("insert into posts values (%s)", (bleach.clean(content),))
    db.commit()
    db.close()
    # POSTS.append((content, datetime.datetime.now()))
