from django.db import models


# Create your models here.
class Person(models.Model):
    email = models.CharField()
    password = models.CharField()
    phone = models.IntField(default=-1)
    name = models.CharField(default="DEFAULT")
    isLoggedOn = models.BoolField(default=False)


class Administrator(Person):
    def __init__(self):
        super()


class Supervisor(Person):
    def __init__(self):
        super()
