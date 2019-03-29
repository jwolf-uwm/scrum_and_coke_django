from django.db import models


# Create your models here.
class Person(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    phone = models.IntegerField(default=-1)
    name = models.CharField(max_length=50, default="DEFAULT")
    isLoggedOn = models.BooleanField(default=False)


class Administrator(Person):
    def __init__(self):
        super()


class Supervisor(Person):
    def __init__(self):
        super()
