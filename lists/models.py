from django.db import models

class List(models.Model):
    pass


class Item(models.Model):
    number = models.IntegerField(default=0)
    guessnumber = models.IntegerField(default=0)
    result = models.TextField(default='')
    list = models.ForeignKey(List, default=None)
