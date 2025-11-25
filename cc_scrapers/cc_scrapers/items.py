# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose
from w3lib.html import remove_tags

# One course 
class CourseItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(remove_tags,))

    url = scrapy.Field(
        input_processor=MapCompose(
            remove_tags,
            lambda url, response=None: response.urljoin(url) if response else url
            )
    )
    
    description = scrapy.Field(input_processor=MapCompose(remove_tags))
    learning_outcomes = scrapy.Field(input_processor=MapCompose(remove_tags))
    platform = scrapy.Field(input_processor=MapCompose(remove_tags))
    provider = scrapy.Field(input_processor=MapCompose(remove_tags))
    prerequisites = scrapy.Field(input_processor=MapCompose(remove_tags))
    subjects = scrapy.Field(input_processor=MapCompose(remove_tags))



