# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from courses.models import Course
from .items import CourseItem


class CcScrapersPipeline:
    def process_item(self, item, spider):
        return item


class DjangoPipeline:
    def process_item(self, item, spider):
        if isinstance(item, CourseItem):
            # Avoid duplicates using url
            Course.objects.get_or_create(
                url=item['url'],
                defaults={
                    "title": item["title"],
                    "provider": item.get("provider", "MIT OCW"),
                    "description": item.get("description", "")
                }
            )
        return item