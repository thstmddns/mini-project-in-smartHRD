from django.db import models

# Create your models here.
class Member(models.Model):
    #중복제거 unique=True 유일해야 한다 
    mem_id = models.CharField(max_length=100, unique=True)
    mem_password = models.IntegerField()
    mem_type = models.CharField(max_length=100)
    mem_age = models.IntegerField()
    mem_name = models.CharField(max_length=100)
    wdate = models.DateTimeField()