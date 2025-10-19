from django.core.management.base import BaseCommand
from tasks.utils import send_due_task_notifications

class Command(BaseCommand):
    help = 'Send email notifications for tasks due soon'

    def handle(self, *args, **kwargs):
        send_due_task_notifications()
        self.stdout.write(self.style.SUCCESS('Notifications sent successfully!'))
