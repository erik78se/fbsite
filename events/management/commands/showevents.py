from django.core.management.base import BaseCommand, CommandError
from happenings.models import Event

# How this was created:
# ./manage.py showevents 1
# https://docs.djangoproject.com/en/1.11/howto/custom-management-commands/


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('event_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for event_id in options['event_id']:
            try:
                event = Event.objects.get(pk=event_id)
            except Event.DoesNotExist:
                raise CommandError('Event "%s" does not exist' % event_id)

            
            # event.save()
            self.stdout.write(self.style.SUCCESS(event.location.get(id=1)))
            self.stdout.write(self.style.SUCCESS('Successfully read event "%s"' % event.title))
