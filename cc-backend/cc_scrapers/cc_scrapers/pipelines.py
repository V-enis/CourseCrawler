from apps.courses.models import Course, Subject, Platform, Provider
from asgiref.sync import sync_to_async

class SaveToDjangoPipeline:
    @sync_to_async
    def process_item_in_db(self, item):
        course, created = Course.objects.update_or_create(
            url=item.get('url'),
            defaults={
                'code': item.get('code'),
                'title': item.get('title'),
                'description': item.get('description'),
                'learning_outcomes': item.get('learning_outcomes', []),
                'prerequisites': item.get('prerequisites', ''),
            }
        )

        needs_save = False

        # Handle Platform (ForeignKey)
        platform_name = item.get('platform')
        if platform_name:
            platform, _ = Platform.objects.get_or_create(name=platform_name)
            if course.platform != platform:
                course.platform = platform
                needs_save = True
        
        # Handle Provider (ForeignKey)
        provider_name = item.get('provider')
        if provider_name:
            provider, _ = Provider.objects.get_or_create(name=provider_name)
            if course.provider != provider:
                course.provider = provider
                needs_save = True
        
        if needs_save:
            course.save(update_fields=['platform', 'provider'])
            
        subject_names = item.get('subjects', [])
        if subject_names:
            current_subjects = set(course.subjects.values_list('name', flat=True))
            new_subjects = set(s.strip() for s in subject_names)
            
            # Only update the database if the subjects have actually changed.
            if current_subjects != new_subjects:
                subjects = []
                for name in new_subjects:
                    subject, _ = Subject.objects.get_or_create(name=name)
                    subjects.append(subject)
                course.subjects.set(subjects)
        
        return item

    async def process_item(self, item, spider):
        return await self.process_item_in_db(item)