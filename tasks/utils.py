from django.core.mail import send_mail
from django.utils import timezone
from .models import Task

def send_due_task_notifications():
    now = timezone.now()
    upcoming_tasks = Task.objects.filter(
        status='pending',
        due_date__lte=now + timezone.timedelta(hours=24),
        due_date__gte=now
    )
    for task in upcoming_tasks:
        subject = f"Task Reminder: {task.title}"
        message = f"Hi {task.owner.username},\n\nYour task '{task.title}' is due on {task.due_date}.\n\nDescription: {task.description}"
        send_mail(subject, message, 'taskmanager@example.com', [task.owner.email])
