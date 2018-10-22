from django.conf.urls import url
from .import views

app_name = 'mains'

urlpatterns = [
    url(r'^$', views.index),
    url(r'^quit/$', views.quit),
    url(r'^modify/$', views.modify),
]