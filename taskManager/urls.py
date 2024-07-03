from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.account import AccountApiSet
from .views.machine import MachineModelViewSet, MachineBorrowViewSet
from .views.youtholer import YoutholerModelViewSet
from .views.public import PublicApiSet
from .views import views

router = DefaultRouter()
router.register(r'account', AccountApiSet, basename='account')
router.register(r'machine', MachineModelViewSet, basename='machine')
router.register(r'borrow', MachineBorrowViewSet, basename='machine-borrow')
router.register(r'member', YoutholerModelViewSet, basename='member')
router.register(r'public', PublicApiSet, basename='public')

urlpatterns = [
    path('', include(router.urls)),
    # path('Create/', view.Create),
]
