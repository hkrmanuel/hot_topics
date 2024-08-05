import random
from scrapy import signals
from scrapy.exceptions import IgnoreRequest

class NewsspiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class NewsspiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent= [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36',
        ]

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.user_agent))
        
class RandomProxyMiddleware:
    def __init__(self):
        # Load proxies from file
        self.PROXY_LIST = self.load_proxies()

    def load_proxies(self):
        # Read proxies from the file
        with open(' proxy_list.txt', 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
        return proxies

    def process_request(self, request, spider):
        # Select a random proxy
        proxy = random.choice(self.PROXY_LIST)
        request.meta['proxy'] = proxy

import random

class RandomProxyMiddleware:
    PROXY_LIST = [
        "http://46.3.80.5:80",
        "http://45.8.21.156:80",
        "http://51.250.13.88:80",
        "http://37.27.82.72:80",
        "http://190.92.227.158:443",
        "http://119.59.99.73:8888",
        "http://5.35.92.156:80",
        "http://123.30.154.171:7777",
        "http://130.0.234.31:8080",
        "http://108.170.12.11:80",
        "socks4://67.43.228.250:1587",
        "socks4://212.57.43.245:4153",
        "http://8.211.42.167:3128",
        "http://106.51.62.106:8080",
        "http://5.161.115.29:51111",
        "http://185.217.198.121:4444",
        "http://67.43.228.253:9737",
        "http://58.20.248.139:9002",
        "socks4://72.167.221.157:47936",
        "socks4://192.111.135.17:18302",
        "http://188.40.59.208:3128",
        "http://155.94.241.134:3128",
        "http://67.43.227.228:29187",
        "http://139.162.78.109:8080",
        "http://122.175.19.164:80",
        "http://66.29.154.103:3128",
        "http://39.109.113.97:3128",
        "http://185.217.143.96:80",
        "socks4://137.184.182.145:13814",
        "socks4://103.94.133.90:4153",
        "socks4://95.128.142.76:1080",
        "http://172.105.197.96:3128",
        "http://189.240.60.168:9090",
        "http://198.176.58.43:80",
        "http://167.102.133.105:80",
        "http://183.215.23.242:9091",
        "http://183.238.163.8:9002",
        "http://185.105.91.62:4444",
        "http://154.203.132.55:8090",
        "socks4://187.62.89.252:4153",
        "http://89.46.249.248:25585",
        "http://45.92.177.60:8080",
        "http://181.41.194.186:80",
        "http://23.247.136.245:80",
        "http://185.105.88.63:4444",
        "socks4://117.74.65.207:443",
        "http://47.76.132.77:1080",
        "http://103.153.154.6:80",
        "http://77.68.100.177:80",
        "http://202.61.204.51:80",
        "socks4://37.221.193.221:31901",
        "http://67.43.227.227:2593",
        "http://119.96.113.193:30000",
        "http://89.145.162.81:3128",
        "http://72.10.160.90:13089",
        "http://67.43.228.253:30467",
        "http://72.10.164.178:8665",
        "http://135.181.154.225:80",
        "http://91.189.177.188:3128",
        "http://152.26.229.57:9443",
        "http://183.60.141.41:443",
        "http://20.204.214.79:3129",
        "http://67.43.227.226:31149",
        "http://103.82.135.177:7005",
        "http://72.10.160.91:28573",
        "http://159.65.0.8:3128",
        "http://189.240.60.171:9090",
        "http://196.223.129.21:80",
        "socks5://117.74.65.207:80",
        "http://172.247.18.4:1080",
        "http://4.236.183.37:8080",
        "http://137.184.100.135:80",
        "http://155.94.241.130:3128",
        "http://51.89.255.67:80",
        "http://20.233.44.207:80",
        "http://94.130.94.45:80",
        "http://89.35.237.187:8080",
        "socks4://115.85.72.202:5678",
        "socks4://36.88.234.186:4153",
        "http://103.133.221.251:80",
        "socks4://197.251.236.226:5678",
        "http://103.87.149.19:80",
        "http://167.102.133.97:80",
        "http://192.53.114.26:80",
        "socks4://178.62.7.98:33399",
        "socks4://89.58.45.94:41532",
        "http://154.0.12.163:80",
        "http://67.43.227.226:11011",
        "http://51.195.40.90:80",
        "http://185.217.199.176:4444",
        "http://20.127.221.223:80",
        "http://217.13.109.78:80",
        "http://72.10.160.172:3601",
        "http://161.35.70.249:3128",
        "http://122.10.225.55:8000",
        "http://72.10.164.178:11357",
        "http://213.169.33.7:4000",
        "http://147.182.180.242:80",
        "http://85.209.153.174:5678",
        "http://67.43.227.228:27761",
        "http://208.109.37.199:80",
        "http://88.80.150.7:3669",
        "socks4://107.152.98.5:4145",
        "http://20.204.212.76:3129",
        "http://85.209.153.173:3128",
        "http://72.10.164.178:24273",
        "http://122.9.183.228:8000",
        "http://115.223.11.212:8103",
        "http://1.94.31.35:8888",
        "socks4://213.252.245.221:6120",
        "http://223.113.80.158:9091",
        "http://80.249.112.162:80",
        "socks4://182.52.70.117:4145",
        "http://178.128.200.87:80",
        "http://67.43.227.227:32745",
        "http://20.44.188.17:3129",
        "http://91.107.183.65:80",
        "http://59.92.211.63:3128",
        "http://45.90.89.20:80",
        "http://20.84.109.185:80",
        "http://39.191.223.109:4096",
        "http://67.43.228.254:31729",
        "http://49.13.51.71:80",
        "http://67.43.236.20:23743",
        "http://188.165.49.152:80",
        "http://50.62.183.223:80",
        "socks5://117.74.65.207:443",
        "http://51.8.224.206:9000",
        "http://195.114.209.50:80",
        "http://154.203.132.49:8090",
        "http://89.35.237.187:8888",
        "http://141.11.40.11:80",
        "http://67.207.78.188:80",
        "http://154.203.132.55:8080",
        "http://85.209.153.175:5678",
        "http://191.101.237.202:3128",
        "http://176.235.136.91:80",
        "socks4://37.220.92.166:31337",
        "http://103.87.149.19:80",
        "http://92.223.10.79:80",
        "socks4://117.74.65.207:80",
        "http://190.196.108.230:8080",
        "http://185.217.143.89:80",
        "http://20.233.37.33:3129",
        "http://118.96.47.158:80",
        "http://212.32.248.92:80",
        "http://170.210.185.162:8080",
        "http://87.120.236.115:80",
        "http://92.118.134.17:80",
        "socks4://92.111.23.64:4166",
        "http://197.255.30.84:80",
        "socks4://182.52.70.117:4153",
        "http://37.49.255.4:80",
        "socks4://119.160.208.26:4153",
        "socks4://45.88.164.13:1981",
        "http://157.245.242.154:8080",
        "socks4://77.247.183.35:4153",
        "http://51.79.144.91:8080",
        "socks4://77.66.81.161:4153",
        "http://183.86.153.27:80",
        "http://194.182.72.106:3128",
        "http://88.80.188.146:8080",
        "http://85.209.153.174:4145",
        "http://43.153.24.178:80",
        "http://47.241.137.179:3128",
        "http://217.182.120.17:80",
        "http://89.36.216.132:80",
        "http://84.38.62.128:3128",
        "socks4://182.16.154.81:9150",
        "socks5://36.67.27.67:1080",
        "http://188.40.94.100:8080",
        "http://157.245.255.2:8080",
        "http://197.231.221.70:8080",
        "http://200.105.215.22:8080",
        "socks4://103.131.99.82:4153",
        "http://180.179.96.195:8080",
        "socks5://45.77.20.84:8888",
        "http://103.78.160.114:80",
        "socks5://43.251.149.62:1080",
        "http://187.0.188.73:80",
        "socks4://139.99.98.109:31568",
        "socks4://159.89.229.95:5678",
        "http://51.81.245.178:3128",
        "socks5://46.32.17.14:1080",
        "socks5://193.169.253.28:1080",
        "http://164.68.110.126:8080",
        "socks4://45.79.37.18:3128",
        "http://179.43.133.24:3128",
        "http://188.166.209.5:3128",
        "socks4://61.7.166.168:4153",
        "http://196.220.102.92:8080",
        "http://178.128.216.46:3128",
        "socks4://193.239.30.57:4153",
        "socks5://183.233.12.60:1080",
        "http://161.35.70.249:80",
        "http://186.236.130.46:8080",
        "http://178.62.193.19:8080",
        "http://103.228.250.28:80",
        "socks4://103.96.221.206:4153",
        "http://49.12.62.102:8080",
        "http://85.209.153.174:4176",
        "socks5://104.248.27.206:1080",
        "http://184.105.182.130:80",
        "http://51.79.143.68:8080",
        "http://194.56.172.116:8080",
        "http://43.139.187.11:8080",
        "http://78.46.30.157:80",
        "http://208.109.9.1:80",
        "http://119.235.246.21:80",
        "http://51.79.119.106:8080",
        "http://195.114.209.12:8080",
        "socks5://160.94.155.220:1080",
        "socks4://182.52.70.117:4145",
        "http://178.62.197.207:8080",
        "http://176.235.136.90:80",
        "http://80.250.250.114:8080",
        "socks5://47.252.8.40:1080",
        "http://192.138.24.189:3128",
        "socks5://206.189.124.212:1080",
        "http://184.105.182.134:8080",
        "socks5://45.79.62.103:1080",
        "http://163.172.213.82:8080",
        "http://191.101.237.202:80",
        "socks5://104.248.212.40:1080",
        "socks5://5.161.115.31:1080",
        "http://119.96.113.193:30000",
        "http://51.79.144.91:8080",
        "socks5://45.79.4.19:1080",
        "socks4://202.58.207.121:4153",
        "http://177.234.42.56:8080",
        "socks5://139.99.98.110:1080",
        "http://103.78.78.13:80",
        "socks4://185.104.186.209:1080",
        "http://185.51.40.232:80",
        "http://170.210.185.161:80",
        "socks5://45.77.253.111:1080",
        "http://103.96.221.206:80",
        "socks4://172.107.76.126:4153",
        "socks4://193.169.253.36:1080",
        "http://200.105.215.22:8080",
        "socks4://119.235.246.21:80",
        "http://163.172.248.161:80",
        "socks5://159.65.0.8:1080",
        "http://164.68.110.125:8080",
        "socks4://178.62.193.19:4153",
        "http://201.151.174.164:80",
        "http://176.235.136.90:80",
        "http://200.90.124.43:8080",
        "socks5://5.9.192.60:1080",
        "http://103.128.185.22:8080",
        "socks5://194.182.72.106:1080",
        "socks4://45.77.48.62:1080",
        "http://109.70.100.2:80",
        "socks4://178.62.7.98:1080",
        "http://47.251.69.116:8080",
        "socks4://188.40.94.100:4153",
        "socks4://161.35.70.249:4153",
        "http://159.89.233.40:8080",
        "http://103.96.221.204:80",
        "socks4://103.99.232.84:5678",
        "http://107.172.228.132:80",
        "socks4://167.99.67.24:1080",
        "socks4://190.92.227.153:4153",
        "socks5://45.79.36.158:1080",
        "socks5://64.140.226.182:1080",
        "socks5://139.99.98.118:1080",
        "socks5://165.227.215.71:1080",
        "socks4://162.243.252.5:4153",
        "http://185.217.144.22:80",
        "socks4://104.248.27.206:1080",
        "http://194.182.72.106:80",
        "http://144.202.9.161:80",
        "http://5.161.115.30:80",
        "http://194.233.87.222:8080",
        "socks4://167.172.37.154:1080",
        "socks5://191.101.237.200:1080",
        "http://51.79.179.118:8080",
        "socks5://159.65.0.7:1080",
        "socks4://138.201.60.113:5678",
        "socks5://165.227.215.70:1080",
        "socks4://195.2.96.233:5678",
        "http://185.217.198.121:80",
        "socks4://82.192.78.110:1080",
        "http://195.221.211.161:8080",
        "socks5://139.59.119.29:1080",
        "socks4://177.92.123.185:5678",
        "http://91.239.237.220:80",
        "socks4://5.161.115.31:4153",
        "http://51.89.255.67:80",
        "socks5://159.65.0.6:1080",
        "http://194.182.72.107:8080",
        "socks4://103.118.13.32:4153",
        "http://190.90.124.32:80",
        "http://189.240.60.171:8080",
        "socks5://51.79.119.102:1080",
        "http://194.233.87.222:3128",
        "socks4://103.132.49.214:4153",
        "http://194.182.72.107:3128",
        "socks5://107.174.51.30:1080",
        "socks4://182.16.154.81:4153",
        "http://194.182.72.106:80",
        "socks4://36.67.27.67:1080",
        "http://39.108.5.51:3128",
        "socks5://206.189.124.212:1080",
        "http://195.114.209.50:80",
        "socks4://198.50.182.18:1080",
        "socks5://185.104.186.208:1080",
        "socks5://45.32.177.161:1080",
        "http://41.139.226.39:8080",
        "socks5://47.252.8.40:1080",
        "http://47.108.146.89:80",
        "socks4://119.235.246.21:5678",
        "socks5://139.59.119.29:1080",
        "http://138.68.96.60:8080",
        "socks4://47.241.137.179:5678",
        "http://37.49.255.4:8080",
        "socks4://103.96.221.204:5678",
        "http://189.240.60.172:9090",
        "socks4://188.40.94.100:5678",
        "http://190.92.227.154:80",
        "http://51.79.119.107:8080",
        "http://49.12.62.102:80",
        "socks4://185.104.186.209:5678",
        "socks5://104.248.27.206:1080",
        "socks5://139.59.119.29:1080",
        "socks4://184.105.182.132:5678",
        "socks4://103.94.138.27:5678",
        "socks5://45.79.37.18:1080",
        "http://197.251.236.226:5678",
        "socks4://115.85.72.202:4153",
        "http://167.102.133.105:80",
        "http://89.45.109.228:8080",
        "http://202.52.77.2:80",
        "http://87.120.236.115:8080",
        "socks4://190.92.227.153:4153",
        "socks4://167.172.89.237:4153",
        "socks4://139.99.98.108:5678",
        "socks4://143.198.99.50:4153",
        "socks4://67.43.228.253:30373",
        "http://37.220.92.166:8080",
        "http://185.217.143.95:8080",
        "socks4://103.97.121.2:4153",
        "socks4://182.52.70.117:4153",
        "socks5://159.65.0.6:1080",
        "socks5://154.202.104.128:1080",
        "socks4://162.243.252.5:4153",
        "http://194.233.87.222:3128",
        "socks5://191.101.237.200:1080",
        "socks5://139.99.98.118:1080",
        "socks4://195.2.96.233:5678",
        "socks4://200.105.215.22:5678",
        "socks5://139.99.98.110:1080",
        "socks4://139.99.98.110:5678",
        "socks4://119.59.99.73:1080",
        "socks5://139.99.98.109:1080",
        "http://182.52.70.117:4153",
        "socks4://182.52.70.117:4153",
        "http://118.96.47.158:80",
        "http://95.128.142.76:1080",
        "http://72.10.164.178:12345",
        "socks5://159.65.0.7:1080",
        "socks5://45.79.4.19:1080",
        "http://194.182.72.106:3128",
        "socks4://45.77.48.62:5678",
        "http://107.172.228.132:80",
        "http://54.86.156.29:80",
        "http://118.96.47.158:3128",
        "http://193.169.253.36:1080",
        "socks5://162.243.252.5:1080",
        "socks5://45.79.37.18:1080",
        "http://94.130.94.45:8080",
        "http://38.132.126.225:8080",
        "socks5://159.65.0.6:1080",
        "socks5://45.79.62.103:1080",
        "socks5://139.59.119.29:1080",
        "socks5://5.161.115.30:1080",
        "socks5://104.248.27.206:1080",
        "socks4://36.67.27.67:1080",
        "socks5://107.152.98.5:1080",
        "socks5://139.59.119.29:1080",
        "socks5://5.161.115.31:1080",
        "socks5://139.59.119.29:1080",
        "socks5://194.182.72.106:1080",
        "socks5://51.79.143.68:1080",
        "socks5://107.152.98.5:1080",
        "socks5://104.248.27.206:1080",
        "http://51.89.179.118:80",
        "socks5://103.228.250.28:1080",
        "socks4://37.49.255.4:1080",
        "socks5://159.65.0.7:1080",
        "socks5://104.248.27.206:1080",
        "socks4://164.68.110.125:4153",
        "http://177.238.250.151:8080",
        "socks5://51.79.144.91:1080",
        "socks5://185.104.186.209:1080",
        "http://118.96.47.158:80",
        "http://191.101.237.200:8080",
        "socks5://139.59.119.29:1080",
        "socks5://45.77.253.111:1080",
        "socks4://103.96.221.204:4153",
        "http://103.96.221.204:3128",
        "socks4://37.220.92.166:4153",
        "http://188.40.94.100:3128",
        "http://178.62.197.207:3128",
        "socks5://139.59.119.29:1080",
        "socks5://139.59.119.29:1080",
        "http://194.182.72.107:3128",
        "socks5://165.227.215.70:1080",
        "socks5://45.79.37.18:1080",
        "socks5://139.59.119.29:1080",
        "http://38.132.126.225:8080",
        "http://187.0.188.73:8080",
        "http://180.179.96.195:8080",
        "socks4://45.79.37.18:4153",
        "socks5://139.59.119.29:1080",
        "socks5://45.79.62.103:1080",
        "socks4://185.104.186.209:4153",
        "socks4://191.101.237.200:4153",
        "socks5://104.248.27.206:1080",
        "socks4://51.79.143.68:5678",
        "http://103.96.221.204:3128",
        "socks5://139.59.119.29:1080",
        "socks5://107.174.51.30:1080",
        "socks4://45.77.37.18:1080",
        "socks5://51.79.119.102:1080",
        "http://194.182.72.107:8080",
        "socks5://165.227.215.71:1080",
        "socks4://51.79.119.107:4153",
        "socks4://104.248.27.206:4153",
        "http://160.94.155.220:8080",
        "socks5://45.79.4.19:1080",
        "socks4://103.96.221.204:4153",
        "http://41.193.94.21:3128",
        "socks5://51.79.119.102:1080",
        "http://94.130.94.45:8080",
        "http://51.79.144.91:8080",
        "socks5://103.124.9.155:1080",
        "http://107.172.228.132:8080",
        "socks4://192.138.24.189:1080",
        "socks5://194.182.72.107:1080",
        "socks4://144.202.9.161:4153",
        "socks5://165.227.215.71:1080",
        "http://186.236.130.46:80",
        "socks4://103.96.221.206:5678",
        "socks4://167.99.67.24:1080",
        "socks5://45.77.62.103:1080",
        "socks5://45.77.253.111:1080",
        "socks4://185.104.186.209:5678",
        "socks4://37.220.92.166:1080",
        "http://37.220.92.166:3128",
        "socks4://182.52.70.117:4153",
        "http://37.220.92.166:8080",
        "http://37.220.92.166:80",
        "socks4://193.169.253.36:1080",
        "socks5://51.79.119.102:1080",
        "socks5://107.174.51.30:1080",
        "socks5://159.65.0.7:1080",
        "socks4://192.138.24.189:1080",
        "socks5://45.79.4.19:1080",
        "http://194.182.72.107:3128",
        "socks4://139.59.119.29:1080",
        "http://37.220.92.166:80",
        "socks4://139.59.119.29:1080",
        "socks4://139.59.119.29:1080",
        "socks5://45.77.48.62:1080",
        "socks5://45.79.37.18:1080",
        "socks4://51.79.119.107:4153",
        "socks5://104.248.27.206:1080",
        "socks5://139.59.119.29:1080",
        "socks4://165.227.215.70:4153",
        "socks5://51.79.119.107:1080",
        "http://179.43.133.24:3128",
        "http://194.182.72.106:3128",
        "socks5://107.152.98.5:1080",
        "socks5://103.118.13.32:1080",
        "socks5://45.79.37.18:1080",
        "http://194.182.72.107:8080",
        "socks5://194.182.72.107:1080",
        "socks5://104.248.27.206:1080",
        "socks5://45.77.48.62:1080",
        "socks5://45.79.37.18:1080",
        "http://189.240.60.171:8080",
        "socks4://37.220.92.166:4153",
        "socks5://45.77.48.62:1080",
        "socks5://45.77.48.62:1080",
        "socks5://45.79.62.103:1080",
        "socks5://107.152.98.5:1080",
        "socks5://107.152.98.5:1080",
        "socks5://139.59.119.29:1080",
        "socks5://107.152.98.5:1080",
        "http://107.172.228.132:8080",
        "http://198.50.182.18:80",
        "socks5://45.77.37.18:1080",
        "socks5://107.152.98.5:1080",
        "socks5://104.248.27.206:1080",
        "socks5://139.59.119.29:1080",
        "socks5://107.152.98.5:1080",
        "socks5://45.79.37.18:1080",
        "http://181.211.72.98:8080",
        "socks5://139.59.119.29:1080",
        "socks5://139.59.119.29:1080",
        "socks5://104.248.27.206:1080",
        "socks5://139.59.119.29:1080",
        "socks5://107.152.98.5:1080",
        "socks5://104.248.27.206:1080",
        "socks5://104.248.27.206:1080",
        "socks5://107.152.98.5:1080",
        "socks5://139.59.119.29:1080",
        "socks5://139.59.119.29:1080",
        "socks5://107.152.98.5:1080",
        "socks5://104.248.27.206:1080",
        "socks5://139.59.119.29:1080",
        "socks5://139.59.119.29:1080",
        "socks5://107.152.98.5:1080",
        "socks5://104.248.27.206:1080",
        "socks5://107.152.98.5:1080",
        "socks5://107.152.98.5:1080",
        "socks5://104.248.27.206:1080",


    ]

    def process_request(self, request, spider):
        proxy = random.choice(self.PROXY_LIST)
        request.meta['proxy'] = proxy
        
USER_AGENT_LIST = [
    # Add your user agents here

    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36'
]