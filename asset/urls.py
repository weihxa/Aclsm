"""xbman_cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from asset import views

urlpatterns = [
    url(r'^index/$',views.index,name="dashboards"),
    # url(r'report/$', views.asset_report, name='asset_report'),
    # url(r'report/asset_with_no_asset_id/$', views.asset_with_no_asset_id, name='acquire_asset_id'),
    url(r'^update_cmdb$', views.update_cmdb, name="update_cmdb"),
    url(r'^get_notice_num', views.get_notice_num, name="get_notice_num"),
    url(r'^get_notice_list', views.get_notice_list, name="get_notice_list"),
    url(r'^asset_list/$', views.asset_list, name="asset_list"),
    url(r'^asset_list/(\d+)/$', views.asset_detail, name="asset_detail"),
    url(r'^asset_list/list/$', views.get_asset_list, name="get_asset_list"),
    url(r'^asset_list/category/$', views.asset_category, name="asset_category"),
    url(r'^asset_list/Cabinet/$', views.asset_Cabinet, name="asset_Cabinet"),
    url(r'^asset_Knifebox_logs/(\d+)/$', views.asset_Knifebox_logs, name="asset_Knifebox_logs"),
]
