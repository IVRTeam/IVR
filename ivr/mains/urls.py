from django.conf.urls import url
from .import views

app_name = 'mains'


urlpatterns = [
    url(r'^$', views.index),
    url(r'^quit/$', views.quit),
    url(r'^user/$', views.user),
    url(r'^getInfo/$', views.getInfo),
    url(r'^modify/$', views.modify),
    url(r'^uploadImg/$', views.uploadImg),
]