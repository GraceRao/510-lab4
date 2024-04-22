import psycopg2

class Database:
    def __init__(self, db_url) -> None:
        self.connection = psycopg2.connect(db_url)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def create_table(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            rating INTEGER NOT NULL,
            price NUMERIC(6,2) NOT NULL
        );
        """
        self.cursor.execute(create_query)
        self.connection.commit()

    def truncate_table(self):
        truncate_query = """
        TRUNCATE TABLE books;
        """
        self.cursor.execute(truncate_query)
        self.connection.commit()
    
    def insert_book(self, book_details):
        insert_query = """
        INSERT INTO books (name, description, rating, price) VALUES (%s, %s, %s, %s);
        """
        self.cursor.execute(insert_query, (book_details['name'], book_details['description'], book_details['rating'], book_details['price']))
        self.connection.commit()