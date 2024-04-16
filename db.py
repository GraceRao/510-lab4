import os
import psycopg2

class Database:
    def __init__(self):
        self.con = psycopg2.connect(os.getenv('DATABASE_URL'))
    
    def create_table(self):
        q = """
        CREATE TABLE IF NOT EXISTS quotes (
        id SERIAL PRIMARY KEY,
        content TEXT NOT NULL,
        author TEXT NOT NULL,
        tags TEXT  NOT NULL
        );
        """
        self.cur.execute(q)

    def insert(self, quote):
        q = """
        INSERT INTO quotes (content, author, tags) VALUES (%s, %s, %s)
        """
        self.cur.execute(q, (quote['content'],quote['author'] , quote['tags']))
        self.con.commit()