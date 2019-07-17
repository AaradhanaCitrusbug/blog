from django.db import models

# Create your models here.

from django.conf import settings
from django.db import models
from django.utils import timezone

class user_details(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mail_sent_time = models.DateTimeField(default=timezone.now)
    status= models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.user.username


