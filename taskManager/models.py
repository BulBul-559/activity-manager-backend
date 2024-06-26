from django.db import models


class Sduter(models.Model):
    sdut_id = models.CharField(max_length=20, db_index=True)  # username in User model
    name = models.CharField(max_length=20, null=True)
    college = models.CharField(max_length=20, null=True)
    grade = models.CharField(max_length=20, null=True)
    identity = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    qq_number = models.CharField(max_length=30, null=True)
    birthday = models.DateField(null=True)
    first_login = models.BooleanField(default=True)   # mark whether first login or not


class Youtholer(models.Model):
    origin_info = models.ForeignKey(Sduter, on_delete=models.CASCADE)  # associate sduter info
    sdut_id = models.CharField(max_length=20, db_index=True)  #一个人可能有多个部门，这里不能当主键
    name = models.CharField(max_length=20, null=True)
    department = models.CharField(max_length=20, null=True)
    identity = models.CharField(max_length=20, null=True)  # 试用 正式
    position = models.CharField(max_length=20, default='成员')   # 成员 副部长 部长 站长

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sdut_id', 'department'], name='youthol_id'),
        ]


class Machine(models.Model):

    machine_id = models.IntegerField()

    pass


class MachineRecord(models.Model):

    pass


class TaskRecord(models.Model):

    pass


class Photo(models.Model):

    pass


