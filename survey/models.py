from asyncore import poll
from pyexpat import model
from statistics import mode
from django.db import models
from datetime import datetime

# Create your models here.




class Poll(models.Model):
    name = models.TextField(max_length=512, blank=False, default='Test poll', unique=True)
    status = models.BooleanField(default=False, blank=False)
    date = models.DateTimeField(blank=False, default=datetime.now())

    def __str__(self):
        return self.name

class Question(models.Model):
    TYPES = (
        ('single', 'Single choice'),
        ('multiple', 'Multiple choice'),
        ('open', 'Open question'),
        ('location', 'Location'),
        ('age', 'Age'),
        ('integer', 'Integer'),
    )

    uz = models.TextField(max_length=4096, blank=False)
    ru = models.TextField(max_length=4096, blank=True)
    finish = models.BooleanField()
    poll = models.ForeignKey(to=Poll, on_delete=models.SET_NULL, null=True)
    num = models.IntegerField()
    type = models.CharField(choices=TYPES, max_length=128)

    def __str__(self):
        return self.uz

class Answer(models.Model):
    ru = models.TextField(max_length=4096, blank=True)
    uz = models.TextField(max_length=4096, blank=False)
    question = models.ForeignKey(to=Question, on_delete=models.SET_NULL, null=True)
    next_question = models.IntegerField()

    def __str__(self):
        return self.uz

class Response(models.Model):
    answer = models.ForeignKey(to=Answer, on_delete=models.SET_NULL, null=True)
    poll = models.ForeignKey(to=Poll, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=datetime.now())
    user_id = models.IntegerField()


