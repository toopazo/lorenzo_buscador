from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
# import extruct

# This 'spider' can be executed on
#   lorenzo_buscador/scrapy_crawler/scrapy_crawler/spiders$
# uisng
#   scrapy crawl corplascondes --logfile corplascondes.log \
#   -o corplascondes.jl -t jsonlines


class CorpLasCondesCrawler(CrawlSpider):
    name = 'corplascondes'
    allowed_domains = ['www.corplascondes.cl']
    start_urls = ['https://www.corplascondes.cl/contenidos/transparencia/'
                  'ley_de_transparencia/compras-adquisiciones.html']
    rules = (
        Rule(
            LinkExtractor(),
            callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):
        _ = self
        return {
            'url': response.url,
            # 'metadata': extruct.extract(
            #     response.text,
            #     response.url,
            #     syntaxes=['opengraph', 'json-ld']
            # ),
        }
