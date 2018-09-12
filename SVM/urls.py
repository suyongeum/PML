from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

app_name = 'SVM'

urlpatterns = [
    url(r'^$', views.svm, name='svm'),
    url(r'check/', views.check, name='check'),
]

urlpatterns += staticfiles_urlpatterns()