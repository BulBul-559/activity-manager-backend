from django.db import models
from django.db import models
from django.core.exceptions import ValidationError


# def validate_existing_file(value):
#     if not value:
#         return
#     from django.core.files.storage import default_storage
#     if not default_storage.exists(value):
#         raise ValidationError(f"The file '{value}' does not exist.")
#
# class RawPhoto(models.Model):
#     name = models.CharField(max_length=100)
#     shoot_time = models.DateTimeField(null=True, blank=True)
#     upload_time = models.DateTimeField(auto_now_add=True)
#     uploader = models.ForeignKey(Youtholer, on_delete=models.CASCADE)
#     modify_time = models.DateTimeField(auto_now=True)
#     upload_photo = models.FileField(upload_to='')
#     existing_photo = models.FilePathField(path='/path/to/existing/images', match='*.jpg', recursive=True, blank=True, null=True, validators=[validate_existing_file])
#
#     def save(self, *args, **kwargs):
#         if self.upload_photo and self.existing_photo:
#             raise ValidationError("You can only use either 'uploaded_image' or 'existing_image_path', not both.")
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.name

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
    model = models.CharField(max_length=50)
    purchase_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000)


class MachineAlloc(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    youtholer = models.ForeignKey(Youtholer, on_delete=models.CASCADE)
    allocation_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(null=True)
    is_valid = models.BooleanField(default=True)
    reason = models.CharField(default='', max_length=1000)


class Task(models.Model):
    name = models.CharField(max_length=100)
    organizer = models.ForeignKey(Youtholer, on_delete=models.CASCADE)
    member = models.ManyToManyField(Youtholer)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    is_valid = models.BooleanField(default=True)


class RawPhoto(models.Model):
    name = models.CharField(max_length=100)
    shoot_time = models.DateTimeField(null=True, blank=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(Youtholer, on_delete=models.CASCADE)
    modify_time = models.DateTimeField(auto_now=True)
    path = models.FilePathField(path='/path/to/existing/images', match='*.jpg', recursive=True, blank=True, null=True)

    def __str__(self):
        return self.name


class PhotoProfile(models.Model):
    origin = models.ForeignKey(RawPhoto, on_delete=models.CASCADE)
    path = models.FilePathField(path='')


class FinalPhoto(models.Model):
    origin = models.ForeignKey(RawPhoto, on_delete=models.SET_NULL)
    uploader = models.ForeignKey(Youtholer, on_delete=models.DO_NOTHING)
    path = models.FileField(upload_to='')
    upload_time = models.DateTimeField(auto_now_add=True)



