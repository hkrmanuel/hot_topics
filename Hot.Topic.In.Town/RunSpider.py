# run_spider.py
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from newsspider.spiders.news_scraper import TrendsNewsSpider
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from scrapy.utils.log import configure_logging
import logging
import sys

# Configure logging for Scrapy
configure_logging()
logger = logging.getLogger(__name__)

def run_spider(country):
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    @inlineCallbacks
    def crawl():
        try:
            yield process.crawl(TrendsNewsSpider, country=country)
            process.start()
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    crawl()
