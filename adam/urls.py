from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^list/$',views.list, name='list'),
    url(r'^export/(?P<path_id>[0-9]+)/$',views.export, name='export'),
    url(r'^test/(?P<path_id>[0-9]+)/$',views.test, name='test'),
    url(r'^(?P<path_id>[0-9]+)/$', views.detail, name='detail')
]