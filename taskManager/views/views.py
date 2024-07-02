from django.http import HttpResponse
from django.contrib.auth.models import User

from ..models import Sduter
from ..models import Youtholer

def Create(request):
    """
        Sign up to the system.
        Here just a simple example.
    """
    username = 'sunorain'
    password = 'youthol'
    email = "1079729701@qq.com"
    User.objects.create_user(username, email, password)

    sdut_id = 'sunorain'
    name = '小悠'
    college = '山东理工大学'
    grade = '214'
    identity = '学生'
    sduter = Sduter.objects.create(sdut_id=sdut_id, name=name, college=college,
                                    grade=grade,identity = identity)
    department = '管理组'
    identity = '管理员'
    youtholer = Youtholer.objects.create(origin_info=sduter, sdut_id=sdut_id, name=name, department=department, identity=identity)
    youtholer.save()

    return HttpResponse('success')

