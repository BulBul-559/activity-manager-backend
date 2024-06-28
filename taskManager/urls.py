
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountApiSet
from .views import MachineModelViewSet
from . import views

router = DefaultRouter()
router.register(r'account', AccountApiSet, basename='account')
router.register(r'machine', MachineModelViewSet, basename='machine')

urlpatterns = [
    path('', include(router.urls)),
    path('Create/', views.Create),
]
