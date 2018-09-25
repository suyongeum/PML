from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'CNN'

urlpatterns = [
    url(r'^$', views.cnn, name='cnn'),
    url(r'change/', views.change, name='change'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)