from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^service/$',views.service, name='service'),
    url(r'^parts_detail/(?P<start_days>[0-9]+)/(?P<end_days>[0-9]+)/$',views.parts_detail, name='parts_detail'),
    url(r'^all_metrics/$',views.all_metrics, name='all_metrics'),
]