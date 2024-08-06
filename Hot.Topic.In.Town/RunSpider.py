from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from newsspider.spiders.news_scraper import TrendsNewsSpider
from scrapy.utils.log import configure_logging

# Configure logging for Scrapy
configure_logging()

@inlineCallbacks
def crawl(runner, country):
    yield runner.crawl(TrendsNewsSpider, country=country)
    reactor.stop()

def run_spider(country):
    runner = CrawlerRunner(get_project_settings())
    # Call the crawl function and start the reactor
    reactor.callLater(0, lambda: crawl(runner, country))
    reactor.run(installSignalHandlers=False)



'''if __name__ == "__main__":
    country = sys.argv[1]
    run_spider(country)'''
