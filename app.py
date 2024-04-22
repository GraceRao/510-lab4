import streamlit as st
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Book Search & Filter App",
    page_icon="📚",
    layout="centered",
)

# connect to the database
def connect_db():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

# query books from the database
def query_books(name=None, description=None, rating=None, price=None, order_by=None):
    conn = connect_db()
    query = """
    SELECT * FROM books
    WHERE (%s IS NULL OR name ILIKE %s)
    AND (%s IS NULL OR description ILIKE %s)
    """
    params = [name, f"%{name}%", description, f"%{description}%"]
    
    if rating is not None:
        query += " AND rating >= %s"
        params.append(rating)
    
    if price is not None:
        query += " AND price <= %s"
        params.append(price)
    
    if order_by and order_by in ['rating', 'price']:
        query += f" ORDER BY {order_by}"

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# initial session_state
if 'books_df' not in st.session_state or 'search_clicked' not in st.session_state:
    st.session_state['books_df'] = query_books()  # load all books initially
    st.session_state['search_clicked'] = False

# Streamlit app layout
st.title('📚 Book Search & Filter 🔍')
st.write('Welcome to the Book Search & Filter App! Use the sidebar to search and filter books we have.')

# search & filter sidebar
with st.sidebar:
    st.header("Search & Filter")
    name = st.text_input('Search by name')
    description = st.text_input('Search by description')
    rating = st.slider('Minimum rating', 0, 5, 0)
    price = st.slider('Maximum price', 0, 100, 100)
    order_by = st.selectbox('Order by', ['None', 'rating', 'price'])
    search = st.button('Search')  # button to trigger search

# search button clicked
if search:
    st.session_state['books_df'] = query_books(name, description, rating, price, None if order_by == 'None' else order_by)
    st.session_state['search_clicked'] = True

# display books
if not st.session_state['books_df'].empty:
    st.write(st.session_state['books_df'])
else:
    st.write("No books found.")
