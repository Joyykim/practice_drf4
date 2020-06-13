from django.db import models


# Create your models here.
class Card(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=500)
    like = models.IntegerField(default=0)
    owner = models.ForeignKey('auth.User', related_name='cards', on_delete=models.CASCADE)
    is_reported = models.BooleanField(default=False)
