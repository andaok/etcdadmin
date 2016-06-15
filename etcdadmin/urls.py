"""etcdadmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from action import views as action_views

urlpatterns = [
    # operator
    url(r'^admin/', admin.site.urls),
    url(r'^$', action_views.home, name='home'),

    # etcd clusters
    url(r'^cluster/add/$', action_views.add_etcd_cluster, name='addetcdcluster'),

    # etcd cluster dirs
    url(r'^ec-(\d{4})/keys/$', action_views.get_dir, name='getdir'),
    url(r'^ec-(\d{4})/keys/set/$', action_views.set_key, name='setkey'),
    url(r'^ec-(\d{4})/keys/update/(?P<key>.*)', action_views.update_key, name='updatekey'),
    url(r'^ec-(\d{4})/keys/del/(?P<key>.*)', action_views.delete_key, name='delkey'),
    
    # etcd cluster state
    url(r'^status/ec-(\d{4})', action_views.ec_status, name='etcdcluster_status'),

    # etcd cluster reset api
    #url(r'^api/', 'action.views.api.*', name='api'),
]
