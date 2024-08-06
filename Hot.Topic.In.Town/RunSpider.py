# run_spider.py
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from newsspider.spiders.news_scraper import TrendsNewsSpider
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from scrapy.utils.log import configure_logging
import logging

# Configure logging for Scrapy
configure_logging()
logger = logging.getLogger(__name__)

def run_spider(country):
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    @inlineCallbacks
    def crawl():
        try:
            yield runner.crawl(TrendsNewsSpider, country=country)
            runner.start()
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    crawl()



'''if __name__ == "__main__":
    country = sys.argv[1]
    run_spider(country)'''
