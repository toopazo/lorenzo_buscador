from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CorpLasCondesCrawler(CrawlSpider):
    name = 'corplascondes'
    allowed_domains = ['www.corplascondes.cl']
    start_urls = ['https://www.corplascondes.cl/contenidos/transparencia/ley_de_transparencia/compras-adquisiciones.html']
    rules = (Rule(LinkExtractor()),)
