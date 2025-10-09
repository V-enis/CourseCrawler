# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CcScrapersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# One course 
class CourseItem(scrapy.Item):
    code = scrapy.Field()
    title = scrapy.Field()
    slug = scrapy.Field()
    platform = scrapy.Field()
    provider = scrapy.Field()
    subjects = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    prerequisites = scrapy.Field()
    url = scrapy.Field()
    is_active = scrapy.Field()
    created_at = scrapy.Field()
    active_version = scrapy.Field()