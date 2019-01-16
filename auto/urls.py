from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index1),
    url(r'^pag(?P<pIndex>[0-9]*)/$', views.index),
    url(r'^pag[0-9]*/(([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])/pag(?P<pIndex>[0-9]*)/$', views.status),
]
