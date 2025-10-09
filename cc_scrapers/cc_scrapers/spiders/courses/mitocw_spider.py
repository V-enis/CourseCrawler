import scrapy
from scrapy_playwright.page import PageMethod

class MITCoursesScrollSpider(scrapy.Spider):
    name = "mit_courses_scroll"
    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 120000,
        "DOWNLOAD_HANDLERS": {
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
    }

    def start_requests(self):
        yield scrapy.Request(
            "https://ocw.mit.edu/courses/",
            meta={"playwright": True, "playwright_include_page": True},
            callback=self.parse_courses,
        )

    async def parse_courses(self, response):
        page = response.meta["playwright_page"]
        last_height = 0

        self.logger.info("Scrolling to load all courses...")

        while True:
            # Scroll to the bottom
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)  # wait for new items

            # Check if more courses loaded
            new_height = await page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # After scrolling finishes, extract full page HTML
        content = await page.content()
        await page.close()

        response = response.replace(body=content)

        count = 0
        for course in response.css("article .learning-resource-card"):
            title = course.css('.lr-row.course-title span[id^="search-result-"]::text').get()
            url = course.css('.lr-row.course-title a::attr(href)').get()
            professors = course.css('.lr-subtitle.listitem .content a[href*="q=%22"]::text').getall()
            topics = course.css('.lr-subtitle.listitem.topics-list .content a.topic-link::text').getall()
            level = course.css('.lr-row.resource-header .resource-type::text').get()

            count += 1
            yield {
                "title": title.strip() if title else None,
                "url": response.urljoin(url) if url else None,
                "professors": [p.strip() for p in professors],
                "topics": [t.strip() for t in topics],
                "level": level.strip() if level else None,
            }

        self.logger.info(f"✅ Extracted {count} courses in total.")
