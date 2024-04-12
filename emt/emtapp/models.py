from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    user_type_choices = (
        ('Admin', 'Admin'),
        ('Lead', 'Lead'),
        ('Employee', 'Employee')
    )
    user_type = models.CharField(max_length=20, choices=user_type_choices)

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    assignee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_by')

    def __str__(self):
        return self.title

class Admin(models.Model):
    task_priority_choice = (
        ('Normal', 'Normal'),
        ('Intermediate', 'Intermediate'),
        ('Critical', 'Critical')
    )
    task_status_choice = (
        ('Pending', 'Pending'),
        ('Acknowledge', 'Acknowledge'),
        ('Completed', 'Completed')
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    priority = models.CharField(max_length=20, choices=task_priority_choice)
    status = models.CharField(max_length=20, choices=task_status_choice)

    def __str__(self):
        return f"{self.user.username} (Admin)"

class Lead(models.Model):
    task_priority_choice = (
        ('Normal', 'Normal'),
        ('Intermediate', 'Intermediate'),
        ('Critical', 'Critical'))
    task_status_choice = (
        ('Pending', 'Pending'),
        ('Acknowledge', 'Acknowledge'),
        ('Completed', 'Completed')
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    task_detail=models.ForeignKey(Task,on_delete=models.CASCADE)
    priority = models.CharField(max_length=20, choices=task_priority_choice)
    status = models.CharField(max_length=20, choices=task_status_choice)
    
    def __str__(self):
        return f"{self.user.username} (Lead)"

class Employee(models.Model):
    task_priority_choice = (
        ('Normal', 'Normal'),
        ('Intermediate', 'Intermediate'),
        ('Critical', 'Critical')
    )
    task_status_choice = (
        ('Normal', 'Normal'),
        ('Intermediate', 'Intermediate'),
        ('Critical', 'Critical')
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    task_to_do = models.ForeignKey(Task, on_delete=models.CASCADE)
    priority = models.CharField(max_length=20, choices=task_priority_choice)
    status = models.CharField(max_length=20, choices=task_status_choice)

    def __str__(self):
        return f"{self.user.username} (Employee)"

