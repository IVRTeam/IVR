from django.conf.urls import url
from . import views

app_name = 'logins'

urlpatterns = [
    # 版本过低
    url(r'^error/$', views.error),
    # 验证码
    url(r'^vertifycode/$', views.vertifycode),
    # 登录检测
    url(r'^loginCheck/$', views.loginCheck),
    url(r'^register/$', views.register),
    url(r'^registerCheck/$', views.registerCheck),
    url(r'^checkUid/$', views.checkUid),
]
