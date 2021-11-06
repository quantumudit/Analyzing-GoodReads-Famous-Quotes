import requests
from bs4 import BeautifulSoup
import re
import datetime

all_quotes = []
all_page_links = []

SESSION = requests.session()

HEADERS = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52",
        "accept-language": "en-US"
    }

def generate_page_links() -> None:
    """
    This function generate the page URLs that are used to scrape quotes
    """
    
    for pgno in range(1,101):
        page_link = f"https://www.goodreads.com/quotes?page={pgno}"
        all_page_links.append(page_link)
    return

def scrape_content(page_url: str) -> None:
    """
    This function page URL, scrapes the required data and appends it to the 'all_quotes' list
    Args:
        page_url (str): The Page URL string
    Returns:
        None: It returns nothing but, appends all individual game and its metric dictionary to 'all_quotes' list
    """
    
    print(f'Scraping quote details from: {page_url}')
    
    current_utc_timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%d-%b-%Y %H:%M:%S')
    
    response = SESSION.get(page_url, headers=HEADERS)
    
    soup = BeautifulSoup(response.content, 'lxml')
    content = soup.find('div', class_='quotes').find_all('div', class_ = 'quote')
    
    for quote in content:
        
        raw_quote = quote.find('div', class_ = 'quoteText').text.strip().replace('\n','')
        
        pattern = re.match(r'(“.*”).*',raw_quote)
        quote_text = pattern.group(1)
        
        author = quote.find('span', class_ = 'authorOrTitle').text.strip().replace(',','')
        likes = quote.find('div', class_='quoteFooter').find('div', class_='right').text.strip().replace(' likes','').replace(' like','')
        
        try:
            author_image = quote.find('a', class_='leftAlignedImage').find('img')['src']
        except:
            author_image=''
        
        try:
            tags = quote.find('div', class_='quoteFooter').find('div', class_='greyText smallText left').text.strip().replace('tags:', '')
            tags = re.sub(r'\s+', '', tags)
        except:
            tags = ''
        
        try:
            quote_book = quote.find('a',class_ = 'authorOrTitle').text.strip()
        except:
            quote_book = ''
            
        quote_details = {
            'quote': quote_text,
            'author': author,
            'author_image': author_image,
            'book_reference': quote_book,
            'tags': tags,
            'likes': likes,
            'last_updated_at_UTC': current_utc_timestamp
        }
        
        all_quotes.append(quote_details)
    return

if __name__ == '__main__':
    
    generate_page_links()
    
    print('\n')
    print(f'Total pages to scrape: {len(all_page_links)}')
    print('\n')
    
    page_url = "https://www.goodreads.com/quotes?page=1"
    
    scrape_content(page_url)
    
    print('\n')
    print(f'Total quotes scraped: {len(all_quotes)}')
    print('\n')
    print(all_quotes)