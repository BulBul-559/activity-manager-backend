from django.db import models

# Create your models here.

class Sduter(models.Model):
    # username = models.CharField(max_length=20)
    sdut_id = models.CharField(max_length=20, db_index=True)
    name = models.CharField(max_length=20, null=True)
    college = models.CharField(max_length=20, null=True)
    grade = models.CharField(max_length=20, null=True)
    identity = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    qq_number = models.CharField(max_length=30, null=True)
    birthday = models.DateField(null=True)
    first_login = models.BooleanField(default=True)


class Youtholer(models.Model):
    sdut_id = models.CharField(max_length=20, db_index=True)
    name = models.CharField(max_length=20, null=True)
    department = models.CharField(max_length=20, null=True)
    identity = models.CharField(max_length=20, null=True)
    position = models.CharField(max_length=20, default='成员')
