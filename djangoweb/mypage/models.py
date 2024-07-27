from django.db import models

class pbreport(models.Model):
    contact_time = models.TextField(null=False)
    channel = models.CharField(max_length=20)
    security = models.CharField(max_length=10)
    purpose = models.TextField(max_length=50, null=False)
    content = models.TextField(max_length=500, null=False)
    future_task = models.TextField()
