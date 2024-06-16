from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import User
    
class File(models.Model):

    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    object = models.FileField(null=True,)
    created_at = models.DateTimeField(null=True,)

    def __str__(self):
        return self.object
    
class Route(models.Model):

    file = models.ForeignKey(File, blank=True, null=True, on_delete=models.CASCADE)
    parent = models.TextField(default = '/', null = True)

    def __str__(self):
        return self.parent