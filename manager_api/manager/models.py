from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import User
    
class Project(models.Model):

    name = models.CharField(max_length = 50, unique=True)
    description = models.TextField(null = True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length = 50) #choices = STATUSES
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    created_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Team(models.Model):

    name = models.CharField(max_length = 50, unique=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.name
    
class Task(models.Model):

    PRIORITISE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )

    STATUSES = (
        ('N', 'New'),
        ('P', 'In progress'),
        ('C', 'Checkout'),
        ('E', 'Ended'),
    )

    name = models.CharField(max_length = 50)
    description = models.TextField(null = True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    priority = models.CharField(max_length = 1, choices = PRIORITISE)
    status = models.CharField(choices = STATUSES, max_length = 1)
    group = models.CharField(max_length = 50)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='executor', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.name, self.pk)

    
class UserToProject(models.Model):

    user = models.ForeignKey(User, related_name='participant', blank=True, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.user.email, self.project.name)

class UserToTeam(models.Model):

    user = models.ForeignKey(User, related_name='participant', blank=True, null=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.user.email, self.team.name)   
    
class TeamToProject(models.Model):

    team = team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.team.name, self.project.name)
    
class ProjectInvites(models.Model):

    user_sent = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    user_get = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    message = models.CharField(max_length = 50)

    def __str__(self):
        return self.pk
    
class TeamInvites(models.Model):

    user_sent = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    user_get = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    message = models.CharField(max_length = 50)

    def __str__(self):
        return self.pk
    
class TaskComment(models.Model):

    task = models.ForeignKey(Task, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    text = models.CharField(max_length = 255)

    def __str__(self):
        return self.pk
    
class Permissions(models.Model):

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)