'''
Created on Mar 16, 2016

@author: Dhiwakar
'''
from django.conf.urls import url, include
from django.contrib.auth.models import User
from gogocar2.views import GoGoCarScore
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'Score', GoGoCarScore, 'GoGoCarScore')

urlpatterns = [
    url(r'^', include(router.urls)),
]