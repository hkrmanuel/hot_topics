import requests
from bs4 import BeautifulSoup
import pycountry
import pandas as pd
import random
import time
import sqlite3 as sql

class TrendsNewsSpider:
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
        # Add more user agents if needed
    ]

    def __init__(self, country=None):
        self.country = country
        self.data = []
        self.base_url_allafrica = 'https://allafrica.com/'
        self.download_delay = 2  # Default delay of 2 seconds

    def start_requests(self):
        if self.country is not None:
            url_allafrica = f'{self.base_url_allafrica}{self.country.lower()}/'
            self.parse_allafrica(url_allafrica)
        else:
            print("No country provided")

    def get_random_user_agent(self):
        return random.choice(self.USER_AGENTS)

    def parse_allafrica(self, url):
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Referer': self.base_url_allafrica
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            self.scrape_allafrica(soup)
        else:
            print(f"Failed to retrieve page: {url}")

    def scrape_allafrica(self, soup):
        articles = soup.select('.container.mid .row .col-tn-12.col-sm-8.column.main .section.box.headlines.two-column .content .stories li a')
        
        for article in articles:
            title = article.get('title')
            link = article.get('href')
            
            if link and not link.startswith('http'):
                link = self.base_url_allafrica + link
            
            if link:
                self.parse_article(link, title)
                time.sleep(random.uniform(1, 3))  # Random delay between requests

    def parse_article(self, url, title):
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Referer': self.base_url_allafrica
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.select('.container.mid .row .col-tn-12.col-sm-8.column.main .story-body p')
            
            body = ' '.join([p.get_text(strip=True) for p in paragraphs]).strip()
            org_link = soup.select_one('.container.mid .row .col-tn-12.col-sm-8.column.main .story-footer-link .source-url')
            org_link = org_link.get('href') if org_link else None

            self.data.append({
                'TITLE': title,
                'COUNTRY': self.country,
                'BODY': body,
                'Website Link': org_link
            })
        else:
            print(f"Failed to retrieve article: {url}")

    def closed(self):
        df = pd.DataFrame(self.data)
        conn = sql.connect('newsData.db')
        df.to_csv('newsData.csv', index=False)
        df.to_sql('news', conn, if_exists='replace', index=False)
        conn.commit()
        conn.close()

# Example usage
if __name__ == "__main__":
    country = 'nigeria'  # Replace with your country of interest
    spider = TrendsNewsSpider(country=country)
    spider.start_requests()
    spider.closed()
