from django.db import models


# Create your models here.
class Card(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=500)
    like = models.IntegerField(default=0)
