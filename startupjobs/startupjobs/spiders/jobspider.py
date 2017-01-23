import scrapy

class JobsSpider(scrapy.Spider):
    name = "startupjobs"
    start_urls = ["http://berlinstartupjobs.com/engineering"]

    def parse(self, response):
        for job in response.css('h2.product-listing-h2'):
            
            yield {
                'title': job.css('a::text').extract_first(),
                'link': job.css('a::attr(href)').extract_first()
            }

