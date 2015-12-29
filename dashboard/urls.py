from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^service/$',views.service, name='service'),
    url(r'^parts/$',views.parts, name='parts'),
]