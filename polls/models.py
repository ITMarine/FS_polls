import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class PollUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)


class Poll(models.Model):
    title = models.CharField(max_length=244)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True)
    description = models.TextField()

    def questions(self):
        if not hasattr(self, '_questions'):
            self._questions = self.question_set.all()
        return self._questions


class Question(models.Model):
    CHOICES = (
        ('single', 'Single'),
        ('multi', 'Multiple'),
        ('text', 'Text'),
    )
    text = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=CHOICES)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)

    def choices(self):
        if not hasattr(self, '_choices'):
            self._choices = self.choice_set.all()
        return self._choices


class Choice(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)


class Answer(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, blank=True, null=True)

