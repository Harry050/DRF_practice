from django.db import models

# Create your models here.

class Articles(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    emails = models.EmailField(max_length=100)
    date_time = models.DateField(auto_now_add=True)

    def __str__(self):
        self.title