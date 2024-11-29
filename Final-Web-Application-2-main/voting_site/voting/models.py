from django.db import models
import random
import string

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class VotingForm(models.Model):
    code = models.CharField(max_length=6, default=generate_code, unique=True)

class Question(models.Model):
    form = models.ForeignKey(VotingForm, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)
