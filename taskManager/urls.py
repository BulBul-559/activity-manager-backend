
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountApiSet
from . import views

router = DefaultRouter()
router.register(r'account', AccountApiSet, basename='account')

urlpatterns = [
    path('', include(router.urls)),
    path('Create/', views.Create),
]
