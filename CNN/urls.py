from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

app_name = 'CNN'

urlpatterns = [
    url(r'^$', views.cnn, name='cnn'),
    #url(r'predict/', views.predict, name='predict'),
]

urlpatterns += staticfiles_urlpatterns()