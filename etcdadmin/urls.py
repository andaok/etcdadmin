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
from api import views as api_views


urlpatterns = [
    # operator
    url(r'^admin/', admin.site.urls),
    url(r'^$', action_views.home, name='home'),

    # etcd clusters
    url(r'^cluster/add/$', action_views.add_ec, name='addetcdcluster'),
    url(r'^cluster/check/$', action_views.check_ec, name='checketcdcluster'),
    #url(r'^cluster/update/$', action_views.update_ec, name='updateetcdcluster'),
    url(r'^cluster/del/$', action_views.delete_ec, name='deletcdcluster'),
    url(r'^status/ec-(?P<ecsn>[0-9a-z-]+)', action_views.ec_status, name='etcdcluster_status'),
    
    # etcd cluster dirs
    url(r'^ec-(?P<ecsn>[0-9a-z-]+)/keys/$', action_views.get_dir, name='getdir'),
    url(r'^ec-(?P<ecsn>[0-9a-z-]+)/keys/set/$', action_views.set_key, name='setkey'),
    url(r'^ec-(?P<ecsn>[0-9a-z-]+)/keys/update/$', action_views.update_key, name='updatekey'),
    url(r'^ec-(?P<ecsn>[0-9a-z-]+)/keys/del/$', action_views.delete_key, name='delkey'),
    
    # etcd cluster reset api
    #url(r'^api/', 'action.views.api.*', name='api'),
    
    # etcdadmin reset api
    url(r'^healthcheck$', api_views.healthcheck, name='healthcheck'),
]
