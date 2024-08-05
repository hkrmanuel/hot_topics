import scrapy
import pycountry
import pandas as pd
import random
import time
import sqlite3 as sql
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class TrendsNewsSpider(scrapy.Spider):
    name = 'trends_news'
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # Default delay of 2 seconds
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 1,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'newsspider.middlewares.RandomUserAgentMiddleware': 400,
        }
    }
    
    def __init__(self, *args, **kwargs):
        super(TrendsNewsSpider, self).__init__(*args, **kwargs)
        self.data = []

    def start_requests(self):
        country = getattr(self, 'country', None)
        if country is not None:
            '''if ' ' in country:
                country1 = country.replace(' ', '-')
                url = 'https://trends24.in/' + country1.lower() + '/'
            else:
                url = 'https://trends24.in/' + country.lower() + '/'''
            url_allafrica = f'https://allafrica.com/{country.lower()}/'
            
            #yield scrapy.Request(url=url, callback=self.parse_trends, meta={'country': country})
            yield scrapy.Request(url=url_allafrica, callback=self.parse_allafrica, meta={'country': country})
        else:
            self.log("No country provided")

    '''def parse_trends(self, response):
        country = response.meta['country']
        trend_list = response.css('.list-container .trend-card__list')
        trends = []
        for trend in trend_list[0].css('li a::text').getall():
            trends.append(trend.strip())
        
        self.log(f"Top 50 trends in {country}:")
        for trend in trends[:50]:
            self.log(trend)
            #time.sleep(random.uniform(1, 3))  # Random delay between requests'''
    
    def parse_allafrica(self, response):
        country = response.meta['country']
        self.log(f"Scraping AllAfrica for {country}")
        
        articles = response.css('.container.mid .row .col-tn-12.col-sm-8.column.main .section.box.headlines.two-column .content .stories li a')
        
        for article in articles:
            title = article.css('::attr(title)').get()
            link = article.css('::attr(href)').get()
            
            if link and not link.startswith('http'):
                link = response.urljoin(link)
            
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'title': title, 'country': country})
            time.sleep(random.uniform(1, 2))  # Random delay between requests

    def parse_article(self, response):
        title = response.meta['title']
        country = response.meta['country']
        
        paragraphs = response.css('.container.mid .row .col-tn-12.col-sm-8.column.main .story-body p::text').getall()
        
        body = ' '.join(paragraphs).strip()
        
        org_link = response.css('.container.mid .row .col-tn-12.col-sm-8.column.main .story-footer-link .source-url::attr(href)').get()

        self.data.append({
            'TITLE': title,
            'COUNTRY': country,
            'BODY': body,
            'Website Link': org_link
        })

    def closed(self, reason):
        df = pd.DataFrame(self.data)
        conn = sql.connect('newsData.db')
        df.to_csv('newsData.csv', index=False)
        df.to_sql('news', conn, if_exists='replace', index=False)
        conn.commit()
        conn.close()