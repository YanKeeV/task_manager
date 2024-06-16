from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import User
    
class Project(models.Model):

    name = models.CharField(max_length = 50, unique=True)
    description = models.TextField(null = True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length = 50) #choices = STATUSES
    start_date = models.DateTimeField(null=True,)
    finish_date = models.DateTimeField(null=True,)
    created_at = models.DateTimeField(null=True,)
    finished_at = models.DateTimeField(null=True,)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.name, self.pk)
    
class Team(models.Model):

    name = models.CharField(max_length = 50, unique=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.name
    
class Task(models.Model):

    PRIORITISE = (
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    )

    STATUSES = (
        ('N', 'New'),
        ('P', 'In progress'),
        ('C', 'Checkout'),
        ('F', 'Finished'),
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

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.user.email, self.team.name)   
    
class TeamToProject(models.Model):

    team = team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.team.name, self.project.name)
    
class ProjectInvite(models.Model):

    user_sent = models.ForeignKey(User, related_name='manager', blank=True, null=True, on_delete=models.CASCADE)
    user_get = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    message = models.CharField(max_length = 50, null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.project.name, self.user_get.email)
    
class TeamInvite(models.Model):

    user_sent = models.ForeignKey(User, related_name='sender', blank=True, null=True, on_delete=models.CASCADE)
    user_get = models.ForeignKey(User, related_name='recipient', blank=True, null=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    message = models.CharField(max_length = 50, null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.team.name, self.user_get.email)
    
class TaskComment(models.Model):

    task = models.ForeignKey(Task, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    text = models.CharField(max_length = 255)

    def __str__(self):
        return str(self.pk)
    
class Permissions(models.Model):

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    can_invite_user = models.BooleanField(default=False)
    can_kick_user = models.BooleanField(default=False)
    can_edit_user_permissions = models.BooleanField(default=False)
    can_create_task = models.BooleanField(default=False)
    can_delete_task = models.BooleanField(default=False)
    can_edit_task = models.BooleanField(default=False)
    can_checkout_task = models.BooleanField(default=False)
    can_set_user_to_task = models.BooleanField(default=False)
    can_delete_project = models.BooleanField(default=False)
    can_edit_project = models.BooleanField(default=False)
    can_finish_project = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.user.email, self.project.pk)