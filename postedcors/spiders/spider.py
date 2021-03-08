import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import PostedcorsItem
from itemloaders.processors import TakeFirst


class PostedcorsSpider(scrapy.Spider):
	name = 'postedcors'
	start_urls = ['http://www.posted.co.rs/novosti.html']

	def parse(self, response):
		post_links = response.xpath('//div[contains(@id, "CollapsiblePanel")]')
		for post in post_links:
			title = post.xpath('./div[@class="CollapsiblePanelTab"]/text()[normalize-space()and not(ancestor::em)]').get()
			description = post.xpath('./div[@class="CollapsiblePanelContent"]//text()[normalize-space()]').getall()
			description = [remove_tags(p).strip() for p in description]
			description = ' '.join(description).strip()
			date = post.xpath('./div[@class="CollapsiblePanelTab"]/em/text()').get()

			item = ItemLoader(item=PostedcorsItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()
