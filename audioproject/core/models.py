from django.db import models

# Create your models here.
class Song(models.Model):
    name = models.CharField(max_length=100, unique=True)
    duration = models.IntegerField()
    uploaded_time = models.DateTimeField()

    class Meta:
        ordering = ('-uploaded_time',)

    def __str__(self):
        return self.name

class Podcast(models.Model):
    name = models.CharField(max_length=100, unique=True)
    duration = models.IntegerField()
    uploaded_time = models.DateTimeField()
    host = models.CharField(max_length=100)
    participants = models.TextField()

    class Meta:
        ordering = ('-uploaded_time',)

    def __str__(self):
        return self.name

class AudioBook(models.Model):

    title = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=100)
    narrator = models.CharField(max_length=100)
    duration = models.IntegerField()
    uploaded_time = models.DateTimeField()

    class Meta:
        ordering = ('-uploaded_time',)

    def __str__(self):
        return self.title