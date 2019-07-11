from django.db import models

# Create your models here.

from django.conf import settings
from django.db import models
from django.utils import timezone

class NewUser(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    password1 = models.CharField(max_length= 15)
    password2 = models.CharField(max_length= 15)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

