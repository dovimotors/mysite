from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^service/$',views.service, name='service'),
    url(r'^parts_detail/$',views.parts_detail, name='parts_detail'),
]