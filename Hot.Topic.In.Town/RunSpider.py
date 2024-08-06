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
    d = crawl(runner, country)
    d.addBoth(lambda _: reactor.stop())
    reactor.run(installSignalHandlers=False)



'''if __name__ == "__main__":
    country = sys.argv[1]
    run_spider(country)'''
