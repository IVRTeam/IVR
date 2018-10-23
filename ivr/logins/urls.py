from django.conf.urls import url
from . import views

app_name = 'logins'

urlpatterns = [
    # 登录界面
    # url(r'^$', views.login),
    # 版本过低
    url(r'^error/$', views.error),
    # 验证码
    url(r'^vertifycode/$', views.vertifycode),
    # 登录检测
    url(r'^loginCheck/$', views.loginCheck),
    url(r'^register/$', views.register),
    url(r'^registerCheck/$', views.registerCheck),
    url(r'^testSession/$', views.testSession),
    url(r'^checkUid/$', views.checkUid),
    url(r'^test/$', views.test),
    url(r'^tests/$', views.tests),
]
