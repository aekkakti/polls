from django.utils import timezone
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Прошел активацию?')
    avatar = models.ImageField(upload_to='media/')


class Meta(AbstractUser.Meta):
        pass

class Poll(models.Model):
    question = models.TextField()
    option_one = models.CharField(max_length=35)
    option_two = models.CharField(max_length=35)
    option_three = models.CharField(max_length=35)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)
    option_three_count = models.IntegerField(default=0)
    poll_avatar = models.ImageField(upload_to='media/')
    full_description = models.TextField(max_length=254)
    short_description = models.CharField(max_length=30)

    begin_date = models.DateTimeField(default=timezone.now())
    end_date = models.DateTimeField(default=timezone.now()+timedelta(hours=2))



    def total(self):
        return self.option_one_count + self.option_two_count + self.option_three_count

    def __str__(self):
        return self.question

