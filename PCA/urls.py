from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

app_name = 'PCA'

urlpatterns = [
    url(r'^$', views.pca, name='pca'),
    url(r'predict/', views.predict, name='predict'),
]

urlpatterns += staticfiles_urlpatterns()