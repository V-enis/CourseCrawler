# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from apps.courses.models import Course, Subject, Platform, Provider
from asgiref.sync import sync_to_async


class SaveToDjangoPipeline:
    async def process_item(self, item, spider):
        # Avoid duplicates
        course, _ = await sync_to_async(Course.objects.get_or_create)(url=item['url'])

        # Update fields
        course.title = (item.get('title') or [''])[0].strip()
        course.description = (item.get('description') or [''])[0].strip()
        course.learning_outcomes = item.get('learning_outcomes', [])
        course.prerequisites = (item.get('prerequisites') or "").strip()

        # Handle platform
        platform_name = (item.get('platform') or [''])[0].strip()
        if platform_name:
            platform, _ = await sync_to_async(Platform.objects.get_or_create)(name=platform_name)
            course.platform = platform
        else:
            course.platform = None

        # Handle Provider
        provider_name = (item.get('provider') or [''])[0].strip()
        if provider_name:
            provider, _ = await sync_to_async(Provider.objects.get_or_create)(name=provider_name)
            course.provider = provider
        else:
            course.provider = None

        await sync_to_async(course.save)()

        # Handle subjects (ManyToMany)
        subjects = []
        for subj_name in item.get('subjects', []):
            subject, _ = await sync_to_async(Subject.objects.get_or_create)(name=subj_name.strip())
            subjects.append(subject)

        await sync_to_async(course.subjects.set)(subjects)
        await sync_to_async(course.save)()


        return item

