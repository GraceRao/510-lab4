import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from db import Database


load_dotenv()
BASE_URL = 'http://books.toscrape.com/catalogue/page-{page}.html'

def get_book_rating(rating_str):
    rating_dict = {
        'Zero': 0,
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    return rating_dict.get(rating_str, 0)

with Database(os.getenv('DATABASE_URL')) as db:
    db.create_table()

    current_page = 1
    while True:
        page_url = BASE_URL.format(page=current_page)
        print(f"Scraping {page_url}")
        page_response = requests.get(page_url)
        page_soup = BeautifulSoup(page_response.content, 'html.parser')
        book_elements = page_soup.select('article.product_pod')

        if not book_elements:
            break

        for book_element in book_elements:
            book_data = {}
            book_data['name'] = book_element.select_one('h3 > a').get('title')
            price_text = book_element.select_one('p.price_color').text[1:]
            book_data['price'] = float(price_text)
            book_data['rating'] = get_book_rating(book_element.select_one('p.star-rating').get('class')[1])
            book_url = 'http://books.toscrape.com/catalogue/' + book_element.select_one('h3 > a').get('href')
            
            book_detail_response = requests.get(book_url)
            book_detail_soup = BeautifulSoup(book_detail_response.content, 'html.parser')
            description_elem = book_detail_soup.select_one('.product_page > p')
            book_data['description'] = description_elem.text if description_elem else 'No description available'

            db.insert_book(book_data)
        current_page += 1
