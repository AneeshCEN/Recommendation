from django.conf.urls import url, include
from django.contrib.auth.models import User
from .views import GoGoCarScore
from rest_framework import routers
 
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'Score', GoGoCarScore, 'GoGoCarScore')

urlpatterns = [
    url(r'^', include(router.urls)),
]