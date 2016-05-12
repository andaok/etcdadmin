#-*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from etcdadmin.settings import ETCDCLUSTER_PREFIX

#from .models import EtcdCluster

import etcd 

eClient = etcd.Client(host="192.168.55.2", port=4001, protocol="http", allow_reconnect=True)

def home(request):
    
    return render_to_response('home.html', context_instance=RequestContext(request))


def get_dir(request):
    
    dirs = eClient.read(str(ETCDCLUSTER_PREFIX), recursive=True, sorted=True) 
    
#     for child in r.children:
#         print(child.key, child.value)
        
    return render_to_response(
        'getdir.html', {
            "dirs": dirs
        },
        context_instance=RequestContext(request)
    )


#def update_key(request, key, value=None):
#    key_str = str(key)
#    eClient.write(key_str, value)
#    eClient.update(result)
#    return render_to_response(
#        'updatekey.html',
#        context_instance=RequestContext(request)
#    )

   
#def set_key(request, key, value=None):
#    key_str = str(key)
#    eClient.write(key_str, value)
#    return render_to_response(
#        'setkey.html',
#        context_instance=RequestContext(request)
#    )
#


