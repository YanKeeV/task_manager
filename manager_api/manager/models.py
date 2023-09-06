from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    
    username = None
    email = models.EmailField(_("email address"), unique=True)
    status = models.CharField(max_length = 255, default = '')
    role = models.CharField(max_length = 50, default = '')


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Project(models.Model):

    # STATUSES = (
    #     ('N', 'New'),
    #     ('P', 'In progress'),
    #     ('C', 'Checkout'),
    #     ('E', 'Ended'),
    # )

    name = models.CharField(max_length = 50, unique=True)
    password = models.CharField(max_length = 50)
    description = models.TextField(null = True)
    status = models.CharField(max_length = 50) #choices = STATUSES
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

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

    ROLES = (
        ('O', 'Owner'),
        ('A', 'Admin'),
        ('W', 'Worker'),
    )

    user = models.ForeignKey(User, related_name='participant', blank=True, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    project_role = models.CharField(max_length = 50, choices = ROLES)

    def __str__(self):
        return '%s - %s' % (self.user.email, self.project.name)