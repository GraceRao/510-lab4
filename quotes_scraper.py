import requests
from bs4 import BeautifulSoup

from db import Database

BASE_URL = 'https://quotes.toscrape.com/page/{page}'
mydb = Database()
mydb.create_table()

response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, 'html.parser')
quote_divs = soup.select('div.quote')

quotes = []
page = 1
while True:
    url = BASE_URL.format(page=page)
    print(f"Scraping {url}")
    response = requests.get(url)

    # if outside of valid page range
    if 'No quotes found!' in response.text:
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    # select all quote divs
    quote_divs = soup.select('div.quote')

    for quote_div in quote_divs:
        # parse individual quote
        quote = {}
        quote['content'] = quote_div.select_one('span.text').text
        quote['author'] = quote_div.select_one('small.author').text
        #quote['author_link'] = quote_div.select('span')[1].select('a')[0]
        quote['tags'] = [tag.text for tag in quote_div.select('a.tag')]
        #quote['tag_links'] = [tag['href'] for tag in quote_div.select('a.tag')]

        # insert into database
        mydb.insert(quote)
        
        quotes.append(quote)
    page += 1

print(quotes)