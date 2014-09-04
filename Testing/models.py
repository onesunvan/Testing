from django.db import models

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Test(models.Model):
    name = models.CharField(max_length=30)
    subject = models.ForeignKey(Subject)

    def __unicode__(self):
        return self.name

class Question(models.Model):
    text = models.TextField()
    test = models.ForeignKey(Test)

    def __unicode__(self):
        return self.text

class Variant(models.Model):
    text = models.TextField()
    correct = models.BooleanField()
    question = models.ForeignKey(Question)

    def __unicode__(self):
        return self.text
