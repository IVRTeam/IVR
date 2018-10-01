from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create_code/$', views.create_code_img),
    url(r'^test_code/$', views.test_code),
]