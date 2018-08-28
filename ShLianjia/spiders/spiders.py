import scrapy

from scrapy.http import Request
from ShLianjia.items import ShlianjiaItem

class LianjiaSpider(scrapy.Spider):

    name = "链家"
    start_urls = ['https://sh.lianjia.com/zufang/']

    def parse(self, response):
        item = ShlianjiaItem()
        infos = response.xpath('//div[@class="info-panel"]')

        for info in infos:
            #get place
            place = info.xpath('div/div/a[@class="laisuzhou"]/span/text()').extract()[0].replace('\xa0','')
            # get size
            size = info.xpath('div/div/span[@class="meters"]/text()').extract()[0].replace('\xa0','')
            # get price
            price = info.xpath('div/div[@class="price"]/span/text()').extract()[0] + info.xpath(
                'div/div[@class="price"]/text()').extract()[0]

            item['place'] = place
            item['size'] = size
            item['price'] = price

            yield item  #return data


        for i in range(2, 101):
            url = 'https://sh.lianjia.com/zufang/pg{}'.format(str(i))
            yield Request(url, callback=self.parse) #回调