from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from ...items import CourseItem

class MitOcwSitemapSpider(SitemapSpider):
    name = "mit"
    allowed_domains = ["ocw.mit.edu"]
    sitemap_urls = ["https://ocw.mit.edu/sitemap.xml"]

    sitemap_rules = [
        (r'/courses/[^/]+/?$', 'parse_main'),
    ]

    def parse_main(self, response):
        self.logger.info(f"Parsing main course page: {response.url}")

        il = ItemLoader(item=CourseItem(), response=response)
        il.add_css("title", "title::text")
        il.add_value("url", response.url)
        il.add_css("description", "#expanded-description::text, #full-description::text")
        il.add_css("subjects", "a.course-info-topic::text")
        il.add_value("platform_name", "MIT OpenCourseWare")
        il.add_value("provider_name", "MIT OCW")

        item = il.load_item()

        # Try syllabus first
        syllabus_url = response.url.rstrip("/") + "/pages/syllabus/"
        insights_url = response.url.rstrip("/") + "/pages/instructor-insights/"

        # Check both in order, but yield only one final result
        yield response.follow(
            syllabus_url,
            callback=self.parse_syllabus_or_insights,
            cb_kwargs={"item": item, "fallback_url": insights_url},
            dont_filter=True,
        )

    def parse_syllabus_or_insights(self, response, item, fallback_url):
        # If this page doesn't exist, try the fallback (insights)
        if response.status in [404, 500]:
            self.logger.info(f"No syllabus page for {item['url']}, trying insights.")
            yield response.follow(
                fallback_url,
                callback=self.parse_syllabus_or_insights,
                cb_kwargs={"item": item, "fallback_url": None},
                dont_filter=True,
            )
            return

        # Extract learning outcomes
        headings = [
            "goal", "goals", "objective", "objectives",
            "outcome", "outcomes", "expectation", "expectations"
        ]
        xpaths = [
            f"//h3[contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{word}')]/following-sibling::*[self::ul or self::ol][1]//li/text()"
            for word in headings
        ] + [
            f"//h4[contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{word}')]/following-sibling::*[self::ul or self::ol][1]//li/text()"
            for word in headings
        ]

        learning_outcomes = []
        for xp in xpaths:
            results = response.xpath(xp).getall()
            if results:
                learning_outcomes.extend([r.strip() for r in results if r.strip()])

        item["learning_outcomes"] = learning_outcomes or []

        self.logger.info(f"YIELDING course: {item.get('title')} with {len(item['learning_outcomes'])} outcomes")
        yield item
