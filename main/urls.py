from os import name
from django.urls import path,include
from .views import *
urlpatterns = [
    path('', homepage, name='home'),
    path('download', download, name='download'),
]