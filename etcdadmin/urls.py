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
from django.contrib.auth import views as auth_views
from action import views as action_views
from account import views as account_views
from api import views as api_views


urlpatterns = [
    # account
    url(r'^admin/', admin.site.urls),
    url(r'^$', account_views.home, name='home'),
    url(r'^accounts/login/$', auth_views.login),
    #url(r'^accounts/login/$', account_views.login),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/accounts/login'}),

    # etcd clusters
    url(r'^ecs$', action_views.ecs_list, name='ecs_list'),
    url(r'^ec/add/$', action_views.add_ec, name='add_ec'),
    url(r'^ec/check/$', action_views.check_ec, name='check_ec'),
    url(r'^ec/update/$', action_views.update_ec, name='update_ec'),
    url(r'^ec/del/$', action_views.delete_ec, name='del_ec'),
    url(r'^status/ec-(?P<ecsn>[0-9a-z-]+)', action_views.ec_status, name='ec_status'),
    url(r'^ec-(?P<ecsn>[0-9a-z-]+)/keys/$', action_views.get_dir, name='get_dir'),
    url(r'^ec-(?P<ecsn>[0-9a-z-]+)/keys/set/$', action_views.set_key, name='set_key'),
    url(r'^ec-(?P<ecsn>[0-9a-z-]+)/keys/update/$', action_views.update_key, name='update_key'),
    url(r'^ec-(?P<ecsn>[0-9a-z-]+)/keys/del/$', action_views.delete_key, name='del_key'),
    
    # etcdadmin restfull api
    #url(r'^api/', 'action.views.api.*', name='api'),
    url(r'^healthcheck$', api_views.healthcheck, name='healthcheck'),
]
