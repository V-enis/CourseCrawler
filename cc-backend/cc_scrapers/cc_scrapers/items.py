import scrapy
from itemloaders.processors import MapCompose, TakeFirst 
from w3lib.html import remove_tags

def extract_course_code(text):
    """
    Takes the raw text like '6.189 | January IAP 2008...' and returns just '6.189'.
    """
    if text:
        # Split the string by the '|' character, take the first piece, and strip whitespace.
        return text.split('|')[0].strip()
    return None


class CourseItem(scrapy.Item):
    # TakeFirst to ensure the final output is a single string
    code = scrapy.Field(
        input_processor=MapCompose(remove_tags, extract_course_code),
        output_processor=TakeFirst() 
    )
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst() 
    )
    url = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst() 
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst() 
    )
    platform = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst() 
    )
    provider = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    prerequisites = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst() 
    )

    # These fields can have multiple values
    learning_outcomes = scrapy.Field(input_processor=MapCompose(remove_tags))
    subjects = scrapy.Field(input_processor=MapCompose(remove_tags))