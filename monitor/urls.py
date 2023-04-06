from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('speed-test/', views.speed_test, name='speed_test'),
    path('check-iis-uptime/', views.check_iis_uptime, name='check_iis_uptime'),
    path('ping-servers/', views.ping_servers, name='ping_servers'),
    path('check-mysql-service/', views.check_mysql_service, name='check_mysql_service'),
    path('ping-mno-links/', views.ping_mno_links, name='ping_mno_links'),
    path('ping-national-switch/', views.ping_national_switch, name='ping_national_switch'),
    path('check-mx-record/<str:mx_record>/', views.check_mx_record, name='check_mx_record'),
]
