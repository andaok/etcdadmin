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
    url(r'^(\d{4})/keys/$', action_views.get_dir, name='getdir'),
    url(r'^(\d{4})/keys/set/(?P<key>.*)', action_views.set_key, name='setkey'),
    url(r'^(\d{4})/keys/update/(?P<key>.*)', action_views.update_key, name='updatekey'),
    url(r'^(\d{4})/keys/del/(?P<key>.*)', action_views.delete_key, name='delkey'),
#    url(r'^status', 'action_views.status', name='etcdstatus'),

    # reset api
    #url(r'^api/', 'action.views.api.*', name='api'),
]
