from django.conf import settings
from django.db import models
from datetime import date

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)  
    due_date = models.DateField(null=True, blank=True) 
    priority = models.CharField(max_length=50, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium') 
    assign_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')  
    category = models.CharField(max_length=100, blank=True) 
    created_at = models.DateField(default=date.today)  
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,  
        blank=True  
    )
    
    def __str__(self):
        return f'({self.id}) {self.title}'
class Subtask(models.Model):
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'({self.id}) {self.value} - {self.task.title}'