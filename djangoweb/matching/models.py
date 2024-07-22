import datetime
from django.db import models
from django.utils import timezone

class crawling(models.Model):
    date = models.DateField('date published')
    title = models.CharField(max_length=100)
    link = models.URLField(max_length=1024)
    content = models.TextField(max_length=2000)
    summary = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)

class easy_summary(models.Model):
    title = models.ForeignKey(crawling, on_delete=models.CASCADE)
    summary = models.TextField(max_length=2000)
    easy = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        return self.easy