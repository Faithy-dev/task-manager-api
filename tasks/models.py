from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

class Category(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories'
    )

    def __str__(self):
        return f"{self.name} ({self.owner.username})"

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    RECURRING_CHOICES = [
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    recurring = models.CharField(max_length=10, choices=RECURRING_CHOICES, default='none')
    shared_with = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='shared_tasks'
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.due_date <= timezone.now():
            raise ValidationError("Due date must be in the future.")

        if self.pk:
            old_task = Task.objects.get(pk=self.pk)
            if old_task.status == 'completed' and self.status != 'completed':
                raise ValidationError("Cannot edit a completed task unless reverting to pending.")

    def save(self, *args, **kwargs):
        is_new_completion = self.status == 'completed' and not self.completed_at

        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status == 'pending':
            self.completed_at = None

        super().save(*args, **kwargs)

        # Log completed task to history
        if is_new_completion:
            TaskHistory.objects.create(
                task=self,
                owner=self.owner,
                title=self.title,
                description=self.description,
                completed_at=self.completed_at
            )

        # Handle recurring tasks
        if self.status == 'completed' and self.recurring != 'none':
            if self.recurring == 'daily':
                new_due_date = self.due_date + timedelta(days=1)
            elif self.recurring == 'weekly':
                new_due_date = self.due_date + timedelta(weeks=1)
            elif self.recurring == 'monthly':
                new_due_date = self.due_date + timedelta(days=30)
            else:
                new_due_date = self.due_date

            Task.objects.create(
                owner=self.owner,
                title=self.title,
                description=self.description,
                due_date=new_due_date,
                priority=self.priority,
                category=self.category,
                recurring=self.recurring,
            )

    def __str__(self):
        return f"{self.title} ({self.owner.username})"

class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='history')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_histories')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed_at = models.DateTimeField()
    logged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History: {self.title} ({self.owner.username})"
