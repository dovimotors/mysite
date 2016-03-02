from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^service/$',views.service, name='service'),
    url(r'^parts_detail/(?P<start_days>[0-9]+)/(?P<end_days>[0-9]+)/(?P<field>[A-Z]+)/(?P<cost>[0-9]+)/$',views.parts_detail, name='parts_detail'),
    url(r'^parts_detail/(?P<start_days>[0-9]+)/(?P<end_days>[0-9]+)/(?P<field>[A-Z]+)/$',views.parts_detail, name='parts_detail'),
    url(r'^all_metrics/$',views.all_metrics, name='all_metrics'),
    url(r'^parts_reports/$',views.parts_reports, name='parts_reports'),
    url(r'^weather_chart_view/$',views.weather_chart_view, name='weather_chart_view'),
]