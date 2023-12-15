from django.utils import timezone
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Прошел активацию?')
    avatar = models.ImageField(upload_to='media/')


class Meta(AbstractUser.Meta):
        pass

class Poll(models.Model):
    question = models.TextField()
    poll_avatar = models.ImageField(upload_to='media/')
    full_description = models.TextField(max_length=254)
    short_description = models.CharField(max_length=30)

    begin_date = models.DateTimeField(default=timezone.now())
    end_date = models.DateTimeField(default=timezone.now()+timedelta(hours=2))

    def is_expired(self):
        return timezone.now() > self.end_date

    def __str__(self):
        return self.question

class Choice(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField()

    def __str__(self):
        return self.choice_text

class Voter(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

