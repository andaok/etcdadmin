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

urlpatterns = [
    # operator
    url(r'^admin/', admin.site.urls),
    url(r'^keys/$', 'action.views.home', name='home'),
    url(r'^keys/(?P<key>.*)', 'action.views.get_dir', name='getdir'),
#    url(r'^keys/set/(?P<key>.*)', 'action.views.set_key', name='setkey'),
#    url(r'^keys/update/(?P<key>.*)', 'action.views.update_key', name='updatekey'),
#    url(r'^keys/del/(?P<key>.*)', 'action.views.del_key', name='delkey'),
#    url(r'^status', 'action.views.status', name='etcdstatus'),
#    
    # reset api
    #url(r'^api/', 'action.views.api.*', name='api'),
]
