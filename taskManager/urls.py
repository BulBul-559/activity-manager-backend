from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.account import AccountApiSet
from .views.machine import MachineModelViewSet, MachineBorrowViewSet
from .views.youtholer import YoutholerModelViewSet
from .views.activity import ActivityModelViewSet, ActivityEntryModelViewSet
from .views.public import PublicApiSet
from .views.photo import RawPhotoModelViewSet
from .views.photo import PhotoProfileModelViewSet
from .views import views

router = DefaultRouter()
router.register(r'account', AccountApiSet, basename='account')
router.register(r'machine', MachineModelViewSet, basename='machine')
router.register(r'borrow', MachineBorrowViewSet, basename='machine-borrow')
router.register(r'member', YoutholerModelViewSet, basename='member')
router.register(r'activity', ActivityModelViewSet, basename='activity')
router.register(r'public', PublicApiSet, basename='public')
router.register(r'rawphoto', RawPhotoModelViewSet, basename='rawphoto')
router.register(r'profile', PhotoProfileModelViewSet, basename='profile')
router.register(r'entry', ActivityEntryModelViewSet, basename='entry')

urlpatterns = [
    path('', include(router.urls)),
    path('photoprofile/<int:pk>/download/', PhotoProfileModelViewSet.as_view({'get': 'download'}),
         name='photoprofile-download'),
    # path('Create/', view.Create),
]
