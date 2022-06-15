from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.automate, name='automate'),
    path('sendmail', views.sendingMail, name='sendingMail'),
    re_path(r'getTotalDocs/$', views.getTotalDocs, name='getTotalDocs'),
    re_path(r'difference/$', views.differences, name='differences'),
]
