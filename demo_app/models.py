from django.db import models


class Document(models.Model):
    text = models.CharField(max_length=200)
